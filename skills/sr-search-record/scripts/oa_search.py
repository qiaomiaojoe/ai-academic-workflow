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

def _get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = "HTTP %s %s" % (e.code, e.reason)
            if e.code in (429, 500, 502, 503):
                time.sleep(2 * (i + 1))
                continue
            break
        except Exception as e:  # noqa: BLE001
            last = str(e)
            time.sleep(1.5 * (i + 1))
    die("请求失败：%s\n  URL: %s" % (last, url))


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


# 三型档位：检索内核共用，终止规则与规模预期按型切换
PROFILES = {
    "systematic": {
        "label": "系统综述（PRISMA）", "goal": "穷尽识别全部合格研究",
        "ok": (30, 3000), "warn": 20000,
        "over": "偏大但可执行：继续，记一条协议偏离。**不得为压数字而收窄纳入标准或删种子**",
        "far": "过宽，必须收紧最泛的块或加限制器",
        "stop": "种子召回 100% + 命中落区间 + 本轮无改动",
    },
    "semi-systematic": {
        "label": "半系统 / 叙事综述（RAMESES）", "goal": "覆盖主要研究传统 / 主题，不追求穷尽",
        "ok": (30, 3000), "warn": 50000,
        "over": "对半系统综述是正常的——**不要为了压数字收紧检索式**；改为启用分层抽样筛选，"
                "并把配额规则（按年份 / 学科 / 传统）写进检索记录",
        "far": "过宽，建议收紧最泛的块，或缩小时间窗并说明理由",
        "stop": "传统 / 主题饱和（连续若干批无新主题，且各传统都有代表）",
    },
    "integrative": {
        "label": "整合式综述（Torraco）", "goal": "覆盖构成概念论证所需的文献，有目的抽样合法",
        "ok": (20, 1000), "warn": 20000,
        "over": "整合式综述用**有目的抽样**：不必全筛，但必须写明选择标准与理由（否则批判性整合站不住）",
        "far": "过宽，收紧概念块——整合式综述的语料应当是精选的",
        "stop": "概念覆盖（概念矩阵每格都有文献）+ 选择理由写清",
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

    rows = []
    for i, b in enumerate(blocks):
        rows.append((b.get("name", "块%d" % (i + 1)),
                     "单块：" + " OR ".join(b["terms"]), count_of([bf[i]])))
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
    if final == 0:
        print("!! 命中 0：概念块过窄或术语拼写有误，必须改式子重跑。")
    elif final < lo:
        print("!! 命中 <%d：偏窄，建议给命中最少的块补同义词。" % lo)
    elif final > pf["warn"]:
        print("!! 命中 >%s：%s" % (format(pf["warn"], ","), pf["far"]))
    elif final > hi:
        print("命中 %s（超出 %d–%d）：%s" % (format(final, ","), lo, hi, pf["over"]))
    else:
        print("命中数落在本型的可筛区间（%d–%d）。" % (lo, hi))
    print("终止规则（本型）：%s" % pf["stop"])
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
               "found_via", "oa_url", "pass1", "ai_decision", "ai_reason",
               "pdf_status", "ft_decision", "ft_reason",
               "reviewer_1", "reviewer_2", "final_decision", "note"]
# AI 可写：题摘筛选 + 全文获取状态 + 全文筛选建议
DECISION_COLS = ["pass1", "ai_decision", "ai_reason", "pdf_status", "ft_decision", "ft_reason"]
# 只能人填
HUMAN_COLS = ["reviewer_1", "reviewer_2", "final_decision", "note"]


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_screen(rows, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCREEN_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def cmd_rank(args):
    """把 records.csv（可多份）排成筛选台账骨架：相关度高的在前。

    **只排序，不排除**——PRISMA 要求每一条记录都要过筛。排序的意义是：
    中途停下时已筛的是最可能相关的那批，而不是一个按抓取顺序切出来的有偏前缀。
    """
    if os.path.exists(args.out) and not args.overwrite:
        try:
            old_rows = read_csv(args.out)
        except Exception:  # noqa: BLE001
            old_rows = []
        done = sum(1 for r in old_rows if r.get("ai_decision"))
        ext = sum(1 for r in old_rows if (r.get("found_via") or "").startswith("external:"))
        if done:
            die("台账 %s 已存在且已有 %d 条判定——重跑 rank 会把它们清空。\n"
                "  续跑筛选：直接从第一条 ai_decision 为空的记录接着筛，不要重跑 rank。\n"
                "  确实要重建：加 --overwrite（先备份）。" % (args.out, done))
        if ext:
            die("台账 %s 里有 %d 条外部检索导入的记录（found_via=external:*）——"
                "它们不在 records.csv 里，重跑 rank 会把它们**永久丢掉**。\n"
                "  正常做法：先 rank 建台账，再 import 导入外部记录。\n"
                "  确实要重建：加 --overwrite（先备份台账），重建后重新 import 一次。" % (args.out, ext))
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

    def title_hits(r):
        """题名里命中了几个概念块——比摘要命中强得多的相关性信号。"""
        t = (r.get("title") or "").lower()
        return sum(1 for b in blocks if any(clean_term(x).lower() in t for x in b["terms"]))

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
        return (title_hits(r), nb, ab, cb)

    rows.sort(key=score, reverse=True)
    out = []
    for i, r in enumerate(rows, 1):
        o = {c: "" for c in SCREEN_COLS}
        o.update({k: r.get(k, "") for k in
                  ("uid", "doi", "title", "year", "journal", "has_abstract", "n_blocks_hit",
                   "found_via", "oa_url")})
        o["seq"] = i
        out.append(o)
    write_screen(out, args.out)
    dist = collections.Counter((r["n_blocks_hit"], r["has_abstract"]) for r in out)
    print("已写出筛选台账骨架 %d 条 → %s（决定列全空，等待筛选）" % (len(out), args.out))
    print("排序键：题名命中块数 → 摘要命中块数 → 有无摘要 → 被引数（**只排序不排除，全部记录都要筛完**）")
    for k in sorted(dist, reverse=True)[:8]:
        print("  块数=%s 摘要=%s : %d 条" % (k[0] or "?", k[1] or "?", dist[k]))
    return out


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


# ---------------------------------------------------------------- import（外部检索源）

def _ris_like(text, tagmap, tag_re):
    """解析 RIS / Refer(EndNote) / RefWorks 这类「每行一个标签」的题录格式。"""
    recs, cur = [], {}
    for raw in text.splitlines():
        line = raw.rstrip("\n\r")
        m = tag_re.match(line)
        if not m:
            if cur and line.strip() and cur.get("_last"):      # 续行接到上一字段
                cur[cur["_last"]] = (cur.get(cur["_last"], "") + " " + line.strip()).strip()
            continue
        tag, val = m.group(1).strip(), (m.group(2) or "").strip()
        key = tagmap.get(tag)
        if tag in ("TY", "%0", "RT") and cur:                  # 新记录开始
            recs.append(cur); cur = {}
        if key:
            if key == "authors":
                cur[key] = (cur.get(key, "") + "; " + val).strip("; ")
            elif key in cur and key == "abstract":
                cur[key] = cur[key] + " " + val
            else:
                cur.setdefault(key, val)
            cur["_last"] = key
        elif tag in ("ER",):
            if cur:
                recs.append(cur); cur = {}
    if cur:
        recs.append(cur)
    return [{k: v for k, v in r.items() if k != "_last"} for r in recs]


RIS_MAP = {"TI": "title", "T1": "title", "AB": "abstract", "N2": "abstract", "AU": "authors",
           "PY": "year", "Y1": "year", "DA": "year", "JO": "journal", "JF": "journal",
           "T2": "journal", "DO": "doi", "UR": "oa_url"}
REFER_MAP = {"%T": "title", "%X": "abstract", "%A": "authors", "%D": "year",
             "%J": "journal", "%R": "doi", "%U": "oa_url"}
REFWORKS_MAP = {"T1": "title", "AB": "abstract", "A1": "authors", "YR": "year",
                "JF": "journal", "DO": "doi", "LK": "oa_url"}


def parse_records(path):
    """按内容自动识别格式，解析成 dict 列表。支持 RIS / EndNote(Refer) / RefWorks / BibTeX / CSV。"""
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        text = f.read()
    head = text[:4000]
    if path.lower().endswith(".csv") or (head.count(",") > 5 and re.match(r"^[^\n]*title[^\n]*\n", head, re.I)):
        rows = read_csv(path)
        norm = []
        for r in rows:
            low = {(k or "").strip().lower(): (v or "") for k, v in r.items()}
            norm.append({"title": low.get("title") or low.get("题名") or low.get("篇名") or "",
                         "doi": low.get("doi") or low.get("DOI".lower()) or "",
                         "year": low.get("year") or low.get("年") or low.get("发表时间") or "",
                         "journal": low.get("journal") or low.get("source") or low.get("来源") or low.get("期刊") or "",
                         "abstract": low.get("abstract") or low.get("摘要") or "",
                         "authors": low.get("authors") or low.get("author") or low.get("作者") or "",
                         "oa_url": low.get("url") or low.get("oa_url") or ""})
        return norm, "CSV"
    if re.search(r"^\s*@\w+\s*\{", head, re.M):
        recs = []
        for blk in re.findall(r"@\w+\s*\{(.*?)\n\}", text, re.S):
            d = {}
            for k, v in re.findall(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", blk + "\n", re.S):
                k = k.lower().strip()
                v = re.sub(r"\s+", " ", v).strip().strip("{}")
                if k == "title": d["title"] = v
                elif k in ("journal", "booktitle"): d["journal"] = v
                elif k == "year": d["year"] = v
                elif k == "doi": d["doi"] = v
                elif k == "abstract": d["abstract"] = v
                elif k == "author": d["authors"] = v
                elif k == "url": d["oa_url"] = v
            if d.get("title"):
                recs.append(d)
        return recs, "BibTeX"
    if re.search(r"^%0\s", head, re.M) or re.search(r"^%T\s", head, re.M):
        return _ris_like(text, REFER_MAP, re.compile(r"^(%[0A-Za-z])\s+(.*)$")), "EndNote/Refer（CNKI 常见）"
    if re.search(r"^RT\s", head, re.M) or re.search(r"^A1\s", head, re.M):
        return _ris_like(text, REFWORKS_MAP, re.compile(r"^([A-Z][A-Z0-9])\s+(.*)$")), "RefWorks（CNKI 常见）"
    if re.search(r"^TY\s+-\s", head, re.M) or re.search(r"^T1\s+-\s", head, re.M):
        return _ris_like(text, RIS_MAP, re.compile(r"^([A-Z][A-Z0-9])\s+-\s?(.*)$")), "RIS"
    die("认不出 %s 的题录格式。支持 RIS / EndNote(Refer, %%0 %%T) / RefWorks(RT A1 T1) / BibTeX / CSV；"
        "CNKI 请导出为 RefWorks 或 EndNote 格式，WoS / Scopus 导出 RIS 或 BibTeX。" % path)


def cmd_import(args):
    """把**外部数据库人工检索**导出的题录导入台账（CNKI / WoS / Scopus / PubMed / 手工清单均可）。

    OpenAlex 覆盖不到的库（中文核心刊、商业库独有条目、灰色文献）走这个口子进来，
    与自动检索的记录**同台账、同标准、同一套筛选流程**，但 found_via 标成 external:<源>，
    PRISMA 里按源单列——这样"多库检索"是如实的，不是假装 OpenAlex 搜到的。
    """
    base = read_csv(args.base)
    seen = {norm_doi(r.get("doi")) for r in base if norm_doi(r.get("doi"))}
    seen |= {norm_title(r.get("title")) for r in base if norm_title(r.get("title"))}
    try:
        nxt = max(int(r.get("seq") or 0) for r in base) + 1
    except ValueError:
        nxt = len(base) + 1

    parsed, fmts, added, dups, no_title = [], [], [], 0, 0
    for path in args.file:
        recs, fmt = parse_records(path)
        fmts.append("%s（%s，%d 条）" % (os.path.basename(path), fmt, len(recs)))
        parsed.extend(recs)

    for r in parsed:
        title = (r.get("title") or "").strip()
        if not title:
            no_title += 1
            continue
        doi = norm_doi(r.get("doi"))
        k = doi or norm_title(title)
        if k in seen:                       # 与台账已有记录、或本批内部重复
            dups += 1
            continue
        seen.add(k)
        ym = re.search(r"(19|20)\d{2}", str(r.get("year") or ""))
        o = {c: "" for c in SCREEN_COLS}
        o.update({"seq": nxt, "uid": doi or norm_title(title)[:60], "doi": doi, "title": title,
                  "year": ym.group(0) if ym else "",
                  "journal": (r.get("journal") or "").strip(),
                  "has_abstract": "Y" if (r.get("abstract") or "").strip() else "N",
                  "n_blocks_hit": "", "oa_url": (r.get("oa_url") or "").strip(),
                  "found_via": "external:%s" % args.source})
        nxt += 1
        added.append(o)

    print("解析：%s" % "；".join(fmts))
    print("共解析 %d 条 | 无题名跳过 %d | 重复去掉 %d（与台账已有记录 或 本批内部重复）| **新增 %d**"
          % (len(parsed), no_title, dups, len(added)))
    if args.dry_run:
        print("（--dry-run：没有写盘。）")
        for r in added[:10]:
            print("  + %s %s" % (r.get("year") or "____", (r.get("title") or "")[:70]))
        return base

    if added:
        write_screen(base + added, args.base)
        print("已写入 %s（seq 从 %d 起，found_via=external:%s）" % (args.base, added[0]["seq"], args.source))
    else:
        print("没有新增，台账未改动。")

    # —— 信息源登记（PRISMA 要按源报数）——
    reg_path = args.reg or os.path.join(os.path.dirname(os.path.abspath(args.base)) or ".", "外部检索源.json")
    reg = []
    if os.path.exists(reg_path):
        try:
            with open(reg_path, encoding="utf-8") as f:
                reg = json.load(f)
        except Exception:
            reg = []
    reg.append({"source": args.source, "query": args.query,
                "date": args.date or time.strftime("%Y-%m-%d"),
                "reported_hits": args.hits if args.hits is not None else None,
                "files": [os.path.basename(x) for x in args.file],
                "parsed": len(parsed), "duplicates_removed": dups,
                "imported": len(added)})
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    print("信息源已登记 → %s（第 %d 条）" % (reg_path, len(reg)))
    if args.hits is None:
        print("!! 没给 --hits：该库页面显示的命中总数缺失，PRISMA 的 Identification 会缺一个数。"
              "回去把命中数抄下来补一条登记（同样的 --source/--query 再跑一次 --dry-run 不写台账，"
              "或直接手工补进 %s）。" % os.path.basename(reg_path))
    elif args.hits > len(parsed):
        print("!! 该库命中 %d 条，但只导出/解析了 %d 条——差额要在方法节说明（导出上限？只取前 N 页？）。"
              % (args.hits, len(parsed)))
    # —— 完整度体检：字段大面积缺失通常意味着导出格式 / 字段选错了 ——
    if added:
        miss = {k: sum(1 for r in added if not (r.get(k) or "").strip())
                for k in ("journal", "year", "doi")}
        bad = {k: v for k, v in miss.items() if v > 0.3 * len(added)}
        if bad:
            print("!! 导入记录的字段大面积缺失：%s（共 %d 条）。"
                  % ("、".join("%s 缺 %d" % (k, v) for k, v in bad.items()), len(added)))
            print("   多半是导出时字段没选全或格式选错了——回去用带完整题录的格式重导（CNKI 选 RefWorks / "
                  "EndNote，WoS / Scopus 选 RIS / BibTeX），否则筛选与特征表都会缺料。"
                  "已导入的记录不会被后续导入覆盖，要修正得先删掉这批再重导。")

    print("这些记录 **ai_decision 为空**，要和数据库检索的记录走同一套标准筛完；"
          "**PRISMA 按 found_via 分源报数，不得把 external:* 混进 OpenAlex 的命中数。**")
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

    done = [r for r in base if r.get("ai_decision")]
    todo = [r for r in base if not r.get("ai_decision")]
    dist = collections.Counter(r["ai_decision"] for r in done)
    print("\n① 题摘筛选：%d / %d（%.1f%%）  合并了 %d 份分片、%d 条判定"
          % (len(done), len(base), 100.0 * len(done) / max(len(base), 1), len(parts), applied))
    for k in ("include", "exclude", "unclear"):
        print("   %-8s %d" % (k, dist.get(k, 0)))
    if todo:
        nxt = todo[0]
        print("   **未筛 %d 条。续跑从 seq=%s 起**（uid=%s）。" % (len(todo), nxt.get("seq"), nxt.get("uid")))
        return base
    print("   **题摘全部筛完。**")

    # 进入全文阶段的候选 = include + unclear（unclear 一律保留到全文判定）
    ft_pool = [r for r in base if r.get("ai_decision") in ("include", "unclear")]
    ft_done = [r for r in ft_pool if r.get("ft_decision")]
    ft_dist = collections.Counter(r["ft_decision"] for r in ft_done)
    pdf_dist = collections.Counter(r.get("pdf_status", "") for r in ft_pool if r.get("pdf_status"))
    print("\n② 全文阶段：候选 %d 条（include %d + unclear %d）"
          % (len(ft_pool), dist.get("include", 0), dist.get("unclear", 0)))
    if pdf_dist:
        print("   全文获取：" + "、".join("%s %d" % (k, v) for k, v in pdf_dist.most_common()))
    print("   全文筛选：%d / %d" % (len(ft_done), len(ft_pool)))
    for k in ("include", "exclude", "unclear"):
        if ft_dist.get(k):
            print("     %-8s %d" % (k, ft_dist[k]))
    ft_todo = [r for r in ft_pool if not r.get("ft_decision")]
    if ft_todo:
        print("   **待全文判定 %d 条。续跑从 seq=%s 起**（uid=%s）。"
              % (len(ft_todo), ft_todo[0].get("seq"), ft_todo[0].get("uid")))
    else:
        print("   **全文筛选也已完成。** PRISMA 的全文评估 / 全文排除 / 最终纳入数可以对账出表了。")
    print("\n注意：ft_decision 仍是 AI 建议；final_decision 由人填（本脚本拒绝 AI 写入）。")
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
    im = sub.add_parser("import", help="外部数据库人工检索的导出题录 → 台账（CNKI / WoS / Scopus / 手工清单）")
    im.add_argument("-b", "--base", required=True, help="筛选台账 csv")
    im.add_argument("-f", "--file", nargs="+", required=True, help="导出的题录文件，可多个（RIS / EndNote / RefWorks / BibTeX / CSV，自动识别）")
    im.add_argument("--source", required=True, help="信息源名，如 CNKI / Web of Science / Scopus")
    im.add_argument("--query", required=True, help="在该库实际用的检索式（原样抄，写进方法节）")
    im.add_argument("--date", help="检索日期，默认今天")
    im.add_argument("--hits", type=int, help="该库页面显示的命中总数（PRISMA 的 Identification 要用）")
    im.add_argument("--reg", help="信息源登记文件，默认台账同目录 外部检索源.json")
    im.add_argument("--dry-run", action="store_true", help="只解析不写盘")

    e = sub.add_parser("epmc")
    e.add_argument("-q", "--query", required=True)
    e.add_argument("-o", "--out", default="epmc")
    e.add_argument("--force", action="store_true")
    rk = sub.add_parser("rank", help="records.csv → 排好序的筛选台账骨架（只排序不排除）")
    rk.add_argument("-i", "--inputs", nargs="+", required=True)
    rk.add_argument("-o", "--out", default="筛选决定.csv")
    rk.add_argument("-c", "--config", help="给了就按题名命中概念块数优先排序（强烈建议给）")
    rk.add_argument("--overwrite", action="store_true", help="覆盖已有判定的台账（危险，先备份）")
    mg = sub.add_parser("merge", help="合并分片筛选结果 + 报进度与续跑位置")
    mg.add_argument("-b", "--base", required=True)
    mg.add_argument("-p", "--parts", nargs="+", required=True)
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
    if args.cmd == "merge":
        cmd_merge(args)
        return
    if args.cmd == "add":
        cmd_add(args)
        return
    if args.cmd == "import":
        cmd_import(args)
        return
    cfg = load_cfg(args.config)
    {"probe": cmd_probe, "recall": cmd_recall, "fetch": cmd_fetch, "cite": cmd_cite}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
