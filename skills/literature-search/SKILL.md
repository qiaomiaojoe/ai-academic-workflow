---
name: literature-search
description: 文献搜索 skill（源自 AI学术工作台 02 文献搜索工作流，单品化）。按 PXYV 四维度检索 → 文献验真（零容忍防捏造）→ 金字塔分层筛选（Classic/Key/Supporting 硬指标）→ 获取 DOI/PDF → 入库 Zotero + 可视化。不依赖选题.md：用户直接给选题一句话或 PXYV/关键词即可跑。Trigger on："帮我搜文献"、"文献搜索工作流"、"按金字塔搜 30 篇文献"、"搜文献入 Zotero"、"search literature for my topic"、"build a literature pyramid"、"find and import papers to Zotero"。
---

# Literature Search · PXYV 四维检索 + 金字塔分层 + Zotero 入库

按 4 个阶段执行：搜索 → 筛选 → 获取 DOI/PDF → 入库 Zotero。**每个阶段完成后输出该阶段结果表格，等用户确认后再进入下一阶段**；用户说"继续"就直接进下一阶段。

## 单品调用约定（输入解耦）

1. **用户直接给的优先**：一句话选题 / PXYV / 关键词清单 / 对标论文。若用户只给了一句话选题，先花一步把它拆成 PXYV 四维（P 理论视角 / X 现象 / Y 语境 / V 拟区分的近邻方向），给用户过目确认后再开搜——不要求用户先跑选题工作流。
- **工作台项目**（可选）：若项目里有 `01_选题/选题.md`（含 workbench 锚块 + 5 近邻），以它为权威依据（任何冲突以该文件为准）。
- **都没有**：向用户一次问齐——选题一句话（必填）+ 下方搜索参数中想改的项。

**搜索参数（均有默认值，用户可覆盖）**：
- 目标总篇数：默认 30；金字塔分配：Classic 1 篇 / Key 默认 5 篇 / Supporting = 总数−1−Key（每节点 ≈ Supporting/4）
- 发表年限：默认近 5 年（Classic 不受此限，可放宽到 1990）
- 文献语言：默认跟随选题语言（中文选题 → 中英混合，可指定纯中/纯英）
- 检索工具：按环境实际可用的挑（见下）；Zotero Collection 名：默认 = 项目名或用户给的选题短名
- 额外检索要求（可选，优先级高于默认设置）

**输出落盘降级**：在项目里 → `02_文献/文献清单.md`、`02_文献/pdf_download/`、`02_文献/[slug]-visualization.html`；不在项目里 → 当前目录 `./文献清单.md`、`./pdf_download/`、`./文献-visualization.html`。

**工具适配**：只用环境里实际可用的检索工具，缺对应 skill 时跳过该工具并告知；若没有任何可用检索工具，停下来输出各维度检索词清单给用户手动执行，不要编造结果。

## 可用检索工具注册表

| 工具 | 语言 | 调用方式 |
|------|------|---------|
| 自带 Web Search | 中英 | 环境内置联网搜索检索学术来源（Google Scholar / Semantic Scholar / OpenAlex / Crossref / 出版商页） |
| Google Scholar | 中英 | `gs-advanced-search` / `gs-search` 检索，`gs-cited-by` 引文滚雪球，`gs-export` 推 Zotero |
| ScienceDirect | 英 | `sd-advanced-search` / `sd-search` 检索，`sd-paper-detail` 取元数据，`sd-download` 下 PDF，`sd-export` 推 Zotero |
| Web of Science | 英 | `wos-search` 检索（可按数据库/版本过滤），`wos-paper-detail` 取元数据+影响因子，`wos-download` 下 PDF，`wos-export` 推 Zotero（需机构登录） |
| 知网 CNKI | 中 | `cnki-advanced-search` 按来源类别（SCI/CSSCI/北大核心）检索，`cnki-parse-results` 提取结果，`cnki-paper-detail` 验真+取被引，`cnki-download` 下 PDF，`cnki-export` 推 Zotero |

CNKI 固定参数：文献类型仅"学术期刊"（严禁学位论文/会议/报纸/年鉴）；来源类别建议 CSSCI / 北大核心 / SCI 以锁定高质量期刊；年限按搜索参数（Classic 放宽到 1990）。每次搜完调用 `cnki-parse-results` 提取结构化结果。

## 阶段 1 · 搜索

按 PXYV 四维度检索。通用规则：
- 每个维度在该语言所有可用工具里各检索一遍，合并去重；命中不足先换同义词/上位词再扩检（每维至少 2 轮）。
- 来源限同行评审学术文献；明显非学术来源（博客 / Medium / 维基 / 知乎 / 推特 / ResearchGate 个人页）不作来源，仅 Step 3.3 找 PDF 时可用。
- 每个维度搜（每节点配额 +2）～（每节点配额 +5）条候选。

中文检索策略：
- P 维度：P 概念的标准中文术语 + 同义词（CNKI 用字段 `KY` 关键词精确锁定）；理论奠基文献归 Classic 并放宽到 1990
- X 维度：「现象词 AND 方法/数据词」（CNKI 用字段 `SU` 主题），定位实证研究
- Y 维度：「现象词 AND 本土语境词（中国 / 省份 / 行业 / 人群）」，定位制度与背景文献
- V 维度：用 5 篇近邻的关键词反查，找需显式区分的对手文献

英文检索策略：
- P 维度：core construct 的 seminal 文献 + 近 5 年应用；检索式 = "P 术语" AND (theory OR framework OR model)，经典奠基归 Classic
- X 维度：现象的实证研究；检索式 = "X 现象词" AND (empirical OR evidence OR effect OR study) AND 方法/数据词
- Y 维度：语境/背景文献（可含政策报告、行业数据）；检索式 = "X 现象词" AND 语境词（国家 / 地区 / 人群 / 行业）
- V 维度：需显式区分的近邻文献（必须找到）；用近邻标题关键词反查 + 沿 cited-by / citing 链滚雪球（Google Scholar 用 `gs-cited-by`）

输出格式 — 候选清单原始表（验真前）：
`| # | 标题 | 作者+年份 | 期刊 | 期刊层级 | 来源维度(P/X/Y/V) | DOI 或 CNKI ID |`

**Step 1.5 — 文献验真（强制，输出最终候选清单前必做）**：
1. **实查**：英文条目用 DOI 去 doi.org / Crossref / OpenAlex 解析，核对标题+作者+年份+期刊，并抓 cited-by（OpenAlex `cited_by_count` 或 Google Scholar 引用数）；来自 WoS / ScienceDirect 的可用 `wos-paper-detail` / `sd-paper-detail` 复核。中文条目用 `cnki-paper-detail` 抓详情页核对，并提取"被引"数字。
2. **被引数采集**：记入候选条目（Stage 3/4 可视化要用）。
3. **零容忍**：任何无法实查、字段对不上、查无此文的条目 → 标记 ⚠️ 可疑，直接剔除。

输出顺序：① 验真报告（通过 X 条 / 剔除 Y 条 / 剔除原因逐条注明）② 最终候选清单表（仅含验真通过条目，新增"被引"列）。

**不允许编造文献，宁缺毋滥**。某维度验真后不足配额 → 明确说"仅找到 N 条可信文献，建议补搜"，不要凑数。

## 阶段 2 · 筛选（金字塔分层）

阶段 1 已完成"是否真实 / 是否相关 / 是否在期刊源里"，阶段 2 只做：金字塔分层、对话关系判定、覆盖配额。

**金字塔三层硬指标**：
- **Classic（1 篇）**四条全满足：① P 维度核心概念的命名者/奠基者（同领域 ≥3 篇综述把它列为概念出处）② 总被引 ≥500（社科）或 ≥1000（自然科学/CS）③ 发表 ≥10 年仍在被引（近 2 年仍有 ≥10 次新引用）④ 不受发表年限限制
- **Key Texts（N 篇）**三条全满足：① 发表在 P 所在领域 top-tier 期刊（表格注明期刊名 + 位次依据，如 SSCI Q1 / 北大核心 / 影响因子 / CNKI 高被引）② 与本研究 RQ 存在直接对话关系 ③ 近 5 年年均引用 ≥10。整组 Key 必须覆盖 P / X / V 三维，每维 ≥1 篇（Y 通常无 Key）
- **Supporting（~余量）**：① 提供具体证据（数据/案例/方法对照/政策文本/行业报告均可）② 按 P/X/Y/V 四节点分配：P/X ≥5，Y/V ≥3 ③ 同行评审期刊优先；权威机构报告可作 Y 节点补充

**三机制检查**：
1. **分层归位**：每篇候选明确判到 Classic / Key / Supporting / 拒（四选一），表格注明分层证据；不满足任一层硬指标 → 拒并注明具体指标。
2. **对话关系**（Key 必填）：这篇是在**支持、扩展、还是反驳**本研究 RQ 的某个立场？一句话说明。仅"主题相关"不构成对话的 Key 候选 → 降级为 Supporting。
3. **覆盖配额**：P ≥5 / X ≥5 / Y ≥3 / V ≥3？Key 覆盖 P/X/V 三维？任一未达标 → 输出"维度缺口表"（缺哪些 + 再搜关键词建议）。不允许用编造或勉强的文献凑配额；让用户决定是否回阶段 1 补搜。

额外输出：对每篇入选文献抽取一句话核心论点（≤30 字，Stage 4 可视化悬停提示用）。

输出格式：`| # | 标题 | 作者+年份 | 金字塔层 | PXYV 节点 | 分层证据 | 对话关系（仅 Key） | 核心论点(≤30字) | DOI/CNKI ID |` + 被拒清单及原因 + 维度缺口表（若有）。

## 阶段 3 · 获取 DOI / PDF + 引用数补全

- Step 3.1 确认 DOI / URL / CNKI ID：英文论文 → DOI；中文论文 → CNKI ID + 期刊+期号；经典专著 → 出版商 URL 或 DOI；非学术来源 → URL。
- Step 3.2 补全引用数：英文用 OpenAlex API（`https://api.openalex.org/works/doi:{DOI}` 取 `cited_by_count`）或 Google Scholar；中文用 `cnki-paper-detail`。阶段 1.5 已采的不重做。
- Step 3.3 查找 PDF 全文并落盘：英文优先 `sd-download` / `wos-download` → Open Access（Unpaywall / OpenAlex / 出版商 OA）→ 作者自存档 → preprint（arXiv / SSRN / OSF）；中文用 `cnki-download`（要求已登录）。PDF 保存到 pdf_download/（命名 AuthorYear.pdf）；找不到标 "no-pdf"。
- Step 3.4 落盘最终清单到 `文献清单.md`（markdown 表格原样保存；这是后续文献分析在 Zotero 不可用时的兜底元数据输入）。

最终清单格式：`| # | 标题 | 作者+年份 | 金字塔层 | PXYV 节点 | DOI/CNKI ID | 被引数 | 核心论点(≤30字) | PDF 状态 |`（PDF 状态 = open-access / preprint / author-copy / cnki / no-pdf）

## 阶段 4 · 入库 Zotero + 可视化

用 Zotero MCP 工具（或 `gs-export` / `sd-export` / `wos-export` / `cnki-export` 直接推送）：

Step 4.1 创建 Collection 结构：顶层 = Collection 名，其下 Classic / Key Texts / Supporting-P / Supporting-X / Supporting-Y / Supporting-V 六个子集合。

Step 4.2 逐条入库：有 DOI → `zotero_add_by_doi(doi, collections=[对应子集], tags=[金字塔层, PXYV节点, 项目slug], attach_mode="auto")`；只有 URL/CNKI → `zotero_add_by_url`。入库后用 `zotero_update_item` 把 citations / core_argument / pxyv_weights 写入 `extra` 字段：

```
citations: 123
core_argument: 一句话核心论点
pxyv_weights: P=0.7, V=0.3
```

（pxyv_weights 用于图 2 罗盘投影，权重按"主导维度"生成；单一维度 = 1.0。标签规则：金字塔层 "classic"/"key"/"supporting"；节点 "P"/"X"/"Y"/"V" 可多选；项目 slug。）

Step 4.3 入库报告：`| # | 标题 | 入库状态 | PDF 附件 | Collection | 标签 |` + 统计（总入库 / PDF 已附 / 金字塔分布 / 节点覆盖）。

Step 4.4 生成入库可视化（单文件 HTML，纯 HTML+CSS+内联 SVG，无外部库；浅色背景 #FAF7F2，amber accent #B8834A）：
- **图 1 文献金字塔分布图**：三层水平堆叠，顶 Classic（窄，标篇名+作者）→ 中 Key（标标题+主要节点）→ 底 Supporting（按数量宽度）；Classic #E65100 / Key #1565C0 / Supporting #558B2F；上窄下宽。
- **图 2 PXYV 四维罗盘投影**：800×800 SVG，中心为原点；四锚点 P=(0,+1) 顶 / X=(+1,0) 右 / Y=(0,-1) 底 / V=(-1,0) 左，边缘标大字母 + 颜色（P #B8834A / X #5B8DBE / Y #7BAE7F / V #9B6DB0）。每篇文献一个圆点：位置 = PXYV 权重归一化加权质心（如 P=0.7、V=0.3 → (−0.3, +0.7)）；半径 = `r = 4 + 6 * log10(citations + 1)`，clip [4,24]px；填充色 = 金字塔层（opacity 0.7）；描边 = 主导维度色。悬停 tooltip：标题 / 作者+年份 / 引用数 / 核心论点。浅灰同心圆 0.25/0.5/0.75/1.0 网格；左下角圆点大小图例、右下角颜色图例。

输出文件：`[slug]-visualization.html`（按落盘降级规则定目录）。
