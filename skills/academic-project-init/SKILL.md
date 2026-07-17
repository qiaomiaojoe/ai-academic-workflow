---
name: academic-project-init
description: AI 学术研究项目初始化（乔淼PhD · AI学术训练营 · AI学术工作流）。为一篇论文建标准项目结构：01_选题 / 02_文献（pdf_download·模块·深读）/ 03_方法 / 04_数据 / 05_全文初稿 / 06_skill源材料 + CLAUDE.md（命名规则与产出位置总表）+ AGENTS.md。初始化后，选题/文献搜索/文献分析/研究设计/数据分析/全文初稿等 skills 都能按命名表自动读写、互相衔接。Trigger on："初始化一个学术项目"、"新建论文项目文件夹"、"建一个 AI 学术工作流项目"、"set up an academic paper project"、"initialize research project folder"。
---

# Academic Project Init · 项目文件夹 + CLAUDE.md + AGENTS.md

为一个 AI 学术研究项目初始化工作目录（一个项目 = 一篇要完成的论文）。

> 这个 skill 是「AI 学术工作台」的项目脚手架——它是唯一负责"文件夹落位"的 skill，把命名表写进项目 CLAUDE.md。其余各 work skill 本身不写死文件夹，标准做法是：在这个结构里运行时按本表归档，独立运行时产出到当前工作目录。

## 输入

- 项目名称（必填）
- 产出语言（必填，问一次）：英文 / 中文 / 中英对照
- 位置：默认在当前工作目录下新建 `项目名/`。若当前目录看起来不像存放论文项目的工作根目录（例如是系统主目录或另一个项目内部），先向用户确认再创建。用户也可给绝对路径。

## 任务 1 · 建目录结构（已存在则跳过，不要覆盖已有文件）

```
项目名/
├── CLAUDE.md
├── AGENTS.md
├── 01_选题/
├── 02_文献/
│   ├── pdf_download/
│   ├── 模块/
│   └── 深读/
├── 03_方法/
├── 04_数据/
├── 05_全文初稿/
└── 06_skill源材料/
```

## 任务 2 · 写 CLAUDE.md（若已存在，保留用户原有内容，仅补齐缺失小节）

```markdown
# [项目名] · AI 学术研究项目

## 项目元信息
- 项目根目录：[路径]
- Zotero 顶层集合：[项目名]
- 产出语言：[语言]

## 命名规则与产出位置（各阶段读写约定 · 优先按路径读上一阶段产出）
| 阶段 | 产出文件 |
|------|----------|
| 01 选题（topic-workbench 分诊 → topic-theory-interpretation / topic-hypothesis-testing / topic-concept-construction / topic-method-driven；综述选题走 topic-review-systematic / topic-review-semisystematic / topic-review-integrative 三型；已有选题用 topic-pxyv-parse）| 01_选题/选题.md（顶部含 workbench 锚块：mode / title / PXYV / RQ / neighbors）；中间产物 选题-A-mining.md / 选题-B-calibration.md（断点续跑用）|
| 2A 文献搜索（literature-search 编排：pxyv-search → lit-verify → lit-pyramid → lit-pdf-zotero）| 02_文献/文献清单.md + 02_文献/pdf_download/（AuthorYear.pdf）+ Zotero 集合入库 |
| 2B 文献分析 · 步骤 1（knowledge-module-list + review-blueprint + research-gap-scan）| 02_文献/知识模块清单.md、02_文献/综述蓝图.md（含 Section 3 gap）、02_文献/综述蓝图.html |
| 2B 文献分析 · 步骤 2（knowledge-module-gen）| 02_文献/模块/M1.md … M_n.md + 02_文献/执行日志.md |
| 2B 文献分析 · 可选深读 | 02_文献/深读/深读-AuthorYear.md |
| 2B 文献分析 · 步骤 3（review-draft-assembly）| 02_文献/综述初稿.md + 同名 .docx（双语项目另加 综述初稿-zh.md）+ 02_文献/引用核验报告.md |
| 03 研究设计 · 阶段A（methods-map）| 02_文献/方法地图.md（含内嵌 methodology_plugin YAML + 2-3 方案）、02_文献/方法地图.html |
| 03 研究设计 · 阶段B（methodology-draft）| 03_方法/研究设计初稿.md（干净 Sec 4 初稿）、03_方法/研究设计-设计说明.md |
| 04 数据分析（data-analysis-round）| 04_数据/：每轮产出带 skill 前缀（quant-* / qual-* / <skill>-*，多轮不覆盖）+ 分析日志.md（逐轮记账）→ 研究发现.md（综合发现 · 由 findings-synthesis 整合全部轮次生成）；RQ / 变量 / 度量层级 / 颗粒度默认从 03_方法/研究设计初稿.md + 研究设计-设计说明.md 读取 |
| S 数据 Skill 工坊（skill-workshop-plan → skill-forge）| 06_skill源材料/（权威源材料 + 源材料清单.md）；skill 成品落 ~/.claude/skills/（独立于本项目，跨项目复用）|
| 05 全文初稿 · Step 1（model-paper-deconstruct）| 05_全文初稿/Model-Paper-拆解-[AuthorYear].md |
| 05 全文初稿 · Step 2（article-framework 反推框架 → fulltext-draft 扩写 · 管线终点）| 05_全文初稿/文章框架.md、05_全文初稿/文章框架-part2.html、05_全文初稿/全文初稿.md |

（以上均为项目内相对路径。工作流编号与文件夹编号现已对齐：01 选题→01_选题、02 文献→02_文献、03 研究设计→03_方法、04 数据分析→04_数据、05 全文初稿→05_全文初稿。三点说明——① 文献阶段拆成 2A 文献搜索 / 2B 文献分析两个工作流，均写入 02_文献/；② 03 研究设计的阶段A 方法地图也落 02_文献/，阶段B 研究设计初稿才落 03_方法/；③ 数据 Skill 工坊（S）用 06_skill源材料/ 造 skill，成品落项目外的 ~/.claude/skills/。综述性论文的"分析"走 04 数据分析、跳过 2B。）

- 文献 PDF 一律下载/存放到 02_文献/pdf_download/（命名 AuthorYear.pdf）。当 Zotero / NotebookLM 无法调用时，分析文献全文可直接读取 pdf_download/ 下的本地 PDF。

## 工作流原则
- 每个阶段先按上表路径读取上一阶段产出，再产出本阶段文件。
- 不编造文献；缺失的引用用 [TBD-citation] 占位、缺失信息用 [待补] 占位。
```

## 任务 2.5 · 写 AGENTS.md（已存在则跳过）

写入一行：`本项目约定（命名规则 / 产出位置 / Zotero 集合 / 产出语言）见同目录 CLAUDE.md —— 开始任何任务前先完整读取它。`

## 任务 3 · 确认

创建完成后，用环境可用的命令（tree / ls -R / Get-ChildItem -Recurse）列出项目目录结构确认。
