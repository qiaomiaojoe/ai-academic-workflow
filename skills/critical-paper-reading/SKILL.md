---
name: critical-paper-reading
description: 单篇论文批判性阅读（乔淼PhD · AI学术训练营 · AI学术工作流 · 文献分析步骤）。基于 UOW (University of Wollongong) Critical Analysis 框架 —— 三层升级 (Description → Analysis → Evaluation) + 四维 interrogation (Content / Authorship / Currency & Quality / Critical Writing Language)，把一篇论文（PDF / Zotero item）拆成结构化的批判性阅读笔记，每条 claim 锚定页码、绝不编造。可独立运行，输入一个 PDF 路径或 Zotero item 即可。Trigger on: "critically read this paper", "critique this paper", "批判性阅读", "帮我批注这篇 paper", "读一下这篇 paper", "deconstruct this paper", "analyze this article critically", "评一下这篇文章".
---

# Critical Paper Reading · UOW 框架

基于 **University of Wollongong Academic Skills · Critical Analysis** 框架，把一篇论文（PDF / Zotero item）拆成结构化、可引用的批判性阅读笔记。

> 来源：https://www.uow.edu.au/student/support-services/academic-skills/online-resources/assessments/critical-analysis/

## 调用约定（独立运行）

- 输入（按下方 Input Protocol 顺序处理）：PDF 路径 / Zotero item 或 citation key / DOI / URL / 纯文本片段。信息不足时用 `AskUserQuestion` 问，不编造。
- 落盘：项目内 → `02_文献/深读/深读-{AuthorYear}.md`（此路径下的深读产物会被 `review-draft-assembly` 组装综述初稿时自动并入 Section 2）；项目外 → 当前目录 `./深读/深读-{AuthorYear}.md`；用户只要会话内结果就不落盘。
- 产出语言：项目 CLAUDE.md 有设定则从之，否则跟随用户。

## 何时使用 / When to invoke

✅ **用本技能** 的场景：
- 读一篇 paper，需要一份稳定的批判性阅读框架而不是摘要
- 判断一篇文献是否值得收进文献库 / 后续引用
- 需要回答"这篇文章怎么样 / 帮我看看这篇 paper"
- 为综述、讨论准备可引用的批判性句子

❌ **不要用本技能** 的场景（用其它 skill）：
- 写自己的论文 → 用 `article-framework` / `fulltext-draft`
- 多篇文献的系统综述 → 用 `literature-analysis`
- 拆一篇范文的写作结构（动静虚实）→ 用 `model-paper-deconstruct`
- 单纯翻译 / 提取 abstract → 用 Read 工具直接处理

## 核心框架 / The UOW Framework

### 三层升级 · Three-Level Progression

UOW 把批判性分析拆成三层，**每一层都必须答**：

| Layer | Questions | 中文含义 |
|-------|-----------|---------|
| 1. **Description** | Who? What? Where? When? | 论文事实层面 |
| 2. **Analysis** | How? Why? | 方法与因果 |
| 3. **Evaluation** | So what? What if? What next? | 意义与延伸 |

⚠️ **重要**：只停在 Description 层 = 不是批判性阅读，是摘要。必须推进到 Evaluation 层。

### 四维 Interrogation · Four Dimensions

每篇 paper 用以下四个维度逐项审问：

**Dimension 1 · Content**（内容本身）
- Research question 是什么？primary aims 清楚吗？
- 用了什么方法 / 证据类型？方法适配 RQ 吗？
- 样本量多大？抽样方法是什么？
- 结论是否 follow logically from findings，还是 overreach？
- 是否呈现 balanced perspectives，还是偏向某一方？
- 与领域内其它研究的发现相比如何？
- 数据 / 结果是否被诚实、可靠地报告？

**Dimension 2 · Authorship**（作者与意图）
- 谁写的？什么时候写的？为谁写的？
- 作者的资历 / 研究记录如何？所在机构？
- 谁资助的（funding / conflict of interest）？
- 哪些信息被排除了？为什么？
- 这项工作是否实质性推进了领域理解，还是只是 incremental？

**Dimension 3 · Currency & Quality**（时效与质量）
- 引用的证据是否 recent？是否 quality evidence？
- 证据是 scientific 还是 anecdotal？
- 引用是否 properly referenced and broadly sourced？
- 发表时间多近？该领域是否 fast-moving？

**Dimension 4 · Critical Writing Language**（如何把批注写成批判性散文）
当把以上分析写成可引用的批注时，用 UOW 推荐的批判性引导句：
- "This is significant because…"
- "This demonstrates…"
- "[Author 1] argues…, however [Author 2] claims…"
- 转折语：yet / nonetheless / nevertheless
- 条件语：if / unless / provided that

避免纯描述性写法（"作者说……作者认为……"），必须夹带评价。

## 输入处理协议 / Input Protocol

技能被触发时，按以下顺序处理输入：

1. **PDF 文件路径** → 用 `Read` 工具直接读（支持 PDF；超过 10 页时用 `pages` 参数分段）
2. **Zotero item / citation key**：
   - 先 `mcp__zotero__zotero_get_item_metadata` 拿 metadata
   - 再 `mcp__zotero__zotero_get_item_fulltext` 拿正文
   - 必要时 `mcp__zotero__zotero_get_pdf_outline` 看结构
3. **DOI / URL** → 用 `WebFetch` 或 `mcp__zotero__zotero_add_by_doi` 先入库
4. **纯文本片段** → 直接基于上下文工作，但在输出中标注"仅基于用户提供的片段"

**信息不足时**：用 `AskUserQuestion` 问用户，**不要编造**作者、年份、页码、引文。

## 执行协议 / Execution Protocol

1. **宣告**："I am using the **critical-paper-reading** skill to do a UOW-framework critical read of this paper."
2. **读取输入**（按上面 Input Protocol）
3. **按模板填充**（见下文模板）—— 每条 claim 必须用 in-text 页码 / section 名锚定
4. **输出**：
   - 在对话中直接给出完整批注
   - 同时按上方「调用约定」落盘（项目内 `02_文献/深读/深读-{AuthorYear}.md`，否则当前目录；用 Write 工具，目录不存在就先建）
5. **Verdict**：给一句话总评 + 是否值得纳入文献库 / 后续引用

## 跨切原则 / Cross-cutting Principles

1. **不编造引文 / 页码 / 作者背景**。不确定的地方写"unclear from text"或问用户。
2. **每个 claim 锚定页码**（格式：`(p. 7)` 或 `(Sec. 3.2)`）。
3. **不只停留在赞美**。如果一篇 paper 在某维度上确实有缺陷，必须说出来 —— 这是批判性阅读的核心。
4. **区分事实 vs 意见**。作者主张 ≠ 已成立的事实。
5. **Evaluation 层不能跳过**。如果只产出 Description + Analysis，技能没有完成。
6. **Verdict 必须给立场**："值得 / 部分值得 / 不值得"纳入文献库或后续引用，并说明理由。

## 输出模板 / Output Template

```markdown
# Critical Read · {Short Title}

**Bibliographic Info**
- Author(s):
- Year:
- Journal / Venue:
- DOI:
- Citation key (Zotero):
- 阅读日期:

---

## Layer 1 · Description (Who / What / Where / When)

- **Topic / 主题**:
- **Field / 学科**:
- **Setting / 研究场景**:
- **Time period covered / 涉及时段**:
- **Key terms / 核心概念**:

## Layer 2 · Analysis (How / Why)

- **Research Question(s)**:
- **Theoretical framework / 理论框架**:
- **Methodology**: (e.g., quantitative survey, ethnography, RCT, …)
- **Sample / Data**:
- **Key findings** (with page anchors):
  1. … (p. X)
  2. … (p. Y)
- **Logical chain / 论证链条**: How does the paper get from data to conclusions?

## Layer 3 · Evaluation (So what / What if / What next)

- **So what · 这项研究的实际意义**:
- **What if · 假如条件改变 / 反例**:
- **What next · 后续可研究的方向**:

---

## Four-Dimension Interrogation

### Dimension 1 · Content
- RQ 清晰度:
- 方法是否适配 RQ:
- 样本 & 抽样:
- 结论是否 overreach (具体举例 + 页码):
- 是否平衡 / balanced perspectives:
- 与领域其它研究的对照:

### Dimension 2 · Authorship
- 作者背景 / 所在机构:
- Funding / COI:
- 写作目的（学术？倡导？商业？）:
- 信息遗漏 (omissions):
- 对领域贡献 (incremental vs substantive):

### Dimension 3 · Currency & Quality
- 发表年份 & 领域时效性:
- 引用质量 (是否 recent, scientific, broadly sourced):
- Scientific vs anecdotal evidence:
- Reference list 抽查 (1-2 条 spot check):

### Dimension 4 · Critical Writing Snippets
（可直接复用到综述 / 讨论 / 批注的批判性句子）
- "This is significant because…"
- "X argues …, however Y suggests …"
- "Nevertheless, the sample size of N=… limits …"
- …

---

## Verdict / 总评

**一句话评价**:

**值得纳入文献库 / 后续引用？**  ☐ 值得  ☐ 部分值得（哪些片段）  ☐ 不值得

**理由**:

---

## Open Questions / What to Read Next

- 阅读后仍未解决的问题:
- 建议下一篇读: (作者, 年份 — 为什么)
```

## 验证 / Verification

技能落地后自测：
1. 触发测试：「帮我批判性阅读这篇 PDF: <path>」→ 应该看到本技能宣告 + 完整三层四维输出
2. Zotero 路径：「批注 Zotero 里这篇 [citation_key]」→ 应该走 zotero MCP
3. 反触发测试：「帮我写一篇论文」「帮我做文献综述」→ **不应该**触发本技能（路由到 `fulltext-draft` / `literature-analysis`）
4. 输出文件落在 `02_文献/深读/`（项目内）或当前目录 `./深读/`
