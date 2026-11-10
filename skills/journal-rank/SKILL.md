---
name: journal-rank
description: 查期刊级别（乔淼PhD · AI学术训练营 · AI学术工作流）。输入刊名或 ISSN，查这本英文期刊被哪些库收录（SCIE / SSCI / AHCI / ESCI / EI）、最新影响因子、JCI、JCR 学科和分区、分区（大类学科 + 1–4 区）、年发文量、综述占比、OA 占比、自引率、出版社；一次可以查几本。数据来自 iJournal（投必得学术），不用登录；随 skill 附 scripts/journal-rank.mjs（要 Node.js 18 以上和 Chrome 或 Edge）。中文期刊（北大核心、CSSCI）不在这里查。Trigger on："这本期刊是不是 SSCI"、"查一下这本期刊的影响因子和分区"、"这几本期刊哪个级别高"、"帮我看看投稿目标期刊的 JCR 分区"、"is this journal SSCI-indexed"、"check the impact factor and quartile of these journals"。
---

# 查期刊级别

**必须用本 skill 目录下的 `scripts/journal-rank.mjs`，不要自己写抓网页的代码，也不要凭印象报影响因子或分区**。脚本会自己打开一个单独的浏览器窗口，在 iJournal 的查询页里读结果，回一段 JSON。

```
node <skill>/scripts/journal-rank.mjs lookup "刊名或 ISSN" ["第二本" ...]
node <skill>/scripts/journal-rank.mjs check
```

- 刊名用英文全称或简称都行，大小写、`&` 和 `and` 都不影响。
- **刊名和 ISSN 都有时，写成 `"刊名|ISSN"` 一起传**（`"Stress and Health|1532-2998"`）：先按 ISSN 查，查不到自动改按刊名查，结果里 `note` 会注明。只出电子版的刊（BMC、Frontiers、MDPI 等）按 ISSN 常常一条都查不到，只传 ISSN 会把 SSCI 期刊误报成 `not_found`。
- 只有 ISSN、回了 `not_found` 时，不要当成「没被收录」：先用 `openalex` 查出刊名，再按刊名查一次。
- 一次可以查几本。每查一页要隔 2–4 秒，按 ISSN 查会多查一页（补 JCR 学科和 EI），一小时最多 120 页。
- 浏览器和 `cnki` skill 共用一个窗口（各用各的标签页），不碰用户平时用的浏览器。

## 返回

先看最外层 `status`：

| status | 意思 | 你怎么做 |
|---|---|---|
| `ok` | 至少查到一本 | 逐本看 `items` 里每本的 `status` |
| `not_found` | 一本都没查到 | 看每本的 `candidates`（名字相近的几本），问用户是不是其中一本；**不要拿相近的顶替** |
| `limit` | 这一小时查太多了 | 停下，告诉用户过一会儿再查 |
| `unreachable` | iJournal 打不开 | 让用户检查网络 |
| `layout_changed` | 网站改了，脚本取不到数据 | 告诉用户「iJournal 改版了，journal-rank 要更新」，把 `msg` 原样转给用户 |
| `no_browser` | 没找到 Chrome 或 Edge；或浏览器开不起来（Mac 上 AI 在沙箱里跑时就会这样） | 没装就请用户装 Chrome。开不起来：照 msg 原样告诉用户（在 POPPER 里是到「AI学术环境配置 → 大家共用的 → 检索浏览器」点「打开」），等用户说开好了再重试；**不要自己想办法开浏览器、改端口、杀进程** |
| `error` | 参数错了或其他问题 | 看 `msg` |

每本期刊（`items` 里 `status: ok` 的）有这些字段：

| 字段 | 意思 |
|---|---|
| `title` / `abbr` / `issn` | 刊名、简称、ISSN |
| `databases` | 收录库：`SCI/SCIE`、`SSCI`、`AHCI`、`ESCI`、`EI` |
| `impact_factor` | 最新影响因子（JIF） |
| `jci` | 期刊引文指标（JCI） |
| `jcr` | 每个 JCR 学科一条：`category` 学科、`edition` 属于 SCIE 还是 SSCI、`quartile` 分区 Q1–Q4、`jci_rank` 该学科里的 JCI 排名 |
| `zone` / `zone_subject` | 分区（1–4 区）和它的大类学科。iJournal 列表里把这一列叫「中科院分区」，期刊详情页叫「新锐分区」；告诉用户时写「分区（iJournal：x 区）」，不要自己断定是哪一套 |
| `annual_articles` | 年发文量 |
| `review_ratio_pct` / `oa_ratio_pct` / `self_cite_pct` | 综述占比、OA 文章占比、自引率（百分数） |
| `publisher` / `link` | 出版社、iJournal 上这本刊的页面 |

同名的几本（`note: 同名的有几本`）放在 `matches` 里，按 ISSN 区分，问用户是哪一本。AHCI 期刊没有 JCR 分区，`jcr` 是空的，这是正常的。

## 规矩

- 告诉用户结果时注明来源「iJournal」和查询日期；影响因子每年 6 月更新，用户要以官方 JCR 为准时提醒一句。
- 不改写数字：影响因子、分区照脚本给的报，不四舍五入成别的，不补脚本没给的。
- 中文期刊（北大核心、CSSCI、CSCD）iJournal 没有，查不到时直接告诉用户，不要猜。
