---
name: sr-search-record
description: 综述文章的检索与筛选记录（乔淼PhD · AI学术训练营 · AI学术工作流 · 综述文章工作台 阶段②）。**Snyder 三型通用**——系统 / 半系统·叙事 / 整合式共用一套检索内核，按 选题.md 锚块的 review_type 切换终止规则与产出档位。AI 全自动跑完文献检索：概念块拆解 → 检索式多轮自动校准（种子文献召回 100% 才收敛）→ 全量抓取去重 → 题摘筛选建议 → 引文追踪补漏 → 全文获取与全文筛选（PDF 落盘 + Zotero 入库，调 lit-pdf-zotero 但不建金字塔）→ 产出论文可直接贴的三张表（检索记录表 S1–Sn 带命中数 / 纳入排除标准表 / PRISMA 流程四个数字）+ 待人工复核清单。检索引擎用 OpenAlex 开放 API（免登录免密钥，随 skill 附 scripts/oa_search.py），医学题目补 Europe PMC（MeSH）。AI 只出筛选建议不当第二评审。Trigger on："跑系统综述的文献检索"、"半系统 / 叙事综述建语料库"、"整合式综述选文献"、"自动检索并筛选文献"、"生成检索记录表和 PRISMA 数字"、"systematic review search"、"build the corpus for my narrative / integrative review"、"run the search and screening for my review"。
---

# SR Search Record · 综述文章的检索与筛选记录

把综述文章的检索环节做成**可复现、数字能对账**的流水线。**Snyder 三型共用这一套**（历史原因名字里带 sr，不只服务 systematic review）。AI 干 80%（设计检索式、多轮校准、全量抓取、去重、题摘筛选建议、记账出表），剩下 20%（最终纳入判断、边界裁决、学科术语补漏）交给人。

**产出不是"搜到的一堆文献"，是论文方法节能直接贴的三张表。**

## 调用约定（独立运行）

- **定型（第一件事）**：读 `01_选题/选题.md` 机器锚块的 `review_type`（systematic / semi-systematic / integrative），写进 `检索配置.json` 的 `review_type` 字段——**它决定可筛区间、超限处置与终止规则**，脚本按它切档。锚块缺失就问用户，不要默认 systematic。
- **输入**：优先读 `01_选题/选题.md`（综述规格、RQ、纳入排除标准、近邻综述）。**有这个文件就直接开跑，不要回头确认概念块**；只有在没有该文件、纳入标准只能从口述推断时，才在拆完概念块后确认一次。
- **输出**：默认落当前工作目录 `系统综述/` 下；调用方给了路径以调用方为准。
- **检索引擎**：本 skill 目录下的 `scripts/oa_search.py`（OpenAlex 开放 API + Europe PMC）。**必须调用这个脚本，不要临时自己写检索代码**——脚本保证每次的检索记录格式一致、命中数可复跑。运行前设 `export OPENALEX_MAILTO=<用户邮箱>` 进礼貌池。
- **质量标准**：对齐已发表 SLR 的主流做法（2 个以上信息源 + 概念块布尔式 + 限制器 + 题摘/全文两轮筛选 + 纳入文献参考文献回溯）。不追求 Cochrane 级的双人独立筛选与 MeSH 逐行检索——那两条必须由人完成，本 skill 只做到可交接。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。

## 三型档位（内核共用，规则按型切）

| | systematic | semi-systematic | integrative |
|---|---|---|---|
| 报告规范 | PRISMA | RAMESES | Torraco (2005) |
| 检索目标 | 穷尽识别全部合格研究 | 覆盖主要研究传统 / 主题，**不追求穷尽** | 覆盖构成概念论证所需的文献，**有目的抽样合法** |
| 可筛区间 | 30–3000（>20000 必须收紧） | 30–3000（>50000 才算过宽） | 20–1000（>20000 才算过宽） |
| 超限处置 | 继续 + 记协议偏离 | **启用分层抽样**，配额规则写进检索记录；不为压数字收紧式子 | 有目的抽样，**写明选择标准与理由** |
| 终止规则 | 种子 100% 召回 + 命中落区间 + 本轮无改动 | **传统 / 主题饱和**：连续若干批无新主题，且各传统都有代表 | **概念覆盖**：概念矩阵每格都有文献 |
| 筛选强度 | 全量过筛，题摘 + 全文两轮 | 全量抓；可按配额抽样筛，抽样规则入档 | 小语料，逐篇论证式选择 |
| 出表（第 7 步） | PRISMA 流程图 + 三张表 | 检索记录表 + 选择流程说明 + **传统 / 主题覆盖表** | 检索记录表 + **语料构成说明** + 概念覆盖矩阵 |

**不要把 systematic 的「穷尽」硬约束套到另外两型**——强推穷尽到整合式综述是方法学错误（Torraco 的选文由概念论证驱动）。反过来也不行：systematic 不许用"抽样"绕过全量筛选。

## 全局硬约束（任何步骤都不得违反）

1. **不编造文献。** 所有条目必须来自脚本实际返回的记录，带 DOI 或 OpenAlex ID。不得凭印象补充"应该还有一篇…"。
2. **AI 不是第二评审。** 筛选表里 AI 的判断写在 `ai_decision` 列，`reviewer_1` / `reviewer_2` 列一律留空给人填。**不得声称完成了双人独立筛选。**
3. **unclear 一律保留。** 摘要缺失、信息不足、边界模糊的记录标 `unclear` 进入人工复核，**不得为了缩短清单自动排除**。
4. **数字必须对账。** PRISMA 每个数字都要能从 records.csv / 筛选决定.csv 反算出来；对不上就报错，不许四舍五入或估算。
5. **检索源如实报告。** 方法节必须写明"检索源为 OpenAlex（+ 补充源）"，不得表述成 Scopus / Web of Science 检索。局限节要写明未使用受控词表与商业库。
6. **不因为跑不动就改纳入标准。** 命中过多要收紧的是检索式（加概念块 / 收窄泛词），不是偷偷提高纳入门槛。任何标准改动写进"协议偏离"记录。
   （semi-systematic / integrative 允许**抽样**，但抽样 ≠ 改标准：**抽样规则与理由必须写进检索记录**，且不得事后按结果调整。）
7. **规模不达标不是失败。** 命中落在本型区间之外时按上表处置——降级、抽样、记偏离都是合法出路，**硬凑一个漂亮数字才是错**。
8. **不中途讨许可。** 本 skill 的每一步都设计成一口气跑完。**除了下面明确写出的三类停点，不得停下来征求"要不要继续"**——尤其不得逐批汇报筛选进度。三类合法停点：① 守卫触发（权威输入缺失 / 数字对不上 / 命中超过本型的过宽阈值）；② 上下文预算将尽（必须先写盘并报出续跑位置再停）；③ 一步跑完后的收尾汇报。**"数量大、要花时间"不是停点**——写盘续跑，别问。

## 步骤

### 第 1 步 · 拆概念块，出配置

读 `选题.md`（或用户口述）→ 把研究问题拆成 **2–4 个概念块**（PICO / PECO / SPIDER / 自定义均可，教育与管理类常用简化的 PIO）。

- 每块列全同义词：全称与缩写、英美拼写、旧称、近义表达。**块内 OR，块间 AND。**
- 不要把 outcome、研究设计、过窄情境塞进检索式，除非纳入标准明确要求——那会牺牲召回。
- 限制器（年份 / 语言 / 文献类型）只在纳入标准有学术理由时才加，理由要写下来。

写成配置文件 `系统综述/检索配置.json`：

```json
{
  "field": "title_and_abstract",
  "blocks": [
    {"name": "AI", "terms": ["artificial intelligence", "machine learning", "ChatGPT"]},
    {"name": "采纳", "terms": ["adoption", "implementation", "usage"]},
    {"name": "中小企业", "terms": ["SME", "small and medium enterprises"]}
  ],
  "filters": {"publication_year": "2015-2026", "type": "article", "language": "en"},
  "sentinels": ["10.xxxx/yyyy"],
  "review_type": "systematic"
}
```

**种子文献（sentinels）不问用户要**，按序自动获得：① `选题.md` 里的近邻综述 / 关键文献的 DOI；② 不够 3 篇时，用最宽的一两个块跑一次 `probe`+`fetch --cap 40`，按被引数排序，AI 从题摘里挑出明显合格的 3–5 篇当种子。用户主动给了就优先用用户给的。

### 第 2 步 · 检索式自动校准（循环，AI 自己跑，不问用户）

每轮执行：

```bash
python3 <skill>/scripts/oa_search.py probe  -c 系统综述/检索配置.json
python3 <skill>/scripts/oa_search.py recall -c 系统综述/检索配置.json
```

看两个指标改式子：

- **种子召回 < 100%** → `recall` 会指出是哪个块（或哪个限制器）把它挡掉了。给那个块补同义词；若是限制器挡的，判断该限制器是否真有学术理由，没有就删掉。
- **命中数**：按上面「三型档位」表的可筛区间与超限处置判断——`probe` 会直接按 `review_type` 打印本型的区间、处置建议与终止规则，照它执行。<30（integrative <20）一律是偏窄，给命中最少的块补同义词。

**收敛条件（三条同时满足，可机器判定）**：种子召回 100% && 命中落在本型可筛区间 && 本轮相对上一轮无改动。

**上限 5 轮。** 5 轮仍不收敛时按命中数分流，**不要停下来让用户在方案之间选**：

- 命中 ≤ 本型的过宽阈值 → **自动接受当前检索式继续往下跑**（第 3 步），把"未收敛 + 原因 + 每轮迭代史"写进检索记录的协议偏离节；semi-systematic 同时定下抽样配额规则，integrative 同时写明选择标准。收尾汇报时一并告知用户。
- 命中 > 过宽阈值 → 停下，列出每轮检索式、命中数、未召回种子与诊断，说明卡在哪。

**种子召回不了且诊断为不可修复时**（概念只出现在全文、题摘完全不提），记录该事实并继续，**不要删掉这个种子**，也不要为它无限加词。

每轮都追加记录到 `系统综述/检索记录.md`，保留全部历史版本（这就是"检索式如何迭代"的证据）。

### 第 3 步 · 全量抓取

```bash
python3 <skill>/scripts/oa_search.py fetch -c 系统综述/检索配置.json -o 系统综述/records
```

得到 `records.csv` / `.jsonl`（含 DOI、题名、年份、期刊、作者、被引数、摘要、命中了哪几个块）。记下三个数：**原始命中数、去重后待筛数、摘要覆盖率**。

学科对口时补跑一个信息源，让"信息源 ≥2"成立：

- 医学 / 健康 / 护理：Europe PMC（支持 MeSH）
  `oa_search.py epmc -q '(MESH:"Artificial Intelligence") AND (MESH:"Education, Nursing")' -o 系统综述/epmc`
- 中文文献：`cnki-advanced-search`（skill 可用时）
- 灰色文献 / 政策报告：WebSearch，**单列来源，不与数据库检索混算**

### 第 4 步 · 题摘筛选（连续跑，AI 出建议）

先把纳入 / 排除标准写成**可判定的条目表**（对齐 `选题.md`；每条都要能对一篇摘要回答 yes/no），落 `系统综述/纳入排除标准.md`。

**4.1 建台账（排序，不排除）**

```bash
python3 <skill>/scripts/oa_search.py rank -i 系统综述/records.csv -c 系统综述/检索配置.json \
  -o 系统综述/筛选决定.csv
```

按"题名命中概念块数 → 摘要命中块数 → 有无摘要 → 被引数"排序，输出带 `seq` 的空台账。**只排序不排除——PRISMA 要求每条记录都要过筛，一条都不能少。**排序的作用是：万一中途停下，已筛的是最可能相关的那批，而不是按抓取顺序切出的有偏前缀。

**台账已存在且已有判定时不要跑 `rank`**（会清空判定，脚本本身也会拒绝执行）——那是续跑，直接跳到 4.2 从第一条空判定接着筛。

**4.2 连续筛（关键：分批是内部颗粒度，不是汇报节奏）**

按 `seq` 顺序，每次在脑子里处理约 40 条（判得准的颗粒度），逐条给：

`ai_decision` ∈ {include, exclude, unclear} + `ai_reason`（排除必须对应标准表里的某一条，**每篇只记一个首要排除理由**）

- 无摘要（`has_abstract=N`）→ 一律 `unclear`，不得据题名排除。
- 判不准 → `unclear`。宁可多留。
- 量大时可以先过一遍题名（只排明显的人群/场景不符，绝不用需要读摘要才能判的标准），再对推进的读摘要；两遍**连着跑完，中间不汇报**。用 `pass1` 列记进度（`exclude` / `advance` / `pass2-done` / `locked-noabs`）。

**每处理完一批，写一个分片文件** `系统综述/筛选决定-partNNN.csv`（列只需 `uid, pass1, ai_decision, ai_reason`），**然后立刻继续下一批——不要停下来汇报，不要问"要不要继续"**（硬约束 7）。分片写盘是为了随时可续跑，不是交互点。

**4.2b 抽样（仅 semi-systematic / integrative，systematic 不适用）**

命中远超可筛区间时，这两型可以**抽样筛**而不是全量筛——但必须：① 抽样规则**事先**写进 `检索记录.md`（如"每年 × 每学科取被引前 N"、"每个研究传统至少 M 篇"）；② 用 `rank` 的排序做分层依据，**不得随手挑**；③ 未筛部分在台账里保留、`pass1` 标 `not-sampled`，**不算排除**；④ 产出里如实写明"本综述采用抽样筛选，未穷尽"。
**事后按结果调整抽样规则 = 改标准，不允许。**

**4.2c 手工补充（书 / 书章 / 库外经典）**

OpenAlex 对专著与书章的覆盖弱于期刊论文，整合式综述尤其容易漏掉最重要的一批：

```bash
python3 <skill>/scripts/oa_search.py add -b 系统综述/筛选决定.csv \
  --dois 10.xxxx/yyy --csv 手工题录.csv --reason "概念奠基专著"
```

补进来的记录 `found_via = manual:<理由>`，走同样的筛选流程，**PRISMA / 选择流程说明里单列为「其他方法识别的记录」，不得混进数据库检索命中数**。

**4.3 合并 + 报进度**

```bash
python3 <skill>/scripts/oa_search.py merge -b 系统综述/筛选决定.csv -p 系统综述/筛选决定-part*.csv
```

`merge` 会把判定写回台账、拒绝 AI 填写人工列、并报出"已筛 X/N + 续跑从 seq=? 起"。

**跑不完怎么办**：上下文预算将尽时，先跑 4.3 写盘，再停，并在汇报里写清 `已筛 X / N，续跑从 seq=Y 起`。下次收到"续跑筛选"时，从台账第一条 `ai_decision` 为空的记录接着跑，**不重筛已判定的**。

台账列固定为：
`seq, uid, doi, title, year, journal, has_abstract, n_blocks_hit, found_via, oa_url, pass1, ai_decision, ai_reason, pdf_status, ft_decision, ft_reason, reviewer_1, reviewer_2, final_decision, note`

AI 可写 `pass1 / ai_decision / ai_reason`（本步）与 `pdf_status / ft_decision / ft_reason`（第 6 步）；
最后四列 `reviewer_1 / reviewer_2 / final_decision / note` **永远留空**给人填，`merge` 会拒绝 AI 写入。

### 第 5 步 · 引文追踪补漏（一轮，自动）

**前提：第 4 步已全部筛完**（`merge` 报「全部筛完」）。**没筛完就先把第 4 步跑完，不要提前做引文追踪**——用一个不完整的 include 集去追踪，追出来的补漏集也是偏的。

对第 4 步 `include` 的记录做双向追踪（对齐已发表 SLR 的"翻纳入文献参考文献"这一步）：

```bash
python3 <skill>/scripts/oa_search.py cite -c 系统综述/检索配置.json \
  --dois-file 系统综述/included_dois.txt --known-csv 系统综述/records.csv \
  -o 系统综述/补漏 --min-blocks 2
```

补漏集走同样的第 4 步筛选（`rank -i 系统综述/补漏.csv` 建一份自己的台账，或与主台账合并后续筛），`found_via` 保留为 `citation:backward` / `citation:forward`，PRISMA 里单列成"其他方法识别的记录"。**只做一轮**，不递归。

### 第 6 步 · 全文获取与全文筛选（PRISMA 的全文评估段）

**前提：第 4 步已全部筛完、第 5 步引文补漏也筛完。** 这一步产生 PRISMA 的「全文评估数 / 全文排除数（按理由）/ 最终纳入数」——**没有这一步，PRISMA 是断的，综述也无法进入综合**。

**6.1 取全文**：对象 = 全部 `ai_decision ∈ {include, unclear}` 的记录（unclear 也要取，它们正是要靠全文才能判的）。

顺序：① 台账 `oa_url` 直接下载（`rank` 已把 OpenAlex 的 OA 链接带进台账；台账该列为空时从 `records.csv` 按 DOI 取）；② 调 `lit-pdf-zotero` 做批量获取与入库，**override 掉它的 PXYV 部分**——见 6.3；③ 仍拿不到的走 `scansci-pdf`（机构 / 多源）；④ 最后仍无全文的标 `pdf_status = not-retrieved`。

PDF 落 `02_文献/pdf_download/`（命名 `AuthorYear.pdf`）。台账写 `pdf_status` ∈ `oa` / `retrieved` / `request-sent` / `not-retrieved`。
**「找不到全文」与「不符合纳入标准」是两件事，分开记**——前者是 PRISMA 里单列的一类，不许混进排除理由。

**6.2 全文筛选**：逐篇按标准表判定，写台账 `ft_decision` ∈ {include, exclude, unclear} + `ft_reason`（排除只记**一个首要理由**）。

- 这一层才判得了「只出现在结果表里」的闸门标准（如是否报告了某种分层结果）——题摘层判不了的都留到这里。
- `pdf_status = not-retrieved` 的 → `ft_decision = unclear`，理由记「全文未获取」，**不得当作排除**。
- 仍判不准 → `unclear`，留给人。
- 分片写 `筛选决定-partFTNNN.csv`（列：`uid, pdf_status, ft_decision, ft_reason`），跑完 `merge`。**同样不逐批汇报**（硬约束 7）。
- `merge` 会分两段报进度：题摘 X/N，全文 Y/M（M = include + unclear）。

**6.3 入 Zotero**：调 `lit-pdf-zotero`，**明确 override**：

- **不建金字塔**——`Classic / Key Texts / Supporting-P/X/Y/V` 是 PXYV 那套，系统综述不用。改按 PRISMA 状态建 Collection：`<项目名>/included`、`/excluded-fulltext`、`/awaiting-fulltext`。
- **不出金字塔分布图，也不出 PXYV 罗盘图**——系统综述不需要这两张，改在第 7 步出 PRISMA 流程图。
- 标签用 `sr-included` / `sr-excluded` / `sr-awaiting` + 项目 slug；`extra` 写 `study_id`、`ft_reason`、`found_via`。
- 其余（多渠道找 PDF、逐条入库、入库报告）照 `lit-pdf-zotero` 原样执行。

最终纳入集**只在这一步之后**才成立，交给 `lit-verify` 做一次 DOI / 题录验真，再进入综合（`review-synthesis`）。

### 第 7 步 · 出表 + 复核清单（产出按型）

**systematic** 出下面 1–4 全套。**semi-systematic**：1、2 照出，3 改为「选择流程说明」（PRISMA-style 流程图可选；必须写清抽样规则与各阶段数量）并**加一张传统 / 主题覆盖表**（每个研究传统各命中几篇）。**integrative**：1、2 照出，3 改为「语料构成说明」（为什么是这些文献、有目的抽样的标准与理由）并**加一张概念覆盖矩阵**（概念 × 文献，标出空格）。

1. **检索记录表** → `系统综述/检索记录.md`
   `| # | 概念块 / 步骤 | 内容 | 命中数 |` 的 S1–Sn 表（`probe` 直接给），加上：检索日期、检索源、完整可复跑检索式、限制器及理由、迭代过程（第 2 步每轮）。
2. **纳入 / 排除标准表** → `系统综述/纳入排除标准.md`
   `| 维度 | 纳入 | 排除 |`，维度如可得性、样本、学科、研究设计、文献类型、语言、年份。
3. **PRISMA 流程数字** → `系统综述/PRISMA流量.md`
   识别（各源命中数）→ 去重删除数 → 待筛数 → 题摘排除数 → 全文评估数（= 第 6 步 `ft_decision` 非空数）→ 全文未获取数（`pdf_status=not-retrieved`，单列，不算排除）→ 全文排除数（按 `ft_reason` 分组）→ 最终纳入数。**每个数字标出从哪张表哪一列反算得来**；对不上就停下报错。
4. **待人工复核清单** → `系统综述/待复核.md`
   只列人真正要看的：全文阶段的 `ft_decision = include` 与 `unclear`（各带 AI 理由与 PDF 状态）——题摘层的 include 已经过了全文这一关，不必重列，加一节「需要你确认的三件事」——① 概念块是否漏了本学科行话；② 是否需要去 Scopus / WoS 复核一次纳入集（投保守期刊时）；③ 边界记录的裁决。

**筛选未跑完时**：三张表照出，但每一份产出的**开头必须放醒目警告**——已筛 X/N（百分比）、剩余 Z 条未筛、题摘排除数与纳入数都是部分值、不得据此绘制 PRISMA 流程图或撰写方法节，并写清续跑位置。**不得把部分结果呈现成最终结果。**

最后给会话内小结：各步数量链、卡住的地方、协议偏离、以及"人接下来要做什么"。

## 与其他 skill 的边界

- 最终纳入集验真 → `lit-verify`（第 6 步之后跑一次）。PDF 获取与 Zotero 入库的**机械动作**由第 6.3 步调 `lit-pdf-zotero` 完成（带 override，不建金字塔）；全文层的**学术判断**在第 6.2 步，属本 skill。
- 下游综合 → `review-synthesis`（三型三方法）。**不要走 `data-analysis-round` / `analyze-quantitative-data`**——那是实证论文的单研究数据分析，不含效应量合成。
- 非系统综述（半系统 / 整合式）的探索性建库 → 走 `literature-search`（PXYV 金字塔），不用本 skill。
- 成文 → `review-draft`（按 PRISMA / RAMESES / Torraco 报告规范）。
