# 更新记录

AI学术工作流 skills（乔淼PhD · AI学术训练营）。整个仓库一个版本号，写在 `version.json`；POPPER 按它告诉学员有没有新版、帮学员更新。

版本号怎么升：改措辞、修毛病 → 第三位（1.1.0 → 1.1.1）；加 skill、删 skill、改了 skill 的输入或产出文件 → 第二位（1.1.0 → 1.2.0）；整套推倒重来 → 第一位。新的写在最上面。

## 1.1.1（2026-10-24）

- **读全文先找 MinerU 转好的文字稿**：POPPER 内容 1.2.3 起「读文献」里有 MinerU 工具，能把 PDF（包括扫描版、带回归表的）转成 `文献/全文/<和 PDF 同名>.md`，每页开头标 `<!-- 第 N 页 -->`（页面上印的页码不一样时标成 `<!-- 第 N 页 · 印的页码 X -->`，引用写印的页码）。`knowledge-module-gen`、`critical-paper-reading`、`model-paper-deconstruct`、`review-draft`、`review-draft-assembly` 读一篇的全文时，有这个文件就读它（页码按标记），没有照旧读 PDF；`academic-project-init` 的「文件放哪」表加了 `文献/全文/` 一行。没装 MinerU 的不受影响。

## 1.1.0（2026-10-23）

- **文献入库跟上新版 Zotero 服务**：zotero-mcp 从 0.15 起改了工具名（比如 `zotero_add_from_file` 改成 `zotero_add_item`）。`lit-pdf-zotero`、`critical-paper-reading`、`review-synthesis`、`sr-search-record` 里写成新名字，旧名放在括号里，装新版、旧版 Zotero 服务的都能用。
- **入库后核对 PDF 附件**（`lit-pdf-zotero`）：旧版 Zotero 服务传 PDF 附件会失败，却说已经传好了。现在入库后会查条目下面是不是真有 PDF，没有就补传，还传不上就在入库报告里写明「PDF 没传上」。

## 1.0.0（2026-10-19）

POPPER 正式发布时的那一套，共 44 个 skill：选题、文献搜索、文献分析、研究设计、数据分析、全文初稿，综述文章，期刊投稿与审稿返修。许可证 CC BY-NC 4.0。
