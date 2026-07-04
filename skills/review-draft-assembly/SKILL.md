---
name: review-draft-assembly
description: 综述初稿组装（乔淼PhD · AI学术训练营 · AI学术工作流 · 文献分析步骤）。按综述蓝图把知识模块组装成综述初稿：三 Section 组装规则 + 深读张力句并入 + 逐条引用核验（对照 Zotero/清单出独立报告）+ 参考文献表 + 反 AI 味写作要求 + 初稿纯净交付（零模块编号零 Zotero key）+ 转 docx。Trigger on："组装综述初稿"、"把模块拼成综述"、"综述成稿"、"assemble my literature review draft"。
---

# Review Draft Assembly · 综述初稿组装

## 调用约定（独立运行）

- 输入：综述蓝图（`02_文献/综述蓝图.md`，必需）+ 模块产出（`02_文献/模块/M*.md`，必需）+ 可选深读产物（`02_文献/深读/深读-*.md`）。缺必需项 → 指路先跑 `review-blueprint` / `knowledge-module-gen`。
- 参数：总字数目标（可选）、引用格式（默认 APA 7th）、输出语言（项目 CLAUDE.md 或用户指定；中英双语 = 先英文 draft 再中文译稿，两稿都要 inline citation）。
- 落盘：项目内 `02_文献/综述初稿.md`（+ 双语 `-zh.md`）+ 同名 .docx + `02_文献/引用核验报告.md`；项目外当前目录同名。

前置：
- 综述蓝图.md（必需 · 含框架 + 模块映射 + Section 3 gap）
- 模块/M1.md … M_n.md（必需）
- 深读/深读-*.md（可选，若存在自动并入 Section 2）

按「综述蓝图.md」指定的逻辑结构组装综述初稿。

## 【字数分配】

- 用户给了总字数目标 → 按 Section 1 ~40% · Section 2 ~40% · Section 3 ~20% 分配（可微调）。
- 未给 → Section 1 ≈ 200-400 字 · Section 2 ≈ 200-400 字 · Section 3 ≈ 100-200 字。
- 字数是目标上限，证据不足时宁缺毋滥，不灌水。

## 【Section 1 · XY 经验段】

- 按蓝图 Section 1 的模块出场顺序整合
- 开头：用蓝图 Section 1 核心 argument 引入
- 主体：依次穿插各模块 output 的核心 finding（含 inline citation）
- 张力：模块间的分歧或竞争立场
- 收尾：1 句连接到 Section 2

## 【Section 2 · PV 理论段】

- 按蓝图 Section 2 的模块论证顺序组装
- 开头：蓝图 Section 2 核心 argument
- 主体：理论谱系 + 框架继承/冲突
- 若存在「深读-*.md」：把深读关键论点作为张力句嵌入主体
- 收尾：1 句指向 Section 3 的 gap

## 【Section 3 · Gap & 定位段】

- 按蓝图 Section 3 组装
- 显式陈述本研究 RQ 如何回应 gap
- 收尾：1 句宣告本研究的贡献

## 【引用核实（对照 Zotero 库 / 文献清单）】

初稿写完后，逐条核对 inline citation：用 zotero_search_items / zotero_get_item_metadata 确认每条引用的 Author/Year 真实存在于集合、拼写与年份无误（Zotero 不可用时对照文献清单/本地 PDF 文件名核对）。
产出一份独立的「引用核验报告.md」（不进初稿）：每条引用 → 是否在库 → 有无出入。
未能核实的引用，在初稿顶部"交付说明"里点名。

## 【参考文献表】

按用户指定引用格式（默认 APA 7th），在初稿正文末尾生成"参考文献"表，覆盖正文所有 inline citation。

## 【写作要求 · 反 AI 味（内联，不调用外部 skill）】

- 去掉空洞过渡词，禁用"值得注意的是 / 综上所述 / 不仅……而且"这类套话。
- 句长要有变化，不要每句同一节奏。
- 具体优于抽象：能给机制 / 数字 / 对象就不要泛泛而谈。
- 陈述性学术语气，不堆形容词。

## 【交付要求 · 初稿纯净】

- 正文零备注：不出现模块编号 M_n、Zotero key、生成过程说明。
- 必要的风险提示集中放在文档最顶部一个"⚠️ 交付说明"区块，仅限：数据源是否降级、哪个 Section 证据偏薄、未能核实的引用、缺页码的引用。除此之外正文是干净综述。
- inline citation 格式 (Author Year, p.X)。
- 输出语言按约定（中英双语 = 先英文 draft `综述初稿.md`，再中文译稿 `综述初稿-zh.md`，两稿都要 inline citation）。
- 中间产物（蓝图 / 模块）语言应与本初稿主语言一致；若不一致，先整体对齐再写，不要逐句机翻。

## 【另存 Word】

md 初稿完成后，再转一份 .docx（用 pandoc 或 docx 能力，保留参考文献表与引用格式），与 md 同目录。中英双语项目：两份 md → 各转一份 docx。
