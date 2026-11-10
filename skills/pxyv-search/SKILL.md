---
name: pxyv-search
description: PXYV 四维度文献检索（乔淼PhD · AI学术训练营 · AI学术工作流）。按 P 理论 / X 现象 / Y 语境 / V 近邻四个维度设计检索式并执行（英文先用 Google Scholar，搜不成才用 OpenAlex；中文用 CNKI），可按期刊级别（SSCI / JCR 分区等）筛，中英双语策略，输出候选文献清单表。只做检索，不验真不分层——验真用 lit-verify，分层用 lit-pyramid。Trigger on："按 PXYV 四维帮我检索文献"、"四维度文献检索"、"给这个选题设计检索式并搜一轮"、"run a PXYV four-dimension literature search"。
---

# PXYV Search · 四维度文献检索

按 PXYV 四维度检索文献，输出**候选清单**（验真前）。本 skill 只负责"搜"；验真交 `lit-verify`，分层交 `lit-pyramid`。

## 调用约定（独立运行）

- 输入优先级：用户直接给的 PXYV / 关键词清单 > `选题.md`（锚块 + 5 近邻，为权威依据）> 用户只给一句话选题 → 先调 `topic-pxyv-parse` 拆四维，用户确认后再搜。
- 参数（均有默认，用户可覆盖）：每维候选条数（默认 8-10 条）；发表年限（默认近 5 年，Classic/奠基文献放宽到 1990）；文献语言（默认跟随选题语言，可指定纯中/纯英/双语）；期刊级别要求（默认不筛；用户说了才筛，比如「只要 SSCI」「JCR Q1–Q2」）；额外检索要求（优先级最高）。
- 输出：会话内候选清单表；可追加落盘 `检索候选.md`（默认当前工作目录）。
- 工具适配：按下面「检索顺序」选工具，缺对应 skill 时跳过并告知；**没有任何可用工具时，输出各维度检索词清单给用户手动执行，不编造结果**。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。

## 可用检索工具注册表

| 工具 | 语言 | 调用方式 |
|------|------|---------|
| Google Scholar | 英文第一选择 | `scholar` skill 的 `search`（`--author` / `--journal` / `--years` / `--title-only` / `--exact`）；`cited-by` 引文滚雪球 |
| OpenAlex | 英文第二选择（只在谷歌学术搜不成时用） | `openalex` skill 的 `search`（带摘要，付费文章多半没有）；`cited-by` / `refs` 引用链；`verify` 补完整刊名、作者、DOI |
| 知网 CNKI | 中文第一选择 | `cnki` skill 的 `search`：`--field` 选字段，`--core` 限 CSSCI / 北大核心 等，`--years` 限年份，回结构化结果 |
| 自带 Web Search | 最后手段 | 环境内置联网搜索检索学术来源（出版商页、Semantic Scholar、Crossref 等） |

## 检索顺序（必须照做）

用户或工作台明确指定了工具时，按指定的来。否则：

**英文**
1. 开始前提醒用户一句：谷歌学术可能弹验证码，要在弹出的窗口里点，最好留在电脑旁；没人点会自动改用 OpenAlex。
2. 每个检索式**先跑 `scholar` 的 `search`**。不能因为 OpenAlex 刊名更全、只要几条、或要按期刊级别筛，就跳过这一步。`scholar` 的输出不要截断，太长就存成文件再读；截断了也不要重跑同一条。
3. 只有下面这些情况，才对没搜成的检索式改用 `openalex` 的 `search`：
   - 没装 `scholar` skill；
   - `scholar` 回 `unreachable` / `blocked` / `limit` / `layout_changed` / `no_browser`；
   - `scholar` 回 `captcha`（3 分钟没人点）。
4. `scholar` 回 `not_found`：换词再搜谷歌学术，这不算搜不成。回 `error`：看 `msg` 改好参数再跑。
5. 回 `blocked` / `limit` / `captcha` 后，这次不要再跑谷歌学术，已经拿到的结果保留，其余检索式用 `openalex`。用户说换了网络，才按 `scholar` 的说明加 `--new-network` 再试。
6. **改用 OpenAlex 时多搜一轮上位词**：OpenAlex 搜不到付费文章的正文，篇名和摘要里没出现检索词的付费文章会漏掉（11-10 实测：谷歌学术前 40 条里 12 篇付费，OpenAlex 同一检索式只搜中 4 篇）。所以每个维度除了原检索式，再用上位词或相邻构念搜一轮（如 burnout → stress / coping / well-being），合并去重。用户限定了检索式数量时按用户的，在报告里说明没补搜。从最相关的几篇做 `cited-by` / `refs` 滚雪球是可选的，结果多，要按主题词和年份筛。
7. `scholar`、`openalex` 都用不了，才用自带 Web Search。

**中文**：用 `cnki`。只有没装 `cnki` skill 时才用自带 Web Search，并在报告里写明。

CNKI 固定参数：文献类型仅"学术期刊"（`--type 期刊`，严禁学位论文/会议/报纸/年鉴）；来源类别建议 `--core CSSCI,北大核心`；`--size 50` 一次多取，少翻页（知网查得太密会拦）。`cnki` 回的 status 不是 `ok` / `not_found` 时，按它的说明处理，这一库标「没搜成」并告诉用户，不拿别的库的结果冒充知网。

Google Scholar：每页 10 条（`scholar` 默认就是，不要传更大的 `--size`：一页 20 条谷歌会直接拦），不够再 `--page 2` 翻页。

**不能搜 Web of Science、Scopus**（要学校订阅）。谷歌学术和 OpenAlex 的结果**不等于这两个库的检索结果**，不要写成「检索了 WoS / Scopus」。

## 按期刊级别筛（用户要求时）

1. 谷歌学术的刊名常被截断（以 `…` 结尾）：先用 `openalex` 的 `verify --file` 补全完整刊名和 DOI；
2. 刊名去重后，用 `journal-rank` 的 `lookup` 查（一次传几本；有 ISSN 时写成 `"刊名|ISSN"` 一起传，**不要只传 ISSN**：只出电子版的刊按 ISSN 常常查不到），结果填进候选表的「期刊层级」列；
3. 按用户要的级别筛掉其余的。查不到的（中文刊、`journal-rank` 没收的）单列出来问用户，不当成不合格；
4. 报告写明：「按 iJournal 的期刊收录和分区筛选（查询日期）。不等于 Web of Science / Scopus 检索结果。」检索来源按「输出」一节写。

## 检索策略

通用规则：
- 每个维度按「检索顺序」检索，合并去重；命中不足先换同义词/上位词再扩检（**每维至少 2 轮**，用户限定了检索式数量时按用户的）。
- 来源限同行评审学术文献；明显非学术来源（博客 / Medium / 维基 / 知乎 / 推特 / ResearchGate 个人页）不作来源。

中文检索：
- P 维度：P 概念的标准中文术语 + 同义词（CNKI 用字段 `KY` 关键词精确锁定）；理论奠基文献放宽到 1990
- X 维度：「现象词 AND 方法/数据词」（CNKI 用字段 `SU` 主题），定位实证研究
- Y 维度：「现象词 AND 本土语境词（中国 / 省份 / 行业 / 人群）」，定位制度与背景文献
- V 维度：用 5 近邻的关键词反查，找需显式区分的对手文献

英文检索：
- P 维度：core construct 的 seminal 文献 + 近 5 年应用；检索式 = "P 术语" AND (theory OR framework OR model)
- X 维度：现象的实证研究；检索式 = "X 现象词" AND (empirical OR evidence OR effect OR study) AND 方法/数据词
- Y 维度：语境/背景文献（可含政策报告、行业数据）；检索式 = "X 现象词" AND 语境词（国家 / 地区 / 人群 / 行业）
- V 维度：需显式区分的近邻文献（**必须找到**）；用近邻标题关键词反查 + 沿 cited-by / citing 链滚雪球（`scholar` 的 `cited-by`，或 `openalex` 的 `cited-by` / `refs`）

## 输出

先写检索来源，每个用到或该用的库一行：谷歌学术写「搜成了」或「没搜成 + `status` / 原因」；OpenAlex 写「没用」或「谷歌学术没搜成，改用」，改用时加一句「OpenAlex 搜不到付费文章的正文，付费文章可能漏掉一些；谷歌学术能用时（比如换个网络）可以再补搜」；知网同样写清。

再亮出各维度实际用的检索式（工具 + 年限），然后给候选清单原始表：

`| # | 标题 | 作者+年份 | 期刊 | 期刊层级 | 来源维度(P/X/Y/V) | DOI 或 CNKI ID |`

末尾报告：各维命中数、扩检轮次、命中不足的维度 + 建议补搜关键词。**下一步建议**：把清单交给 `lit-verify` 验真（强制，未验真的清单不得直接入库或写综述）。
