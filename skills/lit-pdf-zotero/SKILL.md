---
name: lit-pdf-zotero
description: 文献 PDF 获取 + Zotero 入库 + 可视化（乔淼PhD · AI学术训练营 · AI学术工作流）。对一份文献清单批量：确认 DOI/CNKI ID → 补全引用数 → 多渠道找 PDF 落盘（scansci-pdf/OA/preprint/cnki）→ 入一个 Zotero Collection（层级和 PXYV 节点记在标签里，不建子集合；含 extra 元数据）→ 生成金字塔分布图 + PXYV 罗盘投影双图 HTML。Trigger on："把这批文献下载 PDF 入库 Zotero"、"文献入库+可视化"、"batch download PDFs and import to Zotero"、"入 Zotero 并画文献金字塔"。
---

# Lit PDF + Zotero · 获取 PDF → 入库 → 可视化

对一份文献清单（最好是 `lit-pyramid` 的分层清单；无分层也能跑，只是没有层级标签、图 1 跳过）执行四步。

## 调用约定（独立运行）

- 输入：文献清单（分层表 / 普通表 / DOI 列表均可）+ Zotero Collection 名（默认 = 项目名或用户给的短名）。
- 落盘（默认当前工作目录）：PDF 存PDF 文件夹（在项目里按 AGENTS.md 的「文件放哪」表：工作站项目是 文献/PDF/，旧项目 02_文献/pdf_download/；独立运行默认 pdf_download/，或用户给的文件夹），命名 AuthorYear.pdf；最终清单写 `文献清单.md`；可视化写 `[slug]-visualization.html`。
- 工具适配：Zotero MCP 不可用 → 只做 PDF + 清单落盘，并告知手动导入方式；下载工具按环境可用性挑。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。

## Step 1 · 确认 DOI / URL / CNKI ID

英文论文 → DOI；中文论文 → CNKI ID + 期刊+期号；经典专著 → 出版商 URL 或 DOI；非学术来源 → URL。

## Step 2 · 补全引用数

英文用 `openalex` skill 的 `verify --doi`（取 `cited`），没有时用 `scholar` 的 `cited`；中文用 `cnki` skill 的 `verify` 或 `detail`（取 `cited`）。清单里已有的不重采。

## Step 3 · 查找 PDF 并落盘

- 英文优先 `scansci-pdf`（`scansci_pdf_download`，有 DOI 就用 DOI）→ Open Access（Unpaywall / OpenAlex / 出版商 OA）→ 作者自存档 → preprint（arXiv / SSRN / OSF）
- 中文用 `cnki` skill 的 `download <行号或详情页链接> --dir 文献/PDF`（要用户先在它的浏览器窗口里登录；回 `need_login` 就运行 `open` 请用户登录，不问账号密码）。`no_access` / `need_payment` 的标 no-pdf 列给用户，不去点付费
- 找不到的标 "no-pdf"；**不从可疑来源硬凑**。

最终清单落盘（下游文献分析在 Zotero 不可用时的兜底元数据）：
`| # | 标题 | 作者+年份 | 金字塔层 | PXYV 节点 | DOI/CNKI ID | 被引数 | 核心论点 | PDF 状态 |`（状态 = open-access / preprint / author-copy / cnki / no-pdf）

## Step 4 · 入库 Zotero + 可视化

Collection 结构：只建一个 Collection（名字 = Collection 名），**不建子集合**（不按金字塔层、不按 PXYV 节点分）。层级和节点一律记在标签里，用户在 Zotero 里按标签筛就能分开看。Collection 已存在就直接往里加。

逐条入库：有 DOI → `zotero_add_item(source=doi, collections=[Collection], tags=[金字塔层, PXYV节点, 项目slug], attach_mode="auto", if_exists="file")`（旧版 zotero-mcp 叫 `zotero_add_by_doi`，没有 `if_exists`）；只有 URL/CNKI → `zotero_add_item(source=url, …)`（旧版 `zotero_add_by_url`）（或用 `scholar` 的 `export --to zotero` 直接推送；中文没有 DOI 的，可用 `cnki` skill 的 `export <条目编号> --to zotero` 导进 Zotero 当前选中的分类，再用 `zotero_set_item_collections` 放进 Collection）。入库后用 `zotero_update_item` 写 `extra` 字段：

```
citations: 123
core_argument: 一句话核心论点
pxyv_weights: P=0.7, V=0.3
```

（pxyv_weights 按"主导维度"生成，单一维度 = 1.0。标签：金字塔层 `tier:classic` / `tier:key` / `tier:supporting`；节点 `pxyv:P` / `pxyv:X` / `pxyv:Y` / `pxyv:V` 可多选；项目 slug。）

**核对 PDF 附件（必做，三查）**：不能信入库接口回的「attached」——zotero-mcp 附件传不上去也会回报成功，还会留下**一条有记录、没文件的空附件**（用户在 Zotero 里一点就报「找不到文件」）。所以入库后逐条：
1. **有没有记录**：`zotero_get_item_children(item_key)` 看下面有没有 PDF 附件。
2. **文件在不在**：`zotero_get_attachment_path(item_key)` 取附件路径，确认本机这个文件真的存在（读不了本机文件的环境，报告里写「只确认了附件记录，没确认文件」，不写「已附」）。
3. **是不是这篇**：读附件 PDF 第一页（或 `zotero_get_item_fulltext`），标题、第一作者和条目对得上才算数。`attach_mode="auto"` 自动抓的 PDF 可能抓错（比如抓成同主题的另一篇综述）。

查出问题的处理（写死，不要自己发明办法）：
- **空附件或抓错的**：用 `zotero_delete_item(附件 key)` 删掉**这条附件**（Zotero 里删的进回收站，能找回；删前在报告里列出要删的附件和原因）。**不要**改名留着、**不要**另建一条独立附件、**不要**去改 Zotero 的 storage 文件夹。
- 删完，Step 3 有对的本地 PDF → `zotero_attach_file(item_key, file_path=本地 PDF 完整路径)` 重挂，再按上面三查一遍；没有对的 PDF → 报告写「抓错已删 / PDF 没传上」，本地 PDF（如果有）留着。
- 旧版没有 `zotero_attach_file`：**不要拿 `zotero_add_from_file` 代替**（它会新建一条重复条目），直接写「PDF 没传上」，并提示升级 zotero-mcp。
- 空附件不止一两条时，多半是 Zotero 网盘存储满了（免费 300 MB）或上传失败：报告末尾提醒用户看一下 Zotero「设置 → 同步 → 文件同步」；PDF 本地都在 PDF 文件夹里，不影响后面读文献。

入库报告：`| # | 标题 | 入库状态 | PDF 附件 | 标签 |`，「PDF 附件」只写这四种之一：已附（三查都过）/ 只有记录、没确认文件 / 抓错已删 / 没有 PDF；+ 统计（总入库 / PDF 已附 / 金字塔分布 / 节点覆盖 / 语言分布）。

可视化（单文件 HTML，纯 HTML+CSS+内联 SVG 无外部库；浅色背景 #FAF7F2，amber #B8834A）：
- **图 1 文献金字塔分布图**：三层水平堆叠，顶 Classic（窄，标篇名+作者）→ 中 Key（标标题+主要节点）→ 底 Supporting（按数量宽度）；Classic #E65100 / Key #1565C0 / Supporting #558B2F。
- **图 2 PXYV 罗盘投影**：800×800 SVG；四锚点 P=(0,+1) / X=(+1,0) / Y=(0,-1) / V=(-1,0)，边缘标大字母 + 颜色（P #B8834A / X #5B8DBE / Y #7BAE7F / V #9B6DB0）。每篇一个圆点：位置 = pxyv_weights 归一化加权质心；半径 = `4 + 6*log10(citations+1)` clip [4,24]px；填充 = 金字塔层色 opacity 0.7；描边 = 主导维度色；悬停 tooltip（标题/作者年/引用数/核心论点）；同心圆 0.25/0.5/0.75/1.0 网格 + 双图例。
