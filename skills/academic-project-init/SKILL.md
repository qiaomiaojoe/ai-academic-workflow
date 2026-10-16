---
name: academic-project-init
description: AI 学术研究项目初始化（乔淼PhD · AI学术训练营 · AI学术工作流）。为一篇论文写项目说明 AGENTS.md（含「文件放哪」表：选题/ 文献/（PDF/、知识模块/）方法/ 数据/ 写作/ skill源材料/）+ CLAUDE.md 指针。文件夹用到才建，不预建空文件夹。初始化后，选题/文献搜索/文献分析/研究设计/数据分析/全文初稿等 skills 都按这张表读写、互相衔接；和「AI学术工作站」新建项目的结构完全一致。Trigger on："初始化一个学术项目"、"新建论文项目文件夹"、"建一个 AI 学术工作流项目"、"set up an academic paper project"、"initialize research project folder"。
---

# Academic Project Init · 项目说明 + 文件放哪

为一个 AI 学术研究项目初始化工作目录（一个项目 = 一篇要完成的论文）。

> 这个 skill 是项目脚手架：唯一负责"文件放哪"的约定，写进项目 AGENTS.md。其余各 work skill 不写死文件夹——在项目里运行时按 AGENTS.md 的「文件放哪」表归档，独立运行时产出到当前工作目录。表和「AI学术工作站」新建项目时写的那张一模一样，工作站的工作流、工具和这些 skill 共用。

## 输入

- 项目名称（必填）
- 产出语言（必填，问一次）：中文 / 英文 / 中英双语
- 位置：默认在当前工作目录下新建 `项目名/`。若当前目录看起来不像存放论文项目的工作根目录（例如是系统主目录或另一个项目内部），先向用户确认再创建。用户也可给绝对路径。

## 任务 1 · 写 AGENTS.md（已存在则保留原有内容，只在末尾补「文件放哪」一节；已有旧的 01_选题 … 命名表就不补，照旧用它）

```markdown
# 项目说明（AI 每次开工都会先读这份）

- 项目：[项目名]
- 产出语言：[语言]
- 关联的 Zotero 集合：（还没有）

## 我的规矩
- 引用只用真实存在、能核对的文献
- （在这里补充你自己的要求，比如写作风格、目标期刊）

## 文件放哪
（工作流、工具、直接跟 AI 说，都按这张表放。用到才建文件夹，不要另建别的子文件夹；同名文件已存在时先问，或加日期后缀。）

| 放什么 | 放哪 |
|---|---|
| 选题（选题.md；综述文章是 综述选题.md） | 选题/ |
| 文献清单、检索候选、验真报告、金字塔分层、入库报告、文献可视化 | 文献/ |
| 文献 PDF（命名 AuthorYear.pdf） | 文献/PDF/ |
| 综述文章的检索筛选记录（检索配置、全量记录、筛选台账、纳入排除标准、选择流程、待复核清单、验真 / 降级记录） | 文献/检索筛选/ |
| 知识模块清单、综述蓝图、Gap、综述初稿（含 .docx）、引用核验报告、单篇深读（深读-AuthorYear.md） | 文献/ |
| 知识模块 M1…Mn、模块执行日志 | 文献/知识模块/ |
| 方法地图、研究设计初稿、设计说明 | 方法/ |
| 原始数据、每轮分析产出、分析日志、研究发现（综述文章：证据综合.md、综合抽取表、各型综合产出） | 数据/ |
| Model Paper 拆解、文章框架、全文初稿、综述文章初稿（含 .docx、引用核验报告） | 写作/ |
| 投稿与返修：任务登记、交接记录、修改诊断、修订稿、修改对照、期刊要求矩阵、投稿包、审稿意见台账、返修稿、审稿回复（都带 -R1、-R2 轮次）、投稿分析日志 | 写作/投稿/ |
| 数据 skill 工坊的源材料 | skill源材料/ |
```

## 任务 2 · 写 CLAUDE.md（已存在则跳过）

写入一行：`见 [AGENTS.md](AGENTS.md)。`

## 任务 3 · 确认

**不要预建空文件夹**：哪一步第一次往哪写，才建那个文件夹。创建完成后列出项目根目录确认（只有 AGENTS.md、CLAUDE.md）。

## 各阶段读写约定（skill 在项目里运行时按此找上一步的产出）

| 阶段 | skill | 读 | 写 |
|---|---|---|---|
| 选题 | topic-*（四种研究性文章模式）/ topic-pxyv-parse | — | 选题/选题.md（顶部 workbench 锚块） |
| 文献搜索 | literature-search（pxyv-search → lit-verify → lit-pyramid → lit-pdf-zotero） | 选题/选题.md | 文献/文献清单.md、文献/PDF/、Zotero 集合 |
| 文献分析 | literature-analysis（knowledge-module-list → review-blueprint → research-gap-scan → knowledge-module-gen →（可选 critical-paper-reading）→ review-draft-assembly） | 选题/、文献/ | 文献/知识模块清单.md、综述蓝图.md/.html、知识模块/M*.md、深读-*.md、综述初稿.md、引用核验报告.md |
| 研究设计 | research-design（methods-map → methodology-draft） | 选题/、文献/ | 方法/方法地图.md/.html、研究设计初稿.md、研究设计-设计说明.md |
| 数据分析 | data-analysis-round（多轮）→ findings-synthesis | 方法/、数据/ | 数据/（每轮带前缀不覆盖）+ 分析日志.md → 研究发现.md |
| 全文初稿 | model-paper-deconstruct → article-framework → fulltext-draft | 选题/、文献/、方法/、数据/ | 写作/Model-Paper-拆解-*.md、文章框架.md、全文初稿.md |
| 综述文章（独立成篇的综述） | topic-review-{systematic,semisystematic,integrative} → sr-search-record → review-synthesis → review-draft | 选题/综述选题.md、文献/检索筛选/、数据/证据综合.md | 选题/综述选题.md、文献/检索筛选/、文献/PDF/、数据/证据综合.md + 数据/综合-*、写作/综述文章初稿.md |
| 投稿与返修 | submission-task-intake +（manuscript-diagnosis → manuscript-revision → journal-requirements-check → submission-package-preparation；返修：review-response-planning → review-revision-response → 再回期刊要求核对、投稿包） | 写作/（全文初稿或你自己的稿件）、写作/投稿/ | 写作/投稿/（-R<n> 轮次不覆盖，分析日志.md） |
| 数据 skill 工坊 | skill-workshop-plan → skill-forge | 方法/ | skill源材料/；skill 成品落 ~/.claude/skills/ 或 ~/.codex/skills/（项目外） |

- 文献全文默认读 文献/PDF/ 下的本地 PDF，也可走 Zotero。
- 旧项目（01_选题 / 02_文献 / … 那套）不搬文件，照旧按它自己的命名表；综述文章的老项目在项目说明里约定了 `RV_综述/` 的，照旧按 `RV_综述/`。
- 综述文章的选题、综合特意不叫 选题.md / 研究发现.md，免得和写论文的产出撞名。
- 不编造文献；缺失的引用用 [TBD-citation] 占位、缺失信息用 [待补] 占位。
