# AI学术工作流 · 「AI学术训练营」skills 库（乔淼PhD）

> 「**AI学术训练营**」（乔淼PhD）配套的 **AI学术工作流** skills 库：把训练营讲授的完整学术工作流——**选题 → 文献搜索 → 文献分析 → 研究设计 → 数据分析 → 全文初稿**——拆到步骤颗粒度，共 **30 个 skills**。装进 Claude Code / Codex，按任务单独调用，或自由排列组合。
>
> **谁在用**：AI学术训练营学员
---

## 这是什么

「AI学术训练营」教的是一套完整的 **AI学术工作流**，方法论锚点与课程一致：

| 讲次 | 工作流 | 方法论锚 |
|------|--------|---------|
| L2 | 选题 | PXYV 公式 + 四种选题模式 + 贡献阶梯 + 近邻对位 |
| L3 | 文献搜索 / 文献分析 | 文献金字塔 + 验真机制 + 综述蓝图 / 知识模块 |
| L4 | 研究设计 / 写作框架 | 方法地图 + methodology plugin + 动静虚实框架 |
| L5-L6 | 数据分析 / 造 skill | Neuman 7e Ch12 定量 + Ch14 定性 + skill 制作链路 |

训练营学员手里有两件配套工具，**分工不交叉**：

- **AI学术工作台**（单文件 HTML，随课发放）——为六大工作流之间的**流畅交接**而优化：填表出 prompt、产出按命名表落盘、下一步自动读上一步。适合从头到尾跑通一篇论文。
- **本仓库的 skills 库**——把同一套工作流拆到**步骤颗粒度**：每个 self-contained 的功能和步骤都是一个独立 skill，单个 skill 就能运行。适合脱离整篇论文的特定任务（单独搜一批文献、单独验真一份参考文献、单独找 research gap、单独拆一篇范文……），也适合按自己的需要排列组合。

每个 skill 都是同一个三层拼装：

- 📖 **方法论** — 每一步锚定权威来源（上表），不是 AI 即兴发挥
- 🤖 **Skill** — 把方法步骤翻译成 Claude Code / Codex 能执行的指令，硬约束写死（不编造文献、验真零容忍、零结果合法呈现、每个数值报 N）
- 👤 **你** — 理论判断 / 关键选择 / 实质性意义（每个 checkpoint 都停下等你拍板，AI 不替你做主）

三者拼起来 → **AI 扛流程，你做判断**。

---

## Skills 树（30 个）

按工作流组织。**任务级** skill 是完整任务的入口（内部按序编排步骤级 skills，阶段间停下确认）；**步骤级** skill 单独调用、自由组合。

### 0 · 项目初始化（可选）

| Skill | 用途 |
|-------|------|
| [`academic-project-init`](skills/academic-project-init/SKILL.md) | 建标准项目结构 + CLAUDE.md 命名表。建了项目结构，各 skills 的产出会自动落盘衔接；不建也不影响任何 skill 单独运行 |

### 01 · 选题

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`topic-workbench`](skills/topic-workbench/SKILL.md) | 分诊入口：判断该用哪种选题模式 → 转对应 skill |
| 步骤级 | [`topic-theory-interpretation`](skills/topic-theory-interpretation/SKILL.md) | 模式① 理论诠释：三阶段选题教练（挖掘→校准→输出 RQ/Thesis） |
| 步骤级 | [`topic-hypothesis-testing`](skills/topic-hypothesis-testing/SKILL.md) | 模式② 假设检验：三阶段选题教练（输出 H 假设链 + 操作化） |
| 步骤级 | [`topic-concept-construction`](skills/topic-concept-construction/SKILL.md) | 模式③ 概念建构：三阶段选题教练（输出原创概念 + 诠释路径） |
| 步骤级 | [`topic-method-driven`](skills/topic-method-driven/SKILL.md) | 模式④ 方法驱动：三阶段选题教练（输出 Aims + 双 V 方法计划） |
| 步骤级 | [`topic-pxyv-parse`](skills/topic-pxyv-parse/SKILL.md) | 已有选题的 PXYV 四维拆分 + 缺口诊断（不重跑三阶段） |

### 02 · 文献搜索

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`literature-search`](skills/literature-search/SKILL.md) | 完整文献搜索：检索 → 验真 → 分层 → 入库，逐阶段确认 |
| 步骤级 | [`pxyv-search`](skills/pxyv-search/SKILL.md) | PXYV 四维度文献检索（中英策略 + 多工具，只搜不筛） |
| 步骤级 | [`lit-verify`](skills/lit-verify/SKILL.md) | 文献验真：逐条实查 DOI/CNKI，零容忍剔除可疑条目 |
| 步骤级 | [`lit-pyramid`](skills/lit-pyramid/SKILL.md) | 金字塔分层：Classic / Key / Supporting 硬指标 + 对话关系 + 覆盖配额 |
| 步骤级 | [`lit-pdf-zotero`](skills/lit-pdf-zotero/SKILL.md) | 批量 PDF 获取 + Zotero 入库 + 金字塔/PXYV 罗盘可视化 |

### 03 · 文献分析

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`literature-analysis`](skills/literature-analysis/SKILL.md) | 完整文献综述：模块清单 → 蓝图 → gap → 模块生成 → 初稿组装 |
| 步骤级 | [`knowledge-module-list`](skills/knowledge-module-list/SKILL.md) | 知识模块清单：跨文档分析，每模块带证据假设 + 独立生成 prompt |
| 步骤级 | [`review-blueprint`](skills/review-blueprint/SKILL.md) | 综述蓝图：模块编排成综述逻辑结构 + 可视化 HTML |
| 步骤级 | [`research-gap-scan`](skills/research-gap-scan/SKILL.md) | Research Gap 识别：组合扫描 + 三问反驳防伪 gap |
| 步骤级 | [`knowledge-module-gen`](skills/knowledge-module-gen/SKILL.md) | 知识模块生成：机械抽取 spec + map-reduce 逐篇 + 页码诚实 + 执行日志 |
| 步骤级 | [`review-draft-assembly`](skills/review-draft-assembly/SKILL.md) | 综述初稿组装：三 Section 组装 + 引用核验 + 反 AI 味 + docx |

### 04 · 研究设计

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`research-design`](skills/research-design/SKILL.md) | 完整研究设计：方法地图 + 方案 →（你选）→ 初稿 |
| 步骤级 | [`methods-map`](skills/methods-map/SKILL.md) | 方法地图：逐篇扫描方法论 9 字段 + methodology plugin + 2-3 个设计方案 + 可视化 |
| 步骤级 | [`methodology-draft`](skills/methodology-draft/SKILL.md) | 研究设计初稿：段骨架 + 可执行设计清单 + 干净版 Sec 4 方法论 draft |

### 05 · 数据分析

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`data-analysis-round`](skills/data-analysis-round/SKILL.md) | 跑一轮分析（定量 / 定性 / 自定义 skill），多轮记账不覆盖 |
| 任务级 | [`findings-synthesis`](skills/findings-synthesis/SKILL.md) | 综合发现：全部轮次产出 → 对应 RQ 的研究发现（convergence/divergence） |
| 方法级 | [`analyze-quantitative-data`](skills/analyze-quantitative-data/SKILL.md) | 定量分析全流程（Neuman Ch12，内含 7 个 prompt，见下） |
| 方法级 | [`analyze-qualitative-data`](skills/analyze-qualitative-data/SKILL.md) | 定性分析全流程（Neuman Ch14，内含 11 个 prompt，见下） |

### 06 · 全文初稿

| 层级 | Skill | 用途 |
|------|-------|------|
| 步骤级 | [`model-paper-deconstruct`](skills/model-paper-deconstruct/SKILL.md) | 拆 Model Paper：动静虚实四产出高密度拆解（≥6000 字） |
| 步骤级 | [`article-framework`](skills/article-framework/SKILL.md) | 反推文章框架：5 Part 骨架 + 引用预算 + 结构对照 + 可视化 |
| 步骤级 | [`fulltext-draft`](skills/fulltext-draft/SKILL.md) | 全文初稿扩写：骨架 → 可打磨的段落散文（管线终点） |

### S · 数据 Skill 工坊（自己造 skill）

| 层级 | Skill | 用途 |
|------|-------|------|
| 步骤级 | [`skill-workshop-plan`](skills/skill-workshop-plan/SKILL.md) | 规划 + 找料：诊断要不要造、造哪几个 + 下载权威方法学源材料 |
| 步骤级 | [`skill-forge`](skills/skill-forge/SKILL.md) | 源材料 → 成品 skill：5 阶段 2 停点链路（Claude Code / Codex 双平台规范） |

---

## 18 个 prompt 与 2 个数据分析 skills 的关系

`prompts/` 目录下的 **18 个 prompt（定量 7 + 定性 11）就是 `analyze-quantitative-data` 和 `analyze-qualitative-data` 两个 skills 的内容本体**——装了这两个 skills，Claude Code / Codex 会在合适的分析步骤自动应用对应 prompt 的方法与硬约束；不装 skills（或用其他 LLM）的用户，也可以直接浏览 `prompts/`，复制 `## ✂️ Prompt 模板` 段落粘贴填空使用。

### 📊 定量 · Neuman Ch 12（7 个，= analyze-quantitative-data 的步骤）

| # | Prompt | 何时用 |
|---|--------|--------|
| 01 | [建立 Codebook](prompts/quant/01-codebook.md) | 拿到原始数据, 还没整理成可分析格式时 |
| 02 | [清洗数据](prompts/quant/02-clean-data.md) | Codebook 建好, 跑分析前 |
| 03 | [单变量分析](prompts/quant/03-univariate.md) | 看每个变量长什么样 |
| 04 | [双变量分析](prompts/quant/04-bivariate.md) | 看两个变量之间的关系 |
| 05 | [多变量阐释模型](prompts/quant/05-multivariate-elaboration.md) | 用控制变量看 bivariate 是否虚假 |
| 06 | [多元回归](prompts/quant/06-multivariate-regression.md) | 多个自变量同时影响一个因变量 |
| 07 | [推断统计](prompts/quant/07-inferential.md) | 从样本推论总体, 显著性检验 |

### 📝 定性 · Neuman Ch 14（11 个，= analyze-qualitative-data 的步骤）

**编码三阶段** (Strauss 1987):

| # | Prompt | 何时用 |
|---|--------|--------|
| 01 | [开放编码 Open Coding](prompts/qual/01-open-coding.md) | 第一遍读数据, 浮现初步主题 |
| 02 | [轴心编码 Axial Coding](prompts/qual/02-axial-coding.md) | 找概念之间的连接和轴心 |
| 03 | [选择编码 Selective Coding](prompts/qual/03-selective-coding.md) | 主要主题已确定, 扫全部数据找代表证据 |

**边编码边写**:

| # | Prompt |
|---|--------|
| 04 | [分析备忘录 Analytic Memo](prompts/qual/04-analytic-memo.md) |
| 05 | [Outcropping 识别](prompts/qual/05-outcropping.md) |

**七大分析策略**:

| # | Prompt | 适用情境 |
|---|--------|---------|
| 06 | [Ideal Types](prompts/qual/06-ideal-types.md) | 用纯净模型对照现实 |
| 07 | [Successive Approximation](prompts/qual/07-successive-approximation.md) | 反复迭代概念与证据 |
| 08 | [Illustrative Method](prompts/qual/08-illustrative-method.md) | 用证据填充既有理论的空盒子 |
| 09 | [Domain Analysis](prompts/qual/09-domain-analysis.md) | Spradley 文化领域分析 |
| 10 | [Mill 分析比较](prompts/qual/10-analytic-comparison-mill.md) | 多案例比较, 找共同因果 |
| 11 | [Narrative Analysis](prompts/qual/11-narrative-analysis.md) | 历史/过程性数据, 找路径依赖 |

---

## 安装

### Claude Code · 一行命令

```bash
curl -fsSL https://raw.githubusercontent.com/qiaomiaojoe/ai-academic-workflow/main/install.sh | bash
```

（脚本会把仓库内全部 skills 装到 `~/.claude/skills/`；检测到 Codex 目录时同时装到 `${CODEX_HOME:-$HOME/.codex}/skills/`。）

### Codex / 手动安装

```bash
git clone https://github.com/qiaomiaojoe/ai-academic-workflow.git

# Claude Code
cp -r ai-academic-workflow/skills/* ~/.claude/skills/

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -r ai-academic-workflow/skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

只想要某几个 skill？拷对应目录即可——**每个 skill 自包含，单独装单独用**。

### 触发例句（装好后直接说）

- "帮我选题，我想研究……" → `topic-workbench` 分诊 → 对应选题模式
- "把我的选题拆成 PXYV" → `topic-pxyv-parse`
- "检查这些参考文献是不是编的" → `lit-verify`
- "把这批文献做金字塔分层" → `lit-pyramid`
- "帮我找这个方向的 research gap" → `research-gap-scan`
- "我要分析这份调查数据" → `analyze-quantitative-data`；"帮我编码这些访谈" → `analyze-qualitative-data`
- "拆这篇 model paper" → `model-paper-deconstruct`
- "把这本教科书 PDF 做成 skill" → `skill-forge`
- "帮我搜文献入 Zotero"（完整任务）→ `literature-search`；"做文献综述" → `literature-analysis`

---

## Skills 设计原则

1. **单个 skill 可独立运行**：输入按"你直接给的 > 项目结构自动读 > 问最小输入"三级解析，不因缺上游文件卡住。
2. **可组合**：在 `academic-project-init` 建的项目结构里，产出按 CLAUDE.md 命名表落盘，下游 skill 自动衔接；步骤级 skills 也可以按你的需要任意排列组合。
3. **硬约束不稀释**：不编造文献（[TBD-citation] 占位）、验真零容忍、零结果合法呈现（Neuman p.426）、CRITICAL/REFUSE 原样保留。
4. **Checkpoint 必停**：方案选择、准则确认、落盘审批等关键节点必须停下等你拍板。
5. **Prompt 三段结构**（与训练营讲授一致）：前段喂 context → 中段学术逻辑（含硬约束）→ 后段落盘规范。

---

## 边界声明

**这套工作流不替代**:
- 研究问题的价值判断（PXYV 拆得出结构，拆不出你的学术品味）
- 因果识别（需要研究设计 + 域内专家）
- 复杂方法（mediation / SEM / multilevel）的最终把关

> 关键步骤必须找比你懂的人帮看 30 分钟——这是入门者的现实。AI + 方法论框架能把你从"完全不会"推到"能问出有质量的问题"。

---

## 引用

如果这套工作流帮到了你的研究, 引用:

```
乔淼 (2026). AI学术工作流: 从选题到全文初稿的 skills 库.
https://github.com/qiaomiaojoe/ai-academic-workflow
```

数据分析部分的教科书原始出处:

```
Neuman, W. L. (2014). Social Research Methods: Qualitative and Quantitative
Approaches (7th ed.). Pearson Education Limited.
```

## License

[CC BY 4.0](LICENSE) — 可以自由使用 / 修改 / 再分发, 保留原作者署名即可。
