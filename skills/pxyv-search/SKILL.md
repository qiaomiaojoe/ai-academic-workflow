---
name: pxyv-search
description: PXYV 四维度文献检索（乔淼PhD · AI学术训练营 · AI学术工作流）。按 P 理论 / X 现象 / Y 语境 / V 近邻四个维度设计检索式并在可用检索工具（Web Search / Google Scholar / ScienceDirect / WoS / CNKI）里执行，中英双语策略，输出候选文献清单表。只做检索，不验真不分层——验真用 lit-verify，分层用 lit-pyramid。Trigger on："按 PXYV 四维帮我检索文献"、"四维度文献检索"、"给这个选题设计检索式并搜一轮"、"run a PXYV four-dimension literature search"。
---

# PXYV Search · 四维度文献检索

按 PXYV 四维度检索文献，输出**候选清单**（验真前）。本 skill 只负责"搜"；验真交 `lit-verify`，分层交 `lit-pyramid`。

## 调用约定（独立运行）

- 输入优先级：用户直接给的 PXYV / 关键词清单 > `选题.md`（锚块 + 5 近邻，为权威依据）> 用户只给一句话选题 → 先调 `topic-pxyv-parse` 拆四维，用户确认后再搜。
- 参数（均有默认，用户可覆盖）：每维候选条数（默认 8-10 条）；发表年限（默认近 5 年，Classic/奠基文献放宽到 1990）；文献语言（默认跟随选题语言，可指定纯中/纯英/双语）；额外检索要求（优先级最高）。
- 输出：会话内候选清单表；可追加落盘 `检索候选.md`（默认当前工作目录）。
- 工具适配：只用环境实际可用的检索工具，缺对应 skill 时跳过并告知；**没有任何可用工具时，输出各维度检索词清单给用户手动执行，不编造结果**。

## 可用检索工具注册表

| 工具 | 语言 | 调用方式 |
|------|------|---------|
| 自带 Web Search | 中英 | 环境内置联网搜索检索学术来源（Google Scholar / Semantic Scholar / OpenAlex / Crossref / 出版商页） |
| Google Scholar | 中英 | `gs-advanced-search` / `gs-search`；`gs-cited-by` 引文滚雪球 |
| ScienceDirect | 英 | `sd-advanced-search` / `sd-search`；`sd-paper-detail` 取元数据 |
| Web of Science | 英 | `wos-search`（可按数据库/版本过滤）；`wos-paper-detail` 取元数据+影响因子 |
| 知网 CNKI | 中 | `cnki-advanced-search` 按来源类别（SCI/CSSCI/北大核心）检索；`cnki-parse-results` 提取结果 |

CNKI 固定参数：文献类型仅"学术期刊"（严禁学位论文/会议/报纸/年鉴）；来源类别建议 CSSCI / 北大核心 / SCI；每次搜完调用 `cnki-parse-results` 提取结构化结果。

## 检索策略

通用规则：
- 每个维度在该语言所有可用工具里各检索一遍，合并去重；命中不足先换同义词/上位词再扩检（**每维至少 2 轮**）。
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
- V 维度：需显式区分的近邻文献（**必须找到**）；用近邻标题关键词反查 + 沿 cited-by / citing 链滚雪球（`gs-cited-by`）

## 输出

先亮出各维度实际用的检索式（工具 + 年限），再给候选清单原始表：

`| # | 标题 | 作者+年份 | 期刊 | 期刊层级 | 来源维度(P/X/Y/V) | DOI 或 CNKI ID |`

末尾报告：各维命中数、扩检轮次、命中不足的维度 + 建议补搜关键词。**下一步建议**：把清单交给 `lit-verify` 验真（强制，未验真的清单不得直接入库或写综述）。
