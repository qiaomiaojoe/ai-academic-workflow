---
name: literature-analysis
description: 文献分析/综述完整任务入口（乔淼PhD · AI学术训练营 · AI学术工作流）。编排步骤 skill 跑完一次完整的文献综述：knowledge-module-list 模块清单 → review-blueprint 综述蓝图 → research-gap-scan gap 识别 → knowledge-module-gen 模块生成 →（可选 critical-paper-reading 深读）→ review-draft-assembly 综述初稿。只要单独某一步（只列模块/只找 gap/只组装）时直接用对应步骤 skill。Trigger on："帮我做文献综述"、"文献分析工作流"、"从我的 Zotero 集合跑出综述初稿"、"literature review from my collection"。
---

# Literature Analysis · 文献综述任务编排

一次完整的文献综述 = 步骤 skills 按序执行：

| 步骤 | 调用 skill | 产出 |
|------|-----------|------|
| 1a 模块清单 | `knowledge-module-list` | 知识模块清单.md |
| 1b 综述蓝图 | `review-blueprint` | 综述蓝图.md + .html |
| 1c Gap 识别 | `research-gap-scan` | 蓝图 Section 3（gap + 定位） |
| 2 模块生成 | `knowledge-module-gen` | 模块/M1-Mn.md + 执行日志.md |
| （可选）单篇深读 | `critical-paper-reading` | 深读/深读-AuthorYear.md（组装时自动并入 Section 2） |
| 3 初稿组装 | `review-draft-assembly` | 综述初稿.md + .docx + 引用核验报告.md |

## 编排规则

- 开工前一次问齐：选题 context（RQ/PXYV 一句话或 `选题.md`）、文献数据源（Zotero 集合 / 本地 PDF 文件夹 / 文献清单，三选一）、主数据通道（Zotero / NotebookLM / 本地 PDF）、总字数目标、引用格式、输出语言。
- 1a→1b→1c 连续跑完后停一次给用户看蓝图；2 全程不打断（靠执行日志把关）；3 之前问一次是否做单篇深读。
- 各步骤严格按对应 skill 协议执行；步骤 skill 不可用时读其 SKILL.md 内联执行。
- 单篇深读推荐顺序（按性价比）：⭐⭐⭐ Classic 1 篇（理论根基）→ ⭐⭐ 与 RQ 概念正面对话的 Key（概念近邻区分）→ ⭐⭐ 与方法/经验维度正面对话的 Key（经验机制）→ ⭐ 同框架同方法的对话伙伴（张力来源）。不跑也能走完流程。
