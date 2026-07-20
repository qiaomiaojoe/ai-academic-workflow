---
name: knowledge-module-gen
description: 知识模块生成（乔淼PhD · AI学术训练营 · AI学术工作流 · 文献分析步骤）。按知识模块清单逐模块读全文生成 M_n.md：机械抽取模块 prompt（不改写不补全）、flag 而非 ask、map-reduce 逐篇防爆上下文、页码诚实、每模块一行执行日志自检；支持 Zotero / NotebookLM / 本地 PDF 三种数据通道。Trigger on："生成知识模块"、"按模块清单跑模块"、"逐模块读全文写 M1-Mn"、"generate knowledge modules from my module list"。
---

# Knowledge Module Gen · 知识模块生成

## 调用约定（独立运行）

- 输入：知识模块清单（`知识模块清单.md`，或用户给的路径；没有 → 先跑 `knowledge-module-list`）+ 主数据通道（Zotero MCP / NotebookLM / 本地 PDF，问用户或按可用性选）。
- 落盘：`模块/M_n.md` + `执行日志.md`（默认当前工作目录）。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。
- 工具适配：以环境实际可用为准，不可用时走降级通道并注明，不编造工具结果。

前置：已有 知识模块清单.md（步骤 1 Part A 产物）。若没有，先跑步骤 1。

按用户所选主数据通道执行（Zotero / NotebookLM / 本地 PDF；个别模块可在执行时覆盖：文献量大 / 要严格 citation 验证 → 改用 NotebookLM；MCP 不可用 → 改用本地 PDF）。

## 【准确拾取并执行模块 prompt】（防 AI 自由发挥 · 全程不打断）

不需要逐模块回显让用户确认。用三件套保证准确：

1. **机械抽取**（拾取靠切片，不靠理解）：从 知识模块清单.md 中定位"## 模块 M_n"标题，逐字抽取其下代码围栏内的文本，当作字面 spec。不改写、不补全、不重排关键问题与期望输出结构。
2. **flag 而非 ask**（执行忠实，想改只标记，不停下来问）：照原样跑。若认为某处该调整，不要调整——在该模块输出里加一行 `_deviation: 想改什么 + 为什么`，然后仍按原 prompt 执行。
3. **结尾自检日志**（把关靠一份日志，不靠过程确认）：每跑完一个模块，往 执行日志.md 追加一行：`M_n | 用的 prompt 首行 | 结构符合期望(✓/✗) | 证据假设对上(✓/✗) | 有无 _deviation`。全部跑完后用户只看这一份日志，有 ✗ 或 _deviation 的模块才回看。

## 主数据通道分支

- **Zotero MCP**：对该模块每篇文献调 zotero_get_item_fulltext 取全文（或 zotero_get_item_metadata 取摘要；工具名以环境实际注册为准），按下方 map-reduce 逐篇抽取，不要一次性拼接全部全文。
- **NotebookLM MCP**：add_notebook 建新 notebook；提示用户把该模块文献 PDF 上传并粘贴 share URL 注册到 MCP。用 ask_question 喂入该模块的「生成 prompt」，保存 session_id 以便追问。收到返回 → 验证 inline citation → 保存为 M_n.md。（NotebookLM 自身检索已控上下文，map-reduce 主要用于另两种模式。）
- **本地 PDF 直读**：在 pdf_download/（或用户给的文件夹）下按 AuthorYear.pdf 找到本地 PDF，按页读取，逐篇抽取（本地 PDF 天然有页码，引用页码以此为准）。找不到对应 PDF 的文献回退 Zotero 或 NotebookLM。

## 【上下文管理 · map-reduce 逐篇】

注意：map-reduce 不是 Claude Code / Codex 的内置功能，必须显式照做，否则会一次性把全文塞满上下文。对一个模块涉及的多篇文献：
1. map：一篇一篇处理——读第 1 篇 → 抽取与"关键问题"相关的段落（每段记页码）写成中间笔记 → 不保留全文 → 读第 2 篇……
2. reduce：全部读完后，只基于中间笔记 + 证据摘录写该模块，不回头重读全文。

这样既不爆上下文，也避免"lost in the middle"。

## 【页码诚实】

- 优先用能给页码的来源（本地 PDF 按页读，页码最准）。
- Zotero fulltext 若不含页码 → 回退本地 PDF；都拿不到就标注 (Author Year)，不要编造页码。

## 【字数与结构】

- 单模块 ≈500 词英文 / 800 字中文。
- 结构配额：概念/操作化 ~20% · 核心 findings ~50% · 对综述 Section 的贡献 ~30%。
- 证据不足以支撑字数时，标注"该模块证据偏薄"，不灌水重复。

## 【双层产物】

- M_n.md 是工作层，可以"脏"：正文之外附"证据摘录"区（原文 quote + 页码 + Zotero key），供步骤 3 溯源。
- 步骤 3 的综述初稿才要纯净——溯源信息不进初稿。

## 输出

每个模块一个独立 .md，统一写到 模块/ 目录：M1.md, M2.md, ..., M_n.md；外加一份 执行日志.md（每模块一行自检）。

执行顺序建议：先跑 Classic / Key Texts 占比高的模块（学术分量重），再跑 Supporting 为主的模块；每跑完一个模块，对照"生成 prompt"的期望结构与"证据假设"自检——假设对不上就在文件里标注，并考虑回退该模块。
