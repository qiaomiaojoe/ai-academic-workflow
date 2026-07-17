---
name: lit-pdf-zotero
description: 文献 PDF 获取 + Zotero 入库 + 可视化（乔淼PhD · AI学术训练营 · AI学术工作流）。对一份文献清单批量：确认 DOI/CNKI ID → 补全引用数 → 多渠道找 PDF 落盘（OA/preprint/sd-download/wos-download/cnki-download）→ 按金字塔结构建 Zotero Collection 逐条入库（含标签与 extra 元数据）→ 生成金字塔分布图 + PXYV 罗盘投影双图 HTML。Trigger on："把这批文献下载 PDF 入库 Zotero"、"文献入库+可视化"、"batch download PDFs and import to Zotero"、"入 Zotero 并画文献金字塔"。
---

# Lit PDF + Zotero · 获取 PDF → 入库 → 可视化

对一份文献清单（最好是 `lit-pyramid` 的分层清单；无分层也能跑，只是入库不分子集合、图 1 跳过）执行四步。

## 调用约定（独立运行）

- 输入：文献清单（分层表 / 普通表 / DOI 列表均可）+ Zotero Collection 名（默认 = 项目名或用户给的短名）。
- 落盘（默认当前工作目录）：PDF 存 `pdf_download/`，命名 AuthorYear.pdf；最终清单写 `文献清单.md`；可视化写 `[slug]-visualization.html`。
- 工具适配：Zotero MCP 不可用 → 只做 PDF + 清单落盘，并告知手动导入方式；下载工具按环境可用性挑。

## Step 1 · 确认 DOI / URL / CNKI ID

英文论文 → DOI；中文论文 → CNKI ID + 期刊+期号；经典专著 → 出版商 URL 或 DOI；非学术来源 → URL。

## Step 2 · 补全引用数

英文用 OpenAlex API（`https://api.openalex.org/works/doi:{DOI}` 取 `cited_by_count`）或 Google Scholar；中文用 `cnki-paper-detail`。清单里已有的不重采。

## Step 3 · 查找 PDF 并落盘

- 英文优先 `sd-download` / `wos-download` → Open Access（Unpaywall / OpenAlex / 出版商 OA）→ 作者自存档 → preprint（arXiv / SSRN / OSF）
- 中文用 `cnki-download`（要求已登录）
- 找不到的标 "no-pdf"；**不从可疑来源硬凑**。

最终清单落盘（下游文献分析在 Zotero 不可用时的兜底元数据）：
`| # | 标题 | 作者+年份 | 金字塔层 | PXYV 节点 | DOI/CNKI ID | 被引数 | 核心论点 | PDF 状态 |`（状态 = open-access / preprint / author-copy / cnki / no-pdf）

## Step 4 · 入库 Zotero + 可视化

Collection 结构：顶层 = Collection 名，下设 Classic / Key Texts / Supporting-P / Supporting-X / Supporting-Y / Supporting-V（无分层信息则只建顶层）。

逐条入库：有 DOI → `zotero_add_by_doi(doi, collections=[对应子集], tags=[金字塔层, PXYV节点, 项目slug], attach_mode="auto")`；只有 URL/CNKI → `zotero_add_by_url`（或用 `gs-export` / `sd-export` / `wos-export` / `cnki-export` 直接推送）。入库后用 `zotero_update_item` 写 `extra` 字段：

```
citations: 123
core_argument: 一句话核心论点
pxyv_weights: P=0.7, V=0.3
```

（pxyv_weights 按"主导维度"生成，单一维度 = 1.0。标签：金字塔层 "classic"/"key"/"supporting"；节点 "P"/"X"/"Y"/"V" 可多选；项目 slug。）

入库报告：`| # | 标题 | 入库状态 | PDF 附件 | Collection | 标签 |` + 统计（总入库 / PDF 已附 / 金字塔分布 / 节点覆盖）。

可视化（单文件 HTML，纯 HTML+CSS+内联 SVG 无外部库；浅色背景 #FAF7F2，amber #B8834A）：
- **图 1 文献金字塔分布图**：三层水平堆叠，顶 Classic（窄，标篇名+作者）→ 中 Key（标标题+主要节点）→ 底 Supporting（按数量宽度）；Classic #E65100 / Key #1565C0 / Supporting #558B2F。
- **图 2 PXYV 罗盘投影**：800×800 SVG；四锚点 P=(0,+1) / X=(+1,0) / Y=(0,-1) / V=(-1,0)，边缘标大字母 + 颜色（P #B8834A / X #5B8DBE / Y #7BAE7F / V #9B6DB0）。每篇一个圆点：位置 = pxyv_weights 归一化加权质心；半径 = `4 + 6*log10(citations+1)` clip [4,24]px；填充 = 金字塔层色 opacity 0.7；描边 = 主导维度色；悬停 tooltip（标题/作者年/引用数/核心论点）；同心圆 0.25/0.5/0.75/1.0 网格 + 双图例。
