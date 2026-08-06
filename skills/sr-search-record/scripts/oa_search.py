#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oa_search.py · 系统综述检索执行器（OpenAlex 主引擎 + Europe PMC 补充）

给 `sr-search-record` skill 调用。只做机械动作：跑检索、数命中、抓全量、查种子召回、
引文追踪、去重。**不做任何纳入排除判断**——那是 AI + 人的事。

子命令
  probe      逐块累加命中数（生成 S1..Sn 检索记录表的原始数据）
  recall     检查种子文献（DOI）是否被当前检索式召回
  fetch      游标翻页全量抓取，落 CSV + JSONL
  cite       对已纳入文献做前向/后向引文追踪，产出候选补漏集
  epmc       Europe PMC 补充检索（医学健康题目，支持 MeSH）
  rank       records.csv → 按相关度排好序的筛选台账骨架（**只排序不排除**）
  merge      合并分片筛选结果回台账 + 报进度与续跑位置
  add        手工补充文献进台账（书 / 书章 / 库外经典），found_via=manual

配置文件（JSON，UTF-8）
{
  "field": "title_and_abstract",          // 可选 title / title_and_abstract / fulltext
  "blocks": [
    {"name": "AI",     "terms": ["artificial intelligence", "machine learning"]},
    {"name": "采纳",   "terms": ["adoption", "implementation"]}
  ],
  "filters": {"publication_year": "2015-2026", "type": "article", "language": "en"},
  "sentinels": ["10.1016/j.jik.2025.100682"],
  "review_type": "systematic"          // systematic / semi-systematic / integrative
}                                       // 决定可筛区间、超限处置与终止规则（见 PROFILES）

用法
  python3 oa_search.py probe  -c config.json
  python3 oa_search.py recall -c config.json
  python3 oa_search.py fetch  -c config.json -o RV_综述/02_检索筛选/records
  python3 oa_search.py cite   -c config.json --dois-file included_dois.txt -o .../补漏
  python3 oa_search.py epmc   -q '(AI) AND (MESH:"Education, Nursing")' -o .../epmc

约定：所有请求带 mailto 进 OpenAlex 礼貌池；失败重试 3 次；不静默吞错。
"""

import argparse
import collections
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OA_BASE = "https://api.openalex.org/works"
EPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
MAILTO = os.environ.get("OPENALEX_MAILTO", "").strip()
UA = "sr-search-record/1.0 (systematic review search; AI academic workflow)"
PAUSE = 0.12


# ---------------------------------------------------------------- HTTP

def _get(url, tries=5):
    """指数退避。OpenAlex 限流（429）时不要立刻放弃——限流是常态，不是失败。"""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = "HTTP %s %s" % (e.code, e.reason)
            if e.code in (429, 500, 502, 503):
                wait = min(60, 4 * (2 ** i))
                sys.stderr.write("[oa_search] %s，%d 秒后重试（第 %d/%d 次）\n" % (last, wait, i + 1, tries))
                time.sleep(wait)
                continue
            break
        except Exception as e:  # noqa: BLE001
            last = str(e)
            time.sleep(min(30, 3 * (2 ** i)))
    die("请求失败：%s\n  URL: %s\n"
        "  429 持续不退时的降级出路：等 30–60 分钟再跑；或把 filters.publication_year 拆成几段分批抓，\n"
        "  抓到的部分照常进流程，覆盖缺口写进检索记录的降级记录节——**不要因为限流停下整条流水线**。"
        % (last, url))


def oa(params):
    p = dict(params)
    if MAILTO:
        p["mailto"] = MAILTO
    time.sleep(PAUSE)
    return _get(OA_BASE + "?" + urllib.parse.urlencode(p))


def die(msg):
    sys.stderr.write("\n[oa_search] " + msg + "\n")
    sys.exit(1)


# ---------------------------------------------------------------- 配置 → 检索式

def load_cfg(path):
    if not os.path.exists(path):
        die("配置文件不存在：%s" % path)
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    if not cfg.get("blocks"):
        die("配置里没有 blocks（概念块）")
    for b in cfg["blocks"]:
        if not b.get("terms"):
            die("概念块 %s 没有 terms" % b.get("name", "?"))
    cfg.setdefault("field", "title_and_abstract")
    cfg.setdefault("filters", {})
    cfg.setdefault("sentinels", [])
    rt = str(cfg.get("review_type", "systematic")).strip().lower().replace("_", "-")
    if rt not in PROFILES:
        die("review_type 只能是 systematic / semi-systematic / integrative，收到：%s" % rt)
    cfg["review_type"] = rt
    return cfg


# ---- 全型共用的规模目标（摘要层定稿模式） ----
# 阶段 1 校准把命中压到 CAL_OK 里；阶段 2 按相关性排序截断到 SHORTLIST 条；
# 阶段 3 摘要筛选把 include 收敛到 INCLUDE_BAND。三个数一致，流程才闭得上。
CAL_OK = (300, 2000)      # 检索式校准的目标命中区间
SHORTLIST = 300           # 进入摘要筛选的候选数（截断线初值）
SHORTLIST_MAX = 900       # 扩线上限（最多扩 2 次：300 → 600 → 900）
INCLUDE_BAND = (60, 100)  # 摘要层 include 的目标带
PRECISION_LIMIT = 1000000  # 单个概念块命中超过它 = 该块混进了泛词，必须收紧

# 三型档位：检索内核与筛选内核完全共用，只有**报告规范与出表形状**按型切换。
# 摘要层定稿模式下三型都不做全文筛选——这是明示的方法学让步，写进局限，不伪装成完整 PRISMA。
PROFILES = {
    "systematic": {
        "label": "系统综述（PRISMA）", "goal": "尽可能完整地识别合格研究（摘要层定稿）",
        "ok": CAL_OK, "warn": 20000,
        "over": "偏大：交给阶段 2 的相关性排序截断，**不要为压数字收窄纳入标准或删种子**；"
                "但**含泛词的块必须收紧**（判据：种子召回不下降）",
        "far": "过宽，必须先收紧最泛的块或加限制器，再谈截断",
        "stop": "种子召回 100% + 命中落 300–2,000 + 本轮无改动",
        "note": "PRISMA 要求全文评估。本模式只在题摘层定稿，**产出须写明这一偏离**。",
    },
    "semi-systematic": {
        "label": "半系统 / 叙事综述（RAMESES）", "goal": "覆盖主要研究传统 / 主题，不追求穷尽",
        "ok": CAL_OK, "warn": 50000,
        "over": "交给阶段 2 排序截断（比随机抽样召回效率高得多）；同时收紧含泛词的块",
        "far": "过宽，先收紧最泛的块，或缩小时间窗并说明理由",
        "stop": "种子召回 100% + 命中落 300–2,000 + 本轮无改动",
        "note": "RAMESES 不强制全文评估层，本模式与该型不冲突。",
    },
    "integrative": {
        "label": "整合式综述（Torraco）", "goal": "覆盖构成概念论证所需的文献",
        "ok": CAL_OK, "warn": 20000,
        "over": "交给阶段 2 排序截断，并写明选择标准与理由（否则批判性整合站不住）",
        "far": "过宽，收紧概念块——整合式综述的语料应当是精选的",
        "stop": "种子召回 100% + 命中落 300–2,000 + 本轮无改动",
        "note": "Torraco 不强制全文评估层，本模式与该型不冲突。",
    },
}


def clean_term(t):
    """OpenAlex filter 语法里 , 是 AND、| 是 OR，词里出现会破坏解析。"""
    t = re.sub(r"[,|]", " ", str(t)).strip()
    t = re.sub(r"\s+", " ", t)
    return t


def block_filter(field, block):
    terms = []
    for t in block["terms"]:
        t = clean_term(t)
        if not t:
            continue
        terms.append('"%s"' % t if " " in t else t)
    return "%s.search:%s" % (field, "|".join(terms))


def base_filters(cfg):
    """限制器（年份/类型/语言）单独一组，便于 probe 分开报告。"""
    out = []
    f = cfg["filters"]
    for k in ("publication_year", "type", "language", "is_oa", "primary_topic.domain.id"):
        if f.get(k):
            out.append("%s:%s" % (k, f[k]))
    for k, v in f.items():  # 允许配置里写别的 OpenAlex filter
        if k not in ("publication_year", "type", "language", "is_oa", "primary_topic.domain.id") and v:
            out.append("%s:%s" % (k, v))
    return out


def count_of(filters):
    d = oa({"filter": ",".join(filters), "per_page": 1})
    return d["meta"]["count"]


# ---------------------------------------------------------------- probe

def cmd_probe(cfg, args):
    field, blocks = cfg["field"], cfg["blocks"]
    bf = [block_filter(field, b) for b in blocks]
    lim = base_filters(cfg)

    rows, wide = [], []
    for i, b in enumerate(blocks):
        c = count_of([bf[i]])
        rows.append((b.get("name", "块%d" % (i + 1)),
                     "单块：" + " OR ".join(b["terms"]), c))
        if c > PRECISION_LIMIT:
            wide.append((b.get("name", "块%d" % (i + 1)), c,
                         [t for t in b["terms"] if " " not in clean_term(t)]))
    n = len(blocks)
    for i in range(2, n + 1):
        rows.append(("S1–S%d 组合" % i,
                     " AND ".join(b.get("name", "?") for b in blocks[:i]), count_of(bf[:i])))
    final_no_lim = rows[-1][2]
    if lim:
        rows.append(("加限制器", "；".join(lim), count_of(bf + lim)))
    rows = [("S%d" % (i + 1),) + r for i, r in enumerate(rows)]

    print("\n检索记录表（原始数据 · OpenAlex，检索日期 %s）" % time.strftime("%Y-%m-%d"))
    print("| # | 概念块 / 步骤 | 内容 | 命中数 |")
    print("|---|---|---|---|")
    for r in rows:
        print("| %s | %s | %s | %s |" % (r[0], r[1], r[2], format(r[3], ",")))
    final = rows[-1][3]
    print("\n最终命中：%s" % format(final, ","))
    print("检索式（可复跑）：%s" % urllib.parse.unquote(",".join(bf + lim)))
    pf = PROFILES[cfg["review_type"]]
    lo, hi = pf["ok"]
    print("综述型：%s · 检索目标：%s" % (pf["label"], pf["goal"]))

    # ---- 精度守卫：单块命中过大 = 该块混进了泛词，先修词再谈规模 ----
    if wide:
        print("\n!! 精度守卫触发：以下概念块单块命中超过 %s，几乎肯定混进了泛词。"
              % format(PRECISION_LIMIT, ","))
        for name, c, singles in wide:
            print("   · 「%s」命中 %s；块内单词级词条：%s"
                  % (name, format(c, ","), "、".join(singles) if singles else "（无，检查短语是否过泛）"))
        print("   处置：删掉这些块里语义不专属的单词（如 verification / accountability / autonomy /")
        print("   responsibility / subjectivity 这类各学科通用词），改用精确短语。")
        print("   **合法性判据：改动前后 `recall` 的种子召回率不下降。** 守住这条就是纯赚精度，")
        print("   不算「为压数字改标准」——这与硬约束 6 不冲突，硬约束 6 禁的是提高纳入门槛。")

    if final == 0:
        print("!! 命中 0：概念块过窄或术语拼写有误，必须改式子重跑。")
    elif final < lo:
        print("!! 命中 <%d：偏窄，建议给命中最少的块补同义词。" % lo)
    elif final > pf["warn"]:
        print("!! 命中 >%s：%s" % (format(pf["warn"], ","), pf["far"]))
    elif final > hi:
        print("命中 %s（超出 %d–%d）：%s" % (format(final, ","), lo, hi, pf["over"]))
    else:
        print("命中数落在目标区间（%d–%d）。" % (lo, hi))
    print("终止规则：%s" % pf["stop"])
    print("下一步规模链：抓全量 → rank --shortlist %d 截断 → 摘要筛选 → include 收敛到 %d–%d"
          % (SHORTLIST, INCLUDE_BAND[0], INCLUDE_BAND[1]))
    print("本型报告提示：%s" % pf["note"])
    print("（未加限制器的组合命中：%s）" % format(final_no_lim, ","))
    return rows


# ---------------------------------------------------------------- recall

def norm_doi(d):
    if not d:
        return ""
    d = str(d).strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d


def cmd_recall(cfg, args):
    sentinels = [norm_doi(x) for x in (args.dois or cfg.get("sentinels") or []) if norm_doi(x)]
    if args.dois_file:
        with open(args.dois_file, encoding="utf-8") as f:
            sentinels += [norm_doi(l) for l in f if norm_doi(l)]
    sentinels = [s for s in dict.fromkeys(sentinels)]
    if not sentinels:
        die("没有种子 DOI：配置里写 sentinels，或用 --dois / --dois-file")

    field = cfg["field"]
    bf = [block_filter(field, b) for b in cfg["blocks"]]
    lim = base_filters(cfg)

    print("\n种子文献召回检查（%d 篇）" % len(sentinels))
    print("| DOI | 全式命中 | 未命中时：哪些块没过 |")
    print("|---|---|---|")
    miss = []
    for d in sentinels:
        hit = count_of(bf + lim + ["doi:%s" % d]) > 0
        why = "—"
        if not hit:
            bad = []
            in_oa = count_of(["doi:%s" % d]) > 0
            if not in_oa:
                why = "OpenAlex 无此 DOI（核对 DOI 是否正确）"
            else:
                for i, b in enumerate(cfg["blocks"]):
                    if count_of([bf[i], "doi:%s" % d]) == 0:
                        bad.append(b.get("name", "块%d" % (i + 1)))
                for l in lim:
                    if count_of([l, "doi:%s" % d]) == 0:
                        bad.append("限制器 " + l)
                why = "、".join(bad) if bad else "组合后丢失（检查字段范围）"
            miss.append((d, why))
        print("| %s | %s | %s |" % (d, "✅" if hit else "❌", why))
    rate = (len(sentinels) - len(miss)) / len(sentinels)
    print("\n召回率：%d/%d = %.0f%%" % (len(sentinels) - len(miss), len(sentinels), rate * 100))
    if miss:
        print("!! 未达 100%，不进入全量抓取：先给上面标出的块补同义词，再重跑 probe + recall。")
    else:
        print("种子全召回，可以进入 fetch 全量抓取。")
    return miss


# ---------------------------------------------------------------- fetch

SELECT = ("id,doi,display_name,publication_year,publication_date,type,language,"
          "primary_location,authorships,cited_by_count,referenced_works_count,"
          "abstract_inverted_index,open_access")


def inv_to_abstract(ii):
    if not ii:
        return ""
    pos = {}
    for term, ps in ii.items():
        for p in ps:
            pos[p] = term
    return " ".join(pos[k] for k in sorted(pos))


def norm_title(t):
    return re.sub(r"[^a-z0-9一-鿿]+", "", (t or "").lower())


def flatten(w, field, blocks):
    loc = (w.get("primary_location") or {}).get("source") or {}
    auth = [a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])]
    ab = inv_to_abstract(w.get("abstract_inverted_index"))
    hay = ((w.get("display_name") or "") + " " + ab).lower()
    hits = [b.get("name", "块%d" % (i + 1)) for i, b in enumerate(blocks)
            if any(clean_term(t).lower() in hay for t in b["terms"])]
    return {
        "uid": norm_doi(w.get("doi")) or (w.get("id") or "").rsplit("/", 1)[-1],
        "openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
        "doi": norm_doi(w.get("doi")),
        "title": w.get("display_name") or "",
        "year": w.get("publication_year") or "",
        "date": w.get("publication_date") or "",
        "journal": loc.get("display_name") or "",
        "authors": "; ".join([a for a in auth if a]),
        "type": w.get("type") or "",
        "language": w.get("language") or "",
        "cited_by": w.get("cited_by_count", 0),
        "n_refs": w.get("referenced_works_count", 0),
        "oa_url": ((w.get("open_access") or {}).get("oa_url") or ""),
        "blocks_hit": "|".join(hits),
        "n_blocks_hit": len(hits),
        "has_abstract": "Y" if ab else "N",
        "abstract": ab,
    }


def pull(filters, blocks, field, cap=0, stats=None):
    """翻页抓取并去重。stats 传入一个 dict 时回填：
       raw      = 实际遍历过的原始记录数（不是 meta.count）
       dups     = 因同 DOI / 同题名被去掉的条数
       truncated= 是否因 cap 提前停止（此时"没抓到的"不等于"重复的"）"""
    out, cursor, seen = [], "*", set()
    raw = dups = 0
    truncated = False
    while True:
        d = oa({"filter": ",".join(filters), "per_page": 200, "cursor": cursor, "select": SELECT})
        for w in d["results"]:
            raw += 1
            r = flatten(w, field, blocks)
            key = r["doi"] or norm_title(r["title"])
            if key in seen:
                dups += 1
                continue
            seen.add(key)
            out.append(r)
        cursor = (d.get("meta") or {}).get("next_cursor")
        if not cursor or not d["results"]:
            break
        if cap and len(out) >= cap:
            truncated = True
            break
    if stats is not None:
        stats.update({"raw": raw, "dups": dups, "truncated": truncated})
    return out


COLS = ["uid", "doi", "title", "year", "date", "journal", "authors", "type", "language",
        "cited_by", "n_refs", "oa_url", "blocks_hit", "n_blocks_hit", "has_abstract",
        "found_via", "abstract"]


def write_out(rows, out_base, extra_note=""):
    os.makedirs(os.path.dirname(os.path.abspath(out_base)) or ".", exist_ok=True)
    with open(out_base + ".csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with open(out_base + ".jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("已写出 %d 条 → %s.csv / .jsonl %s" % (len(rows), out_base, extra_note))


def cmd_fetch(cfg, args):
    field, blocks = cfg["field"], cfg["blocks"]
    pf = PROFILES[cfg["review_type"]]
    filters = [block_filter(field, b) for b in blocks] + base_filters(cfg)
    total = count_of(filters)
    print("检索式命中 %s 条，开始游标翻页抓取…（%s）" % (format(total, ","), pf["label"]))
    if total > pf["warn"] and not args.force:
        die("命中 %s 条 > %s：%s（确要抓取加 --force）"
            % (format(total, ","), format(pf["warn"], ","), pf["far"]))
    if total > pf["ok"][1]:
        print("!! 超出本型可筛区间 %d–%d：%s" % (pf["ok"][0], pf["ok"][1], pf["over"]))
    st = {}
    rows = pull(filters, blocks, field, cap=args.cap, stats=st)
    for r in rows:
        r["found_via"] = "database:OpenAlex"
    n_ab = sum(1 for r in rows if r["has_abstract"] == "Y")
    write_out(rows, args.out)
    print("摘要覆盖：%d/%d (%.0f%%)；无摘要的不得据题名排除，保留到全文阶段。"
          % (n_ab, len(rows), 100.0 * n_ab / max(len(rows), 1)))
    if st.get("truncated"):
        print("!! 抓取被 --cap %d 截断：只遍历了前 %s 条（其中同 DOI/同题名重复 %d 条），"
              "检索式实际命中 %s 条，**还有约 %s 条没抓**。"
              % (args.cap, format(st["raw"], ","), st["dups"],
                 format(total, ","), format(max(total - st["raw"], 0), ",")))
        print("!! 没抓到的那部分**不是去重差额，不得写进 PRISMA**。"
              "PRISMA 的 Identification / 去重 / 待筛三个数必须用不带 --cap 的完整抓取产生；"
              "本次结果只能当试跑样本用。")
    else:
        print("PRISMA · Identification：数据库检索命中 %s，遍历 %s 条，去重删除 %d 条（同 DOI/同题名），去重后待筛 %d 条"
              % (format(total, ","), format(st.get("raw", len(rows)), ","), st.get("dups", 0), len(rows)))
        if st.get("raw") is not None and st["raw"] != total:
            print("   注：API 报的命中数（%s）与实际遍历数（%s）差 %d 条——写方法节时以**遍历数**为准并说明差异（OpenAlex 的 meta.count 是估算值，翻页时可能有出入）。"
                  % (format(total, ","), format(st["raw"], ","), abs(total - st["raw"])))
    return rows


# ---------------------------------------------------------------- cite

def cmd_cite(cfg, args):
    dois = [norm_doi(x) for x in (args.dois or [])]
    if args.dois_file:
        with open(args.dois_file, encoding="utf-8") as f:
            dois += [norm_doi(l) for l in f if norm_doi(l)]
    dois = [d for d in dict.fromkeys(dois) if d]
    if not dois:
        die("没有种子 DOI：用 --dois 或 --dois-file 给已纳入文献")

    field, blocks = cfg["field"], cfg["blocks"]
    lim = base_filters(cfg)
    known = set(dois)
    if args.known_csv and os.path.exists(args.known_csv):
        with open(args.known_csv, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if row.get("doi"):
                    known.add(norm_doi(row["doi"]))

    seeds, back_ids = [], []
    for d in dois:
        r = oa({"filter": "doi:%s" % d, "per_page": 1, "select": "id,referenced_works"})
        if r["results"]:
            w = r["results"][0]
            seeds.append((w["id"].rsplit("/", 1)[-1], d))
            back_ids += [x.rsplit("/", 1)[-1] for x in (w.get("referenced_works") or [])]
        else:
            print("  ! OpenAlex 查不到 %s，跳过（记入待人工处理）" % d)
    print("种子 %d 篇；后向参考文献 %d 条（去重前）" % (len(seeds), len(back_ids)))

    rows = []
    back_ids = list(dict.fromkeys(back_ids))
    for i in range(0, len(back_ids), 50):
        chunk = "|".join(back_ids[i:i + 50])
        for w in pull(["openalex_id:" + chunk] + lim, blocks, field):
            w["found_via"] = "citation:backward"
            rows.append(w)
    for oid, d in seeds:
        for w in pull(["cites:" + oid] + lim, blocks, field):
            w["found_via"] = "citation:forward(%s)" % d
            rows.append(w)

    seen, uniq = set(), []
    for r in rows:
        k = r["doi"] or norm_title(r["title"])
        if k in seen or k in known:
            continue
        seen.add(k)
        uniq.append(r)
    keep = [r for r in uniq if r["n_blocks_hit"] >= args.min_blocks]
    print("引文追踪去重后新增 %d 条；其中命中 ≥%d 个概念块的 %d 条进入待筛。"
          % (len(uniq), args.min_blocks, len(keep)))
    write_out(keep, args.out, "（引文追踪补漏，尚未筛选）")
    return keep


# ---------------------------------------------------------------- rank / merge（筛选台账）

SCREEN_COLS = ["seq", "uid", "doi", "title", "year", "journal", "has_abstract", "n_blocks_hit",
               "found_via", "oa_url", "rank_score", "pass1", "ai_decision", "ai_reason",
               "pdf_status", "evidence_level",
               "reviewer_1", "reviewer_2", "final_decision", "note"]
# AI 可写：摘要筛选 + （③ 成文阶段回填的）全文获取状态与证据级别
# ft_decision / ft_reason 已退休——摘要层定稿模式只有一层判定，ai_decision 就是纳入决定。
DECISION_COLS = ["pass1", "ai_decision", "ai_reason", "pdf_status", "evidence_level"]
# 只能人填
HUMAN_COLS = ["reviewer_1", "reviewer_2", "final_decision", "note"]
# 排序截断线以外的记录：**不是排除**，是"未进入筛选"，PRISMA/选择流程说明里单列
LOWRANK = "not-screened-lowrank"


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_screen(rows, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCREEN_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


_TERM_RE = {}


def term_re(t):
    """词边界匹配，避免 `LLM` 命中 `allmost`、`autonomy` 命中 `autonomous`。"""
    r = _TERM_RE.get(t)
    if r is None:
        r = re.compile(r"(?<![a-z0-9])" + re.escape(t.lower()) + r"(?![a-z0-9])")
        _TERM_RE[t] = r
    return r


def term_weight(t):
    """精确短语 3 分，单词 1 分。

    这是压制泛词噪音最直接的杠杆：一条只靠 `responsibility` 命中的记录，
    和一条命中 `epistemic responsibility` 的记录，相关性不是一个量级。
    """
    return 3 if " " in clean_term(t) else 1


def relevance(r, blocks):
    """相关性总分 = Σ_块 (题名最佳词权 × 2 + 摘要最佳词权)。

    题名权重加倍：概念出现在题名里，说明它是这篇文章讲的东西，而不是背景里带一句。
    """
    title = (r.get("title") or "").lower()
    abstract = (r.get("abstract") or "").lower()
    total = 0
    for b in blocks:
        tw = aw = 0
        for t in b["terms"]:
            t = clean_term(t)
            if not t:
                continue
            w = term_weight(t)
            rx = term_re(t)
            if w > tw and rx.search(title):
                tw = w
            if w > aw and rx.search(abstract):
                aw = w
        total += tw * 2 + aw
    return total


def cmd_rank(args):
    """把 records.csv（可多份）排成筛选台账骨架，并按相关性截断出候选集。

    与旧版的区别：旧版"只排序不排除、全部要筛完"，在命中上万时无法执行，
    实跑退化成了 1% 随机抽样。现在改为**按相关性排序后截断**——
    截断线以外的标 not-screened-lowrank，**不是排除**，如实写进选择流程说明。
    同样是"未穷尽"，但截断的召回效率远高于随机抽样。
    """
    if os.path.exists(args.out) and not args.overwrite:
        try:
            done = sum(1 for r in read_csv(args.out) if r.get("ai_decision"))
        except Exception:  # noqa: BLE001
            done = 0
        if done:
            die("台账 %s 已存在且已有 %d 条判定——重跑 rank 会把它们清空。\n"
                "  续跑筛选：直接从第一条 ai_decision 为空的记录接着筛，不要重跑 rank。\n"
                "  确实要重建：加 --overwrite（先备份）。" % (args.out, done))
    src = []
    for p in args.inputs:
        if not os.path.exists(p):
            die("输入不存在：%s" % p)
        src += read_csv(p)
    seen, rows = set(), []
    for r in src:
        k = norm_doi(r.get("doi")) or norm_title(r.get("title"))
        if k in seen:
            continue
        seen.add(k)
        rows.append(r)
    print("合并 %d 份输入，共 %d 条（去重删 %d）" % (len(args.inputs), len(rows), len(src) - len(rows)))

    blocks = load_cfg(args.config)["blocks"] if args.config else []
    if not blocks:
        print("!! 没给 -c 配置，无法按词权排序，退化为按命中块数 / 被引数排序（相关性会差很多）。")

    def score(r):
        try:
            nb = int(r.get("n_blocks_hit") or 0)
        except ValueError:
            nb = 0
        ab = 1 if r.get("has_abstract") == "Y" else 0
        try:
            cb = int(r.get("cited_by") or 0)
        except ValueError:
            cb = 0
        return (relevance(r, blocks) if blocks else 0, nb, ab, cb)

    scored = sorted(((score(r), r) for r in rows), key=lambda x: x[0], reverse=True)

    n = args.shortlist if args.shortlist is not None else SHORTLIST
    if n <= 0 or n >= len(scored):
        n = len(scored)
    out = []
    for i, (sc, r) in enumerate(scored, 1):
        o = {c: "" for c in SCREEN_COLS}
        o.update({k: r.get(k, "") for k in
                  ("uid", "doi", "title", "year", "journal", "has_abstract", "n_blocks_hit",
                   "found_via", "oa_url")})
        o["seq"] = i
        o["rank_score"] = sc[0]
        if i > n:
            o["pass1"] = LOWRANK  # 未进入筛选，**不是排除**
        out.append(o)
    write_screen(out, args.out)

    cut = out[n - 1]["rank_score"] if n else ""
    print("已写出筛选台账 %d 条 → %s" % (len(out), args.out))
    print("排序键：Σ_块(题名最佳词权 ×2 + 摘要最佳词权) → 命中块数 → 有无摘要 → 被引数")
    print("        词权：精确短语 3 分 / 单词 1 分（压制泛词噪音）")
    if n < len(out):
        print("\n**截断线 = 前 %d 条**（rank_score ≥ %s）进入摘要筛选；"
              "其余 %d 条标 %s。" % (n, cut, len(out) - n, LOWRANK))
        print("  截断不是排除：选择流程说明里单列一行「未进入筛选（低相关性排序）」。")
        print("  筛完若 include 不足 %d，用 `expand -b %s -n %d` 扩线，只筛新增部分。"
              % (INCLUDE_BAND[0], args.out, min(n * 2, SHORTLIST_MAX)))
    else:
        print("\n全部 %d 条都进入筛选（未触发截断）。" % len(out))
    dist = collections.Counter((r["n_blocks_hit"], r["has_abstract"]) for r in out[:n])
    print("候选集构成：")
    for k in sorted(dist, reverse=True)[:8]:
        print("  块数=%s 摘要=%s : %d 条" % (k[0] or "?", k[1] or "?", dist[k]))
    return out


def cmd_expand(args):
    """扩截断线：把 seq ≤ N 里被标为 not-screened-lowrank 的记录放回待筛。

    收敛闭环的一环——筛完 include 不够时扩线，**只筛新增的那批，已判定的一条都不动**。
    """
    base = read_csv(args.base)
    freed = 0
    for r in base:
        try:
            seq = int(r.get("seq") or 0)
        except ValueError:
            continue
        if seq <= args.n and r.get("pass1") == LOWRANK and not r.get("ai_decision"):
            r["pass1"] = ""
            freed += 1
    if not freed:
        print("没有可释放的记录（seq ≤ %d 的都已在待筛或已判定）。" % args.n)
        return base
    write_screen(base, args.base)
    still = sum(1 for r in base if r.get("pass1") == LOWRANK)
    print("截断线扩到 %d：释放 %d 条进入待筛；仍在线外 %d 条。" % (args.n, freed, still))
    print("**只筛这 %d 条新增的，已判定的不要重筛。**扩线动作要写进检索记录（含扩线前的 include 数与理由）。"
          % freed)
    return base


def cmd_add(args):
    """手工补充文献进台账（书 / 书章 / 数据库外的经典文献）。

    OpenAlex 对专著与书章的覆盖弱于期刊论文——整合式综述尤其容易漏掉最重要的一批。
    这个口子专门补它，补进来的记录 found_via = manual:<理由>，**在 PRISMA 里单列**。
    """
    base = read_csv(args.base)
    seen = {norm_doi(r.get("doi")) for r in base if norm_doi(r.get("doi"))}
    seen |= {norm_title(r.get("title")) for r in base if norm_title(r.get("title"))}
    try:
        nxt = max(int(r.get("seq") or 0) for r in base) + 1
    except ValueError:
        nxt = len(base) + 1

    new = []
    for d in (args.dois or []):
        d = norm_doi(d)
        if not d or d in seen:
            continue
        r = oa({"filter": "doi:%s" % d, "per_page": 1, "select": SELECT})
        if not r["results"]:
            print("  ! OpenAlex 查不到 %s —— 请改用 --csv 手工填题录（书 / 书章常见）" % d)
            continue
        new.append(flatten(r["results"][0], "title_and_abstract", []))
    if args.csv:
        for r in read_csv(args.csv):
            if not (r.get("title") or "").strip():
                die("--csv 每行至少要有 title：%s" % args.csv)
            new.append({"uid": norm_doi(r.get("doi")) or norm_title(r.get("title"))[:60],
                        "doi": norm_doi(r.get("doi")), "title": r.get("title", ""),
                        "year": r.get("year", ""), "journal": r.get("journal") or r.get("publisher", ""),
                        "has_abstract": "Y" if (r.get("abstract") or "").strip() else "N",
                        "n_blocks_hit": "", "oa_url": r.get("oa_url", "")})

    added = []
    for r in new:
        k = norm_doi(r.get("doi")) or norm_title(r.get("title"))
        if k in seen:
            continue
        seen.add(k)
        o = {c: "" for c in SCREEN_COLS}
        o.update({k2: r.get(k2, "") for k2 in
                  ("uid", "doi", "title", "year", "journal", "has_abstract", "n_blocks_hit", "oa_url")})
        o["seq"] = nxt
        o["found_via"] = "manual:%s" % (args.reason or "手工补充")
        nxt += 1
        added.append(o)
    if not added:
        print("没有新增（都已在台账里，或都没查到）。")
        return base
    write_screen(base + added, args.base)
    print("手工补充 %d 条 → %s（found_via=manual，seq 从 %d 起）"
          % (len(added), args.base, added[0]["seq"]))
    for r in added:
        print("  + %s %s" % (r.get("year") or "____", (r.get("title") or "")[:70]))
    print("这些记录走同样的筛选流程；**PRISMA 里要单列为「其他方法识别的记录」，不要混进数据库检索命中数。**")
    return base + added


def cmd_merge(args):
    """把分片写回的筛选结果合并进台账，并报进度与续跑位置。"""
    base = read_csv(args.base)
    parts = sorted(args.parts)
    # 三级匹配：uid → 归一化 DOI → 归一化题名（分片可能来自别的 id 体系）
    by_uid = {r["uid"]: r for r in base}
    by_doi = {norm_doi(r.get("doi")): r for r in base if norm_doi(r.get("doi"))}
    by_title = {norm_title(r.get("title")): r for r in base if norm_title(r.get("title"))}

    # 先全量校验，**不合规就一条都不写**
    guarded = sum(1 for p in parts for r in read_csv(p)
                  for c in HUMAN_COLS if r.get(c, ""))
    if guarded:
        die("分片里有 %d 处填写了 reviewer_1 / reviewer_2 / final_decision / note ——"
            "这四列只能由人填（硬约束 2）。**未写入任何内容**，请清空这些值后重跑 merge。" % guarded)

    applied, unknown, by_fallback = 0, 0, 0
    for p in parts:
        for r in read_csv(p):
            t = by_uid.get(r.get("uid", ""))
            if t is None:
                t = by_doi.get(norm_doi(r.get("doi"))) or by_title.get(norm_title(r.get("title")))
                if t is not None:
                    by_fallback += 1
            if t is None:
                unknown += 1
                continue
            for c in DECISION_COLS:
                if r.get(c, ""):
                    t[c] = r[c]
            applied += 1
    write_screen(base, args.base)
    if by_fallback:
        print("（%d 条靠 DOI / 题名回退匹配上，uid 体系与台账不同）" % by_fallback)
    if unknown:
        print("!! %d 条分片记录在台账里找不到对应，已忽略（检查是不是漏了把补漏集一起 rank 进台账）" % unknown)

    # 候选集 = 截断线以内的记录；线外的 not-screened-lowrank 是合法完成态，不算"未筛"
    pool = [r for r in base if r.get("pass1") != LOWRANK]
    lowrank = len(base) - len(pool)
    done = [r for r in pool if r.get("ai_decision")]
    todo = [r for r in pool if not r.get("ai_decision")]
    dist = collections.Counter(r["ai_decision"] for r in done)
    print("\n摘要筛选：%d / %d（%.1f%%）  合并了 %d 份分片、%d 条判定"
          % (len(done), len(pool), 100.0 * len(done) / max(len(pool), 1), len(parts), applied))
    if lowrank:
        print("  （台账共 %d 条，其中 %d 条在截断线外标 %s——**未进入筛选，不是排除**）"
              % (len(base), lowrank, LOWRANK))
    for k in ("include", "exclude", "unclear"):
        print("   %-8s %d" % (k, dist.get(k, 0)))
    if todo:
        nxt = todo[0]
        print("   **未筛 %d 条。续跑从 seq=%s 起**（uid=%s）。" % (len(todo), nxt.get("seq"), nxt.get("uid")))
        return base

    # ---- 收敛闭环：include 落带才算达标 ----
    inc = dist.get("include", 0)
    lo, hi = INCLUDE_BAND
    print("   **候选集全部筛完。**")
    print("\n收敛检查：include %d（目标 %d–%d）" % (inc, lo, hi))
    if inc < lo:
        nxt_n = min(len(pool) * 2, SHORTLIST_MAX)
        print("  → 偏少。扩截断线：`expand -b %s -n %d`，**只筛新增部分**，然后重跑 merge。"
              % (args.base, nxt_n))
        print("     扩线已达 %d 仍不足时：接受当前数字，如实记账，不再扩。" % SHORTLIST_MAX)
    elif inc > hi:
        print("  → 偏多。**不要扩线、也不要改纳入标准**：对 include 集按标准表里最核心的 1–2 条闸门")
        print("     再过一遍，边缘的降为 unclear（进候选池，**不是 exclude**），然后重跑 merge。")
    else:
        print("  → 达标。可以出表 + 入 Zotero 了。")
    print("  调整最多 2 次；两次后仍越界就接受当前数字并如实汇报，**不要为凑数字反复调**。")

    unc = dist.get("unclear", 0)
    if unc:
        print("\nunclear %d 条：全部保留进候选池交人复核（硬约束 3），不得自动排除。" % unc)
    print("\n摘要层定稿模式：ai_decision 就是纳入决定，没有全文筛选层。")
    print("  全文在 ③ 成文阶段 best-effort 获取，拿不到不改变纳入集，只影响 evidence_level。")
    print("  final_decision 仍由人填（本脚本拒绝 AI 写入）。")

    # 合并成功后归档分片，避免目录被空壳文件淹掉
    if not args.no_archive and parts:
        d = os.path.join(os.path.dirname(os.path.abspath(args.base)) or ".", "_parts")
        os.makedirs(d, exist_ok=True)
        moved = 0
        for p in parts:
            try:
                os.replace(p, os.path.join(d, os.path.basename(p)))
                moved += 1
            except OSError:
                pass
        if moved:
            print("\n已把 %d 份分片归档到 %s/（判定都在台账里了，分片只是续跑凭证）。" % (moved, d))
    return base


# ---------------------------------------------------------------- europe pmc

def cmd_epmc(args):
    rows, cursor, total = [], "*", None
    while True:
        p = {"query": args.query, "format": "json", "pageSize": 100,
             "cursorMark": cursor, "resultType": "core"}
        time.sleep(PAUSE)
        d = _get(EPMC_BASE + "?" + urllib.parse.urlencode(p))
        if total is None:
            total = d.get("hitCount", 0)
            print("Europe PMC 命中 %s 条" % format(total, ","))
            if total > 3000 and not args.force:
                die("命中过多，请收紧 query（或加 --force）")
        for w in d.get("resultList", {}).get("result", []):
            rows.append({
                "uid": norm_doi(w.get("doi")) or ("pmid:" + str(w.get("pmid") or w.get("id"))),
                "doi": norm_doi(w.get("doi")), "title": w.get("title") or "",
                "year": w.get("pubYear") or "", "date": w.get("firstPublicationDate") or "",
                "journal": w.get("journalTitle") or "", "authors": w.get("authorString") or "",
                "type": w.get("pubType") or "", "language": w.get("language") or "",
                "cited_by": w.get("citedByCount", 0), "n_refs": "", "oa_url": "",
                "blocks_hit": "", "n_blocks_hit": "", "abstract": w.get("abstractText") or "",
                "has_abstract": "Y" if w.get("abstractText") else "N",
                "found_via": "database:EuropePMC",
            })
        nxt = d.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
    seen, uniq = set(), []
    for r in rows:
        k = r["doi"] or norm_title(r["title"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    write_out(uniq, args.out, "（Europe PMC 补充检索）")
    print("query（可复跑）：%s" % args.query)
    return uniq


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="系统综述检索执行器（OpenAlex / Europe PMC）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("probe", "recall", "fetch", "cite"):
        s = sub.add_parser(name)
        s.add_argument("-c", "--config", required=True)
        s.add_argument("-o", "--out", default="records")
        s.add_argument("--dois", nargs="*")
        s.add_argument("--dois-file")
        s.add_argument("--known-csv")
        s.add_argument("--min-blocks", type=int, default=2)
        s.add_argument("--cap", type=int, default=0,
                       help="只抓前 N 条（试跑用）。加了 cap 的结果不得用来算 PRISMA 数字")
        s.add_argument("--force", action="store_true")
    e = sub.add_parser("epmc")
    e.add_argument("-q", "--query", required=True)
    e.add_argument("-o", "--out", default="epmc")
    e.add_argument("--force", action="store_true")
    rk = sub.add_parser("rank", help="records.csv → 按相关性排序的筛选台账 + 截断出候选集")
    rk.add_argument("-i", "--inputs", nargs="+", required=True)
    rk.add_argument("-o", "--out", default="筛选决定.csv")
    rk.add_argument("-c", "--config", help="给了才能按词权排序（**强烈建议给**，不给相关性会差很多）")
    rk.add_argument("--shortlist", type=int, default=None,
                    help="截断线：前 N 条进入摘要筛选，其余标 not-screened-lowrank（默认 %d，0=不截断）"
                         % SHORTLIST)
    rk.add_argument("--overwrite", action="store_true", help="覆盖已有判定的台账（危险，先备份）")
    ex = sub.add_parser("expand", help="扩截断线：把 seq ≤ N 的 lowrank 记录放回待筛（include 不足时用）")
    ex.add_argument("-b", "--base", required=True)
    ex.add_argument("-n", type=int, required=True, help="新的截断线，如 600")
    mg = sub.add_parser("merge", help="合并分片筛选结果 + 收敛检查 + 报续跑位置")
    mg.add_argument("-b", "--base", required=True)
    mg.add_argument("-p", "--parts", nargs="+", required=True)
    mg.add_argument("--no-archive", action="store_true", help="合并后不把分片移进 _parts/")
    ad = sub.add_parser("add", help="手工补充文献进台账（书 / 书章 / 库外经典），found_via=manual")
    ad.add_argument("-b", "--base", required=True)
    ad.add_argument("--dois", nargs="*", help="有 DOI 的走 OpenAlex 取题录")
    ad.add_argument("--csv", help="手工题录 CSV，至少含 title 列（可含 doi/year/journal/publisher/oa_url）")
    ad.add_argument("--reason", help="补充理由，写进 found_via，如「Torraco 概念奠基专著」")
    args = ap.parse_args()

    if not MAILTO and args.cmd in ("probe", "recall", "fetch", "cite", "epmc", "add"):
        sys.stderr.write("[oa_search] 提示：未设 OPENALEX_MAILTO，未进礼貌池，量大时可能限流。\n")
    if args.cmd == "epmc":
        cmd_epmc(args)
        return
    if args.cmd == "rank":
        cmd_rank(args)
        return
    if args.cmd == "expand":
        cmd_expand(args)
        return
    if args.cmd == "merge":
        cmd_merge(args)
        return
    if args.cmd == "add":
        cmd_add(args)
        return
    cfg = load_cfg(args.config)
    {"probe": cmd_probe, "recall": cmd_recall, "fetch": cmd_fetch, "cite": cmd_cite}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
