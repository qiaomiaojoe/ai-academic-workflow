---
name: literature-analysis
description: 文献分析/综述 skill（源自 AI学术工作台 03 文献分析工作流，单品化）。三步骤产出文献综述：步骤 1 跨文档分析（综述蓝图 + 知识模块清单 + gap 组合扫描 + 可视化）→ 步骤 2 知识模块生成（map-reduce 逐篇、页码诚实、执行日志）→ 步骤 3 综述初稿组装（引用核验 + 反 AI 味 + 参考文献表 + docx）。文献来源支持 Zotero 集合 / 本地 PDF 文件夹 / 文献清单，任选其一即可，不依赖上一阶段。Trigger on："帮我做文献综述"、"跨文档分析"、"生成知识模块"、"组装综述初稿"、"文献分析步骤1/2/3"、"literature review from my Zotero collection"、"synthesize these PDFs into a review"。
---

# Literature Analysis · 综述蓝图 → 知识模块 → 综述初稿

三步骤工作流，每步一个独立可跑的协议（详见 references/）。用户可从任何一步进入，只要该步的输入齐了。

## 单品调用约定（输入解耦）

**选题 context（三步共用）**，按优先级：
1. 用户直接给的 RQ / PXYV / 研究定位一句话；
2. 项目内 `01_选题/选题.md`（含 PXYV + RQ + 5 近邻）；
3. 都没有 → 请用户用 1-3 句话说清：研究问题 + 理论视角 + 现象/语境。不要因缺选题文件拒跑。

**文献数据源（三选一，用户指定或自动探测）**：
- Zotero 集合（用户给集合名；用 `zotero_get_collection_items` / `zotero_get_item_metadata` / `zotero_get_item_fulltext`）
- 本地 PDF 文件夹（项目内默认 `02_文献/pdf_download/`，或用户给任意文件夹路径；AuthorYear.pdf 命名最佳，页码最可靠）
- 文献清单 markdown（项目内默认 `02_文献/文献清单.md`，或用户粘贴清单）作为元数据兜底
数据源降级时在产出顶部注明"数据源已降级"。

**主数据通道**（步骤 1/2 需要，问用户或按可用性选）：
- Zotero MCP 直接读原文（默认）
- NotebookLM MCP（严格 citation 验证 / 全文长）：add_notebook 建 notebook → 提示用户上传该模块文献 PDF 并注册 share URL → ask_question 喂入模块生成 prompt，保存 session_id
- 本地 PDF 直读（页码最可靠）：按 AuthorYear.pdf 定位，按页读取

**输出落盘降级**：在项目里 → 按命名表写 `02_文献/`（综述蓝图.md / 知识模块清单.md / 综述蓝图.html / 模块/M_n.md / 执行日志.md / 综述初稿.md / 引用核验报告.md）；不在项目里 → 当前目录建 `./文献分析/` 同名文件。

**引用格式**：默认 APA 7th，用户可指定。**产出语言**：项目 CLAUDE.md 或用户指定；中英双语 = 先英文 draft 再中文译稿，两稿都要 inline citation。

**工具适配**：Zotero / NotebookLM 等以环境实际可用为准，不可用时明确说并走降级通道，不要编造工具结果。

## 三个步骤

| 步骤 | 输入前置 | 产出 | 协议文件 |
|------|---------|------|---------|
| 1 跨文档分析 | 选题 context + 文献数据源 | 知识模块清单.md + 综述蓝图.md（含 Section 3 gap）+ 综述蓝图.html（自动打开） | `references/step1-综述蓝图.md` |
| 2 知识模块生成 | 知识模块清单.md（无则先跑步骤 1） | 模块/M1.md … M_n.md + 执行日志.md | `references/step2-知识模块.md` |
| （可选）单篇深读 | Classic / 关键 Key 的 PDF 或 Zotero key | 深读/深读-AuthorYear.md | 调用 `critical-paper-reading` skill（UOW 框架：Description / Analysis / Evaluation），产物放 深读/ 下，步骤 3 自动并入 Section 2 |
| 3 综述初稿组装 | 综述蓝图.md + 模块/*.md（+ 可选深读产物） | 综述初稿.md（+ 双语时 -zh.md）+ 同名 .docx + 引用核验报告.md | `references/step3-综述初稿.md` |

判断用户要跑哪一步（明说步骤号，或按已有产物推断），读对应 references 文件后执行。

单篇深读推荐顺序（按性价比）：⭐⭐⭐ Classic 1 篇（理论根基）→ ⭐⭐ 与 RQ 概念正面对话的 Key 1 篇（概念近邻区分）→ ⭐⭐ 与方法/经验维度正面对话的 Key 1 篇（经验机制）→ ⭐ 同框架同方法的对话伙伴（张力来源）。不跑也能走完流程；跑完会让步骤 3 的 Section 2 显著更扎实。
