# 更新记录

AI学术工作流 skills（乔淼PhD · AI学术训练营）。整个仓库一个版本号，写在 `version.json`；POPPER 按它告诉学员有没有新版、帮学员更新。

版本号怎么升：改措辞、修毛病 → 第三位（1.1.0 → 1.1.1）；加 skill、删 skill、改了 skill 的输入或产出文件 → 第二位（1.1.0 → 1.2.0）；整套推倒重来 → 第一位。新的写在最上面。

## 1.1.3（2026-10-27）

- **投稿与审稿 7 个 skill 的说明写完整了**：`submission-task-intake`、`manuscript-diagnosis`、`manuscript-revision`、`journal-requirements-check`、`submission-package-preparation`、`review-response-planning`、`review-revision-response` 的 description 改成和其他 skill 一样：写清做什么、产出什么、交给下一步哪个 skill，加上「Trigger on：」触发例句，AI 更容易在该用的时候想到它们。
- **正文不再用 s01–s07 编号**：互相指代一律写 skill 名；去掉「入口卡」「工作台外」「精加工过」等只有开发时才懂的说法。旧编号在每个 SKILL.md 开头「工作流位置」里留一处对照，老工作台按编号调用仍能对上。方法本身没改，各 skill 的方法版本不变。
- **修了 `critical-paper-reading` 的 description**：里面有个英文冒号「Trigger on: 」，严格的 YAML 解析（比如 Codex）会读错，改成中文冒号。
- **README 加「依赖与降级」**：本库用到、但要另装的工具（知网 / WoS / ScienceDirect / Google Scholar 检索 skills、scansci-pdf、Zotero 服务、OpenAlex key、pandoc、skill-creator、MinerU）从哪装、哪些 skill 用、没装时会怎样。
- **加 skill 体检脚本和自动检查**：`python3 scripts/validate_skills.py` 检查 frontmatter、name 和文件夹是否一致、description 长度和触发例句、`version.json` 名单、CHANGELOG 版本、README 里的数量和链接、引用的 skill 是否存在、旧编号是否回潮；GitHub 上每次推送自动跑一遍（`.github/workflows/validate-skills.yml`）。

## 1.1.2（2026-10-24）

- **更多 skill 读全文先找 MinerU 文字稿**：`review-synthesis`（证据综合逐篇读全文；有文字稿的算拿到全文 `evidence_level = fulltext`）、`methods-map`（逐篇扫描方法），以及投稿返修的 7 个 skill（`submission-task-intake`、`manuscript-diagnosis`、`manuscript-revision`、`journal-requirements-check`、`submission-package-preparation`、`review-response-planning`、`review-revision-response`）回原文核对文献时，`文献/全文/<同名>.md` 有就读它，页码按 `<!-- 第 N 页 -->`（有印的页码用印的）。

## 1.1.1（2026-10-24）

- **读全文先找 MinerU 转好的文字稿**：POPPER 内容 1.2.3 起「读文献」里有 MinerU 工具，能把 PDF（包括扫描版、带回归表的）转成 `文献/全文/<和 PDF 同名>.md`，每页开头标 `<!-- 第 N 页 -->`（页面上印的页码不一样时标成 `<!-- 第 N 页 · 印的页码 X -->`，引用写印的页码）。`knowledge-module-gen`、`critical-paper-reading`、`model-paper-deconstruct`、`review-draft`、`review-draft-assembly` 读一篇的全文时，有这个文件就读它（页码按标记），没有照旧读 PDF；`academic-project-init` 的「文件放哪」表加了 `文献/全文/` 一行。没装 MinerU 的不受影响。

## 1.1.0（2026-10-23）

- **文献入库跟上新版 Zotero 服务**：zotero-mcp 从 0.15 起改了工具名（比如 `zotero_add_from_file` 改成 `zotero_add_item`）。`lit-pdf-zotero`、`critical-paper-reading`、`review-synthesis`、`sr-search-record` 里写成新名字，旧名放在括号里，装新版、旧版 Zotero 服务的都能用。
- **入库后核对 PDF 附件**（`lit-pdf-zotero`）：旧版 Zotero 服务传 PDF 附件会失败，却说已经传好了。现在入库后会查条目下面是不是真有 PDF，没有就补传，还传不上就在入库报告里写明「PDF 没传上」。

## 1.0.0（2026-10-19）

POPPER 正式发布时的那一套，共 44 个 skill：选题、文献搜索、文献分析、研究设计、数据分析、全文初稿，综述文章，期刊投稿与审稿返修。许可证 CC BY-NC 4.0。
