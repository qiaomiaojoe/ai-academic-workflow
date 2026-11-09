# 更新记录

AI学术工作流 skills（乔淼PhD · AI学术训练营）。整个仓库一个版本号，写在 `version.json`；POPPER 按它告诉学员有没有新版、帮学员更新。

版本号怎么升：改措辞、修毛病 → 第三位（1.1.0 → 1.1.1）；加 skill、删 skill、改了 skill 的输入或产出文件 → 第二位（1.1.0 → 1.2.0）；整套推倒重来 → 第一位。新的写在最上面。

## 1.4.0（2026-11-09）

（加了 skill，升第二位。11-03 定的「检索 skill 重做留在 1.2.x」已经过时，乔淼 11-09 定了改向，接着往下加。配合 POPPER 内容 1.6.2。）

- **新加 `scholar`：谷歌学术检索**。关键词、作者、刊名、年份、精确短语、只搜篇名；被引数；「谁引了这篇」；导出 BibTeX 或进 Zotero。不用账号，自带脚本，和 `cnki`、`journal-rank` 共用单独的浏览器窗口；每页隔 5–10 秒，一小时最多 60 页，遇到验证码请用户点，不破解。从头写，没有用 cookjohn/gs-skills 的代码。
- **新加 `openalex`：英文文献公开接口**。检索、按 DOI 或篇名核对（对上 / 有出入 / 没找到，会报撤稿）、被引数、引用链。OpenAlex 用不了退到 Crossref，引用链退到 Semantic Scholar；不用浏览器，key 可填可不填。
- **`pxyv-search` 英文检索改用 `scholar`，上不去谷歌时用 `openalex`**；可以按期刊级别筛（`journal-rank`），报告写明这不等于 Web of Science / Scopus 检索结果。不再用 `gs-*`、`sd-*`、`wos-*`。
- **`lit-verify` 英文验真改用 `openalex` 的 `verify`**，再用 `scholar` 补查。
- **`lit-pdf-zotero` 英文 PDF 优先 `scansci-pdf`**，不再写 `sd-download`、`wos-download`。中文 PDF 暂时还是 `cnki-download`。

## 1.3.1（2026-11-07）

- **`sr-search-record` 在 Mac 的 AI 沙箱里检索不再断**：以前 `oa_search.py` 用 Python 自带的 urllib 联网，每次请求完就断开连接；POPPER 交给 Claude Code 的任务在沙箱里跑，联网要过沙箱的代理，代理会把还没转完的数据丢掉，报 `IncompleteRead`，重试 5 次都一样，检索跑不起来。现在改成保持连接、多次请求共用一条连接（照旧沿用系统代理设置），OpenAlex 和 Europe PMC 都是。11-07 在沙箱里实测 probe、recall、fetch（754 条翻页）、cite、epmc 都正常。
- **`cnki`、`journal-rank` 在 AI 沙箱里能用了（配合 POPPER 内容 1.5.2）**：Mac 上 AI 在沙箱里开不起查知网、查期刊用的浏览器（建不了 `~/.cnki-skill/`，Chrome 起来就退），一律回 `no_browser`。现在 POPPER 在沙箱外替它开好，脚本先等两三秒连上就用；查询记录写不了 `~/.cnki-skill` 时改写临时文件夹；实在开不起来，提示用户到 POPPER「AI学术环境配置 → 大家共用的 → 检索浏览器」点「打开」。SKILL.md 里 `no_browser` 的处理改成：照原样告诉用户、等用户开好再试，不要自己开浏览器、改端口、杀进程。自己在终端里跑跟以前一样。

## 1.3.0（2026-11-05）

（改了 skill 读的文件位置，按规矩升第二位。配合 POPPER 内容 1.5.1。）

- **MinerU 文字稿换地方**：POPPER 的 MinerU 工具从内容 1.5.1 起，把文字稿放在 PDF 所在文件夹下的 `MinerU文字稿/` 里，和 PDF 同名。比如 `文献/PDF/Smith2020.pdf` 的文字稿在 `文献/PDF/MinerU文字稿/Smith2020.md`。以前统一放 `文献/全文/`，那里已经转好的照旧认。
- 读全文先找文字稿的 15 个 skill 都改成先找新位置、再找旧位置：`knowledge-module-gen`、`critical-paper-reading`、`model-paper-deconstruct`、`review-synthesis`、`review-draft`、`review-draft-assembly`、`methods-map`、投稿与审稿 7 个，还有 `academic-project-init` 的「文件放哪」表。README 依赖表同步改。

## 1.2.1（2026-11-03）

（加了 skill，按规矩该升第二位；乔淼 11-03 定：这一轮检索 skill 重做都留在 1.2.x。）

- **新加 `journal-rank`：查英文期刊级别**。输入刊名或 ISSN（一次可以几本），回收录库（SCIE / SSCI / AHCI / ESCI / EI）、影响因子、JCI、JCR 学科和分区、分区、年发文量、综述占比、OA 占比、自引率、出版社。
  - 数据来自 iJournal（投必得学术），不用登录。网站把数据加密传输，脚本不碰它的接口，在单独的浏览器窗口里打开查询页、读页面显示出来的结果；和 `cnki` 共用一个浏览器窗口。
  - 每页隔 2–4 秒，一小时最多 120 页；查不到时给名字相近的候选，不拿相近的顶替。
- `lit-pyramid`：Key Texts 的期刊位次依据，英文期刊用 `journal-rank` 查。

## 1.2.0（2026-11-02）

起因：学员装的知网 skill（cookjohn/cnki-skills）作者 3 月后没再更新，要装 Chrome DevTools MCP，国内站证书出错就用不了，被拦、要验证码时只会说「失败」。

- **新加 `cnki`：自己的知网 skill**。随 skill 附脚本 `scripts/cnki.mjs`（只要 Node.js 18 以上，不装 npm 包、不装 MCP）：自己开一个单独资料的 Chrome（没有就用 Edge），在知网页面里调用知网自己的检索和导出接口。
  - 能做：检索（字段、年份、CSSCI / 北大核心等、只要学术期刊、翻页）；按篇名核对一篇是否真实存在并比对作者 / 年份 / 刊名（`verify`）；取题录详情；导出 RIS 或进 Zotero；自检。
  - 国内站打不开（证书错等）自动换海外版；每次请求随机隔 2–5 秒、一小时最多 150 次；遇到验证码把窗口提到前面等学员拖，不自动破解。
  - 每次回一段 JSON，`status` 说清是成功、没查到、要拖验证码、被拦、查太多、打不开还是知网改版了，调用它的 skill 按状态决定等人还是换来源。
  - 从头写的，没有复制原仓库的代码（原仓库没有开源许可证）。
- `lit-verify` 中文条目改用 `cnki` 的 `verify`；`pxyv-search` 知网检索改用 `cnki` 的 `search`；`lit-pdf-zotero` 中文被引数改用 `cnki`。中文 PDF 下载仍沿用原来的方式。
- README「依赖与降级」：知网一行改成 Node.js + Chrome。

## 1.1.4（2026-10-31，没有单独发布，随 1.2.0 一起发）

起因：学员 10-30 跑「文献搜索全流程」，选了中英混合，入库的却全是英文；Zotero 里有一条点开就「找不到文件」，还多了一条「误匹配附件」。

- **知网用不了时，中文文献换个地方核对**（`lit-verify`）：以前中文只认知网详情页，知网要登录、出验证码、连不上，中文候选就全卡在「待核」。现在按顺序换万方 / 维普详情页 → 期刊官网 → DOI，有一个来源的标题、作者、期刊、年份对得上就算通过，报告里单列「替代核查」。都查不到的照样剔除，不放松。
- **选了中英混合，就不能拿英文补中文**（`literature-search`）：某种语言验真后不够，停下来告诉你只核实了几条、卡在哪，让你选补搜、登录知网再验，还是接受少一些；总数不够就照实交少的。快速模式不为这个停，但照样不补，在「我替你做的决定」和报告开头写明。每阶段和最终报告都写语言分布。
- **Zotero 附件三查**（`lit-pdf-zotero`）：入库后不光看有没有附件记录，还要确认本机文件真的在、PDF 第一页真是这篇。空附件、抓错的 PDF 删掉那条附件（进 Zotero 回收站）再挂对的，不再改名留着；报告的「PDF 附件」只写四种状态。空附件多的提醒看 Zotero 网盘是不是满了。

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
