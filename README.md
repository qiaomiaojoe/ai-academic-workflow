# AI学术工作流 · 「AI学术训练营」skills 库（乔淼PhD）

> 「**AI学术训练营**」（乔淼PhD）配套的 **AI学术工作流** skills 库，按 **期刊初稿**、**综述文章**、**投稿与审稿** 三条工作流组织，共 **44 个 skills**。先选要完成的工作流，再按阶段调用 skill；也可以独立运行某一步。支持 Claude Code / Codex。
>
> **谁在用**：AI学术训练营学员
---

## 这是什么

本仓库目前收录三条工作流，覆盖研究性论文初稿、独立综述文章，以及已有稿件的改稿、投稿和返修：

| 工作流 | 阶段 | 目标产出 |
|--------|------|----------|
| **期刊初稿** | 选题 → 文献搜索 → 文献分析 → 研究设计 → 数据分析 → 全文初稿 | 一篇研究性论文的全文初稿 |
| **综述文章** | 综述选题 → 检索与筛选 → 证据综合 → 综述文章初稿 | 一篇系统 / 半系统·叙事 / 整合式综述文章 |
| **投稿与审稿** | 材料核实 → 初稿诊断与改稿 → 期刊要求核对 → 投稿包；收到意见后进入回应决策与返修 | 待作者确认的修订稿、投稿包及返修回复 |

工作流内的方法论锚点与训练营课程一致：

| 讲次 | 阶段 / 内容 | 方法论锚 |
|------|--------|---------|
| L1-2 | AI工作台 / 选题 | PXYV 公式 + 7 种选题模式（研究性 4 + 综述性 3 · Snyder 三型）+ 贡献阶梯 + 近邻对位 |
| L3 | 文献搜索 / 文献分析 | 文献金字塔 + 验真机制 + 综述蓝图 / 知识模块 |
| L4 | 研究设计 / 写作框架 | 方法地图 + methodology plugin + 动静虚实框架 |
| L5-L6 | 数据分析 / 造 skill | Neuman 7e Ch12 定量 + Ch14 定性 + skill 制作链路 |

训练营学员手里有两件配套工具，**分工不交叉**：

- **AI学术工作台**（单文件 HTML，随课发放）——为每条工作流中各阶段的**流畅交接**而优化：填表出 prompt、产出按命名表落盘、下一步自动读上一步。适合从头到尾跑通一篇论文。
- **本仓库的 skills 库**——把各条工作流拆到**步骤颗粒度**：按具体功能和步骤提供 skills，多数可独立运行；投稿与审稿的业务方法需配套安装共用入口和支持文件。适合脱离整篇论文的特定任务（单独搜一批文献、单独验真一份参考文献、单独找 research gap、单独拆一篇范文……），也适合按自己的需要排列组合。

每个 skill 都是同一个三层拼装：

- 📖 **方法依据** — 记录方法文献或已确认的项目设计；投稿与审稿各 skill 的 `references/` 保留来源与适用边界
- 🤖 **Skill** — 把方法步骤翻译成 Claude Code / Codex 能执行的指令，硬约束写死（不编造文献、验真零容忍、零结果合法呈现、每个数值报 N）
- 👤 **你** — 理论判断 / 关键选择 / 实质性意义（每个 checkpoint 都停下等你拍板，AI 不替你做主）

三者拼起来 → **AI 扛流程，你做判断**。

---

## Skills 树（按工作流分类 · 44 个）

以下是使用导航，按 **工作流 → 阶段 → skill** 展开；仓库中的安装目录仍为 `skills/<name>/`。同一个 skill 可被多条工作流复用，数量按唯一 skill 目录统计，不重复计数。

```text
AI学术工作流
├── 期刊初稿
│   ├── 项目初始化（可选）
│   ├── 01 选题
│   ├── 02 文献搜索
│   ├── 03 文献分析（产出论文的文献综述节）
│   ├── 04 研究设计
│   ├── 05 数据分析
│   ├── 06 全文初稿
│   └── 配套：数据 Skill 工坊
├── 综述文章
│   ├── 01 综述选题（系统 / 半系统·叙事 / 整合式）
│   ├── 02 检索与筛选
│   ├── 03 证据综合
│   └── 04 综述文章初稿
└── 投稿与审稿
    ├── 共用：任务登记与材料核实 · submission-task-intake
    ├── 01 初稿诊断 · manuscript-diagnosis
    ├── 02 批准范围内改稿 · manuscript-revision
    ├── 03 期刊要求核对 · journal-requirements-check
    ├── 04 投稿包整理 · submission-package-preparation
    ├── 05 审稿意见与回应决策 · review-response-planning
    └── 06 返修改稿与逐条回复 · review-revision-response
```

**任务级** skill 编排一个阶段的完整任务；**步骤级** skill 执行具体步骤；**方法级** skill 提供分析方法。各 skill 按自身约定保留人工判断与确认节点。

### 工作流一 · 期刊初稿

从研究问题出发，经过文献、研究设计与数据分析，形成可继续打磨的研究性论文初稿。理论研究等任务按具体研究需要选择阶段。

这里的“文献分析”服务于论文中的文献综述节，使用 `literature-analysis` / `review-draft-assembly`；整篇综述文章的流程见下方“工作流二”。

#### 0 · 项目初始化（可选）

| Skill | 用途 |
|-------|------|
| [`academic-project-init`](skills/academic-project-init/SKILL.md) | 建标准项目结构 + CLAUDE.md 命名表。建了项目结构，各 skills 的产出会自动落盘衔接；不建也不影响任何 skill 单独运行 |

#### 01 · 选题

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`topic-workbench`](skills/topic-workbench/SKILL.md) | 分诊入口：判断该用哪种选题模式 → 转对应 skill |
| 步骤级 | [`topic-theory-interpretation`](skills/topic-theory-interpretation/SKILL.md) | 模式① 理论诠释：三阶段选题教练（挖掘→校准→输出 RQ/Thesis） |
| 步骤级 | [`topic-hypothesis-testing`](skills/topic-hypothesis-testing/SKILL.md) | 模式② 假设检验：三阶段选题教练（输出 H 假设链 + 操作化） |
| 步骤级 | [`topic-concept-construction`](skills/topic-concept-construction/SKILL.md) | 模式③ 概念建构：三阶段选题教练（输出原创概念 + 诠释路径） |
| 步骤级 | [`topic-method-driven`](skills/topic-method-driven/SKILL.md) | 模式④ 方法驱动：三阶段选题教练（输出 Aims + 双 V 方法计划） |
| 步骤级 | [`topic-pxyv-parse`](skills/topic-pxyv-parse/SKILL.md) | 已有选题的 PXYV 四维拆分 + 缺口诊断（不重跑三阶段） |

#### 02 · 文献搜索

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`literature-search`](skills/literature-search/SKILL.md) | 完整文献搜索：检索 → 验真 → 分层 → 入库，逐阶段确认 |
| 步骤级 | [`pxyv-search`](skills/pxyv-search/SKILL.md) | PXYV 四维度文献检索（中英策略 + 多工具，只搜不筛） |
| 步骤级 | [`lit-verify`](skills/lit-verify/SKILL.md) | 文献验真：逐条实查 DOI/CNKI，零容忍剔除可疑条目 |
| 步骤级 | [`lit-pyramid`](skills/lit-pyramid/SKILL.md) | 金字塔分层：Classic / Key / Supporting 硬指标 + 对话关系 + 覆盖配额 |
| 步骤级 | [`lit-pdf-zotero`](skills/lit-pdf-zotero/SKILL.md) | 批量 PDF 获取 + Zotero 入库 + 金字塔/PXYV 罗盘可视化 |

#### 03 · 文献分析

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`literature-analysis`](skills/literature-analysis/SKILL.md) | 论文文献综述节的完整流程：模块清单 → 蓝图 → gap → 模块生成 → 初稿组装 |
| 步骤级 | [`knowledge-module-list`](skills/knowledge-module-list/SKILL.md) | 知识模块清单：跨文档分析，每模块带证据假设 + 独立生成 prompt |
| 步骤级 | [`review-blueprint`](skills/review-blueprint/SKILL.md) | 综述蓝图：模块编排成综述逻辑结构 + 可视化 HTML |
| 步骤级 | [`research-gap-scan`](skills/research-gap-scan/SKILL.md) | Research Gap 识别：组合扫描 + 三问反驳防伪 gap |
| 步骤级 | [`knowledge-module-gen`](skills/knowledge-module-gen/SKILL.md) | 知识模块生成：机械抽取 spec + map-reduce 逐篇 + 页码诚实 + 执行日志 |
| 步骤级 | [`critical-paper-reading`](skills/critical-paper-reading/SKILL.md) | 单篇论文批判性阅读（UOW 框架：Description → Analysis → Evaluation + 四维 interrogation），产出结构化批注；组装初稿时深读产物自动并入 Section 2 |
| 步骤级 | [`review-draft-assembly`](skills/review-draft-assembly/SKILL.md) | 论文文献综述节组装：三 Section 组装 + 引用核验 + 反 AI 味 + docx |

#### 04 · 研究设计

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`research-design`](skills/research-design/SKILL.md) | 完整研究设计：方法地图 + 方案 →（你选）→ 初稿 |
| 步骤级 | [`methods-map`](skills/methods-map/SKILL.md) | 方法地图：逐篇扫描方法论 9 字段 + methodology plugin + 2-3 个设计方案 + 可视化 |
| 步骤级 | [`methodology-draft`](skills/methodology-draft/SKILL.md) | 研究设计初稿：段骨架 + 可执行设计清单 + 干净版 Sec 4 方法论 draft |

#### 05 · 数据分析

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`data-analysis-round`](skills/data-analysis-round/SKILL.md) | 跑一轮分析（定量 / 定性 / 自定义 skill），多轮记账不覆盖 |
| 任务级 | [`findings-synthesis`](skills/findings-synthesis/SKILL.md) | 综合发现：全部轮次产出 → 对应 RQ 的研究发现（convergence/divergence） |
| 方法级 | [`analyze-quantitative-data`](skills/analyze-quantitative-data/SKILL.md) | 定量分析全流程（Neuman Ch12，内含 7 个 prompt，见下） |
| 方法级 | [`analyze-qualitative-data`](skills/analyze-qualitative-data/SKILL.md) | 定性分析全流程（Neuman Ch14，内含 11 个 prompt，见下） |

#### 06 · 全文初稿

| 层级 | Skill | 用途 |
|------|-------|------|
| 步骤级 | [`model-paper-deconstruct`](skills/model-paper-deconstruct/SKILL.md) | 拆 Model Paper：动静虚实四产出高密度拆解（≥6000 字） |
| 步骤级 | [`article-framework`](skills/article-framework/SKILL.md) | 反推文章框架：5 Part 骨架 + 引用预算 + 结构对照 + 可视化 |
| 步骤级 | [`fulltext-draft`](skills/fulltext-draft/SKILL.md) | 全文初稿扩写：骨架 → 可打磨的段落散文（管线终点） |

#### 配套 · 数据 Skill 工坊（自己造 skill）

| 层级 | Skill | 用途 |
|------|-------|------|
| 步骤级 | [`skill-workshop-plan`](skills/skill-workshop-plan/SKILL.md) | 规划 + 找料：诊断要不要造、造哪几个 + 下载权威方法学源材料 |
| 步骤级 | [`skill-forge`](skills/skill-forge/SKILL.md) | 源材料 → 成品 skill：5 阶段 2 停点链路（Claude Code / Codex 双平台规范） |

### 工作流二 · 综述文章

把文献本身作为研究材料，完成一篇独立的综述文章。系统、半系统 / 叙事、整合式三型共用检索筛选入口，证据综合与成文按选定类型分流。

#### 01 · 综述选题

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级（复用） | [`topic-workbench`](skills/topic-workbench/SKILL.md) | 尚未定型时的分诊入口：判断文章类型，再转入对应综述选题 skill |
| 步骤级 | [`topic-review-systematic`](skills/topic-review-systematic/SKILL.md) | 综述① 系统综述：三阶段选题教练（窄问题 + 纳入排除 + 检索协议 · PRISMA） |
| 步骤级 | [`topic-review-semisystematic`](skills/topic-review-semisystematic/SKILL.md) | 综述② 半系统/叙事：三阶段选题教练（组织框架 + 研究议程 · RAMESES） |
| 步骤级 | [`topic-review-integrative`](skills/topic-review-integrative/SKILL.md) | 综述③ 整合式：三阶段选题教练（批判性整合 → 新框架/类型学 · Torraco） |

#### 02 · 检索与筛选

| 层级 | Skill | 用途 |
|------|-------|------|
| 任务级 | [`sr-search-record`](skills/sr-search-record/SKILL.md) | 三型通用的检索与筛选：检索式校准 → 抓取去重 → 相关性排序截断 → 题名 / 摘要筛选 → 引文追踪 → Zotero 入库，产出检索记录、纳入排除标准与选择流程数字 |

当前实现采用**摘要层定稿**：筛选阶段不获取全文，也不进行全文合格性评估；综合阶段再获取全文并标注证据级别。系统综述必须如实披露这一流程边界，不能把当前产出称为完整 PRISMA 流程。

#### 03 · 证据综合

| 层级 | Skill | 用途 |
|------|-------|------|
| 方法级 | [`review-synthesis`](skills/review-synthesis/SKILL.md) | 获取纳入文献全文并综合证据：系统型按可比性做 meta-analysis 或 SWiM 综合；半系统型做主题 / meta-narrative 综合；整合式做批判性概念整合，产出研究发现 |

#### 04 · 综述文章初稿

| 层级 | Skill | 用途 |
|------|-------|------|
| 步骤级 | [`review-draft`](skills/review-draft/SKILL.md) | 根据综述类型、研究发现与筛选记录扩写整篇文章，逐条核验引用，生成参考文献表及 Markdown / Word 初稿 |

综述文章和期刊初稿共用一张「文件放哪」表（见 `academic-project-init`）：`选题/综述选题.md` → `文献/检索筛选/`、`文献/PDF/` → `数据/证据综合.md`（+ `数据/综合-*`）→ `写作/综述文章初稿.md`。证据综合使用 `review-synthesis`，成文使用 `review-draft`；期刊初稿中的 `data-analysis-round` 与 `review-draft-assembly` 分别处理单项研究数据和论文文献综述节。

### 工作流三 · 投稿与审稿

面向已有稿件的人文社科作者，可从初稿诊断、投稿准备或收到审稿意见处进入。期刊初稿或综述文章形成初稿后，按当前材料和作者批准范围接入本工作流；进入投稿或返修时无需重跑已完成阶段。

| 阶段 | Skill | 用途 |
|------|-------|------|
| 共用前置 | [`submission-task-intake`](skills/submission-task-intake/SKILL.md) | 核实项目、匿名任务标识、材料版本与作者批准范围，随首个业务阶段完成登记 |
| 01 初稿诊断 | [`manuscript-diagnosis`](skills/manuscript-diagnosis/SKILL.md) | 诊断论证和证据，生成带原文定位、稳定问题 ID、修改建议及作者决定的诊断表 |
| 02 批准范围内改稿 | [`manuscript-revision`](skills/manuscript-revision/SKILL.md) | 仅实施已批准问题，保留逐项修改对照与未完成项，形成待作者确认稿 |
| 03 期刊要求核对 | [`journal-requirements-check`](skills/journal-requirements-check/SKILL.md) | 从指定期刊的实际可读要求形成来源、适用范围、强制 / 建议及差距矩阵 |
| 04 投稿包整理 | [`submission-package-preparation`](skills/submission-package-preparation/SKILL.md) | 依据确认稿、要求矩阵与真实声明事实整理投稿或返修材料，保留格式和实名待补状态 |
| 05 审稿意见与回应决策 | [`review-response-planning`](skills/review-response-planning/SKILL.md) | 保留意见原文，拆分稳定 ID，提出证据需求和回应方案，等待作者逐项决定 |
| 06 返修改稿与逐条回复 | [`review-revision-response`](skills/review-revision-response/SKILL.md) | 先落实获准返修，再据实际修订稿写逐条回复，核对意见、改动、位置与未完成项 |

七个方法和其他 skill 一样全局安装即可：六个业务方法先读取装在同一个 skills 文件夹里的 `submission-task-intake`（论文项目里另有 `skills/submission-task-intake/SKILL.md` 时以项目那份为准），各自还需读取 `references/source-basis.md`；质性初稿诊断另读 `references/qualitative-criteria.md`。

返修经作者确认后回到“期刊要求核对 → 投稿包整理”。产出都在 `写作/投稿/`（项目说明另有约定的以项目为准），文件带 `-R1`、`-R2` 轮次，绝不覆盖；作者批准记录写进 `交接记录-R<n>.md`，AI 不代批；最终投稿与对外发送由作者决定。

来源为 [`ai-submission-review-skills`](https://github.com/qiaomiaojoe/ai-submission-review-skills)，2026-10-15 合入本库；2026-10-16 改成全局可装、落盘统一到 `写作/投稿/`（诊断 1.2.0，其余 1.1.0，方法本体不变）。版本与验证边界见 [投稿与审稿使用说明](docs/workflows/submission-review.md)。

### 后续扩展与归类规则

1. **先定工作流，再列阶段和 skill**：新工作流在 Skills 树中新增一级分支，并说明适用任务、阶段顺序与最终产出。
2. **新增 skill 归入对应阶段**：在所属工作流的阶段表中补充名称、用途与链接，同时更新树和 skill 总数。辅助工具放在所属工作流的“配套”阶段。
3. **跨工作流复用同一份 skill**：可在多条工作流中列出入口，并标注复用；保留同一个源目录，统计时只计一次。
4. **新增独立 skill 库也按工作流登记**：在对应工作流下列出库名、仓库链接、覆盖阶段与安装入口；跨工作流的库分别链接到相关工作流，库内也沿用“工作流 → 阶段 → skill”的导航。
5. **导航与安装路径分开维护**：工作流分类体现在 README；本库继续使用 `skills/<name>/`，保持已有链接和安装方式可用。其他库的 skills 单独标注数量，本库总数只统计本库实际收录的目录。

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

只想要某几个 skill？拷对应完整目录，并保留其 `references/` 等支持文件。**投稿与审稿的六个业务方法还依赖 `submission-task-intake`，要一起装。**

### 依赖与降级（装了哪些外部工具，效果才完整）

本库只放方法。检索数据库、下载 PDF、读写 Zotero、转 Word 用的是下面这些**不在本库里**的工具，要另装。都没装时每个 skill 照样能跑，只是按下表降级，而且会在结果里说明哪一步降级了，**不会编造检索结果或文献**。用 POPPER · AI学术工作站的学员，在「AI学术环境配置」里逐项点安装即可。

| 外部工具 | 从哪装 | 用到它的 skill | 没装时会怎样 |
|---|---|---|---|
| 数据库检索 skills：`cnki-*`（中国知网）、`wos-*`（Web of Science）、`sd-*`（ScienceDirect）、`gs-*`（Google Scholar） | [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills)、[wos-skills](https://github.com/cookjohn/wos-skills)、[sd-skills](https://github.com/cookjohn/sd-skills)、[gs-skills](https://github.com/cookjohn/gs-skills)；要配 Chrome DevTools MCP，在浏览器里登录（知网下载、WoS 和 ScienceDirect 要用机构账号） | `pxyv-search`、`lit-verify`、`lit-pdf-zotero` | `pxyv-search` 跳过没装的库并告诉你，一个都没有时只给各维度检索词，由你手动去搜；`lit-verify` 改走 doi.org / Crossref / OpenAlex，还查不了的给每条的手动核查链接，不凭印象判真假；中文条目没有知网 skill 就没法自动核对 |
| scansci-pdf（PDF 下载 MCP 服务） | [Rimagination/scansci-pdf](https://github.com/Rimagination/scansci-pdf)，要 Python 3.11 以上 | `review-synthesis`、`skill-workshop-plan`，以及 `lit-pdf-zotero` 的下载渠道 | 只从开放获取渠道找全文；`review-synthesis` 拿不到全文的研究按「仅摘要」降级表述，**不会因此把它踢出纳入集**；`skill-workshop-plan` 给手动获取方式 |
| Zotero 服务（zotero-mcp） | [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)，服务名要叫 `zotero`；本地模式只能读，要入库还得配 Zotero 网页版的 API key | `lit-pdf-zotero`、`sr-search-record`、`knowledge-module-list`、`knowledge-module-gen`、`critical-paper-reading`、`model-paper-deconstruct`、`review-synthesis`、`review-draft`、`review-draft-assembly` | `lit-pdf-zotero` 只落盘 PDF 和 `文献清单.md`，告诉你怎么手动导入；`sr-search-record` 改导出 RIS / BibTeX；文献分析类改读本地 PDF 或文献清单；引用核验改对照文献清单 |
| OpenAlex API key（免费）+ Python 3 | [openalex.org](https://openalex.org/) 申请；写进环境变量 `OPENALEX_API_KEY` 或文件 `~/.config/openalex/api_key` | `sr-search-record`（自带脚本 `scripts/oa_search.py`） | 没有 key 只抓得到每个检索式的第一页（100 条），照样往下走，写进 `降级记录.md`，PRISMA 数字标「待有 key 后完整抓取」；没有 Python 3 脚本跑不了 |
| pandoc | [pandoc.org](https://pandoc.org/installing.html) | `review-draft`、`review-draft-assembly`（转 .docx） | skill 里没写替代办法：只拿得到 .md 初稿，.docx 等装好后再转 |
| skill-creator | Claude Code 用官方的 `skill-creator` skill；Codex 用自带的 skill-creator（`init_skill.py`） | `skill-forge` | skill 里没写替代办法，造 skill 那一步做不了 |
| MinerU 文字稿（可选） | POPPER「读文献」里的 MinerU 工具，把 PDF 转成 `文献/全文/<同名>.md` | 读全文的 skill（`knowledge-module-gen`、`critical-paper-reading`、`model-paper-deconstruct`、`review-synthesis`、`methods-map`、投稿与审稿 7 个等） | 直接读 PDF |

装好后可以先用一句话试试工具通没通，比如「用 cnki-search 搜一下『数字劳动』，只列前 3 条」「用 zotero 服务列出我的文献集合」。

维护者：`python3 scripts/validate_skills.py` 会列出各 skill 引用了哪些本库没有的 skill。新增依赖时同步更新这张表和脚本里的 `EXTERNAL_SKILL_PREFIXES`。

### 触发例句（装好后直接说）

- "帮我选题，我想研究……" → `topic-workbench` 分诊 → 对应选题模式
- "把我的选题拆成 PXYV" → `topic-pxyv-parse`
- "检查这些参考文献是不是编的" → `lit-verify`
- "把这批文献做金字塔分层" → `lit-pyramid`
- "帮我找这个方向的 research gap" → `research-gap-scan`
- "我要分析这份调查数据" → `analyze-quantitative-data`；"帮我编码这些访谈" → `analyze-qualitative-data`
- "批判性阅读这篇 paper" / "评一下这篇文章" → `critical-paper-reading`
- "拆这篇 model paper" → `model-paper-deconstruct`
- "把这本教科书 PDF 做成 skill" → `skill-forge`
- "为我的研究论文搜文献入 Zotero"（完整任务）→ `literature-search`；"写论文中的文献综述节" → `literature-analysis`
- "我要写一篇独立综述文章，先帮我选型" → `topic-workbench` → 对应 `topic-review-*`
- "跑综述的文献检索和筛选" → `sr-search-record`
- "综合我的综述语料库" → `review-synthesis`；"写综述文章初稿" → `review-draft`
- "诊断这份初稿，保留我的核心观点" → `manuscript-diagnosis`；"按我批准的问题清单改稿" → `manuscript-revision`
- "核对目标期刊要求并整理投稿材料" → `journal-requirements-check` → 确认要求后 `submission-package-preparation`
- "拆解审稿意见，先给我回应方案" → `review-response-planning`；"按已确认意见返修并写逐条回复" → `review-revision-response`

---

## Skills 设计原则

1. **按任务调用**：期刊初稿与综述文章的步骤按各自最小输入独立运行；投稿与审稿六个业务方法先执行共用材料核实，缺少必要输入或批准时按其规则局部停止。
2. **按工作流交接**：三条工作流都按项目的「文件放哪」表落盘（选题/ 文献/ 方法/ 数据/ 写作/，投稿与审稿在 `写作/投稿/`）。跨工作流显式核实输入路径、材料版本与作者确认范围，沿用各方法的交接约定。
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

[CC BY-NC 4.0](LICENSE)（署名—非商业性使用）© 乔淼（乔淼PhD），2026-10-19 起。

- ✅ 任何人都可以使用、分享和改编这些 skills
- ✅ 使用、分享或改编时注明出自「乔淼PhD · AI学术训练营」，并附上本仓库链接
- ❌ 不得用于商业用途（付费课程 / 培训 / 咨询 / 付费社群 / 盈利性产品与服务）
- 「乔淼PhD」「AI学术训练营」「POPPER」等名称和标识不在许可范围内

配套的桌面软件 **POPPER · AI学术工作站**：[下载](https://github.com/qiaomiaojoe/ai-academic-app)。商业合作与授权咨询：微信公众号「乔淼PhD」。完整条款见 [LICENSE](LICENSE)。
