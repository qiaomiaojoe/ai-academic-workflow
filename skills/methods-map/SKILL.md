---
name: methods-map
description: 方法地图（乔淼PhD · AI学术训练营 · AI学术工作流 · 研究设计步骤）。map-reduce 逐篇扫描一批文献的方法论（9 字段：研究类型/设计/收集/样本/抽样/分析/度量层级/RQ链接）→ 汇总成方法地图（分布/组合频率/RQ-方法映射/趋势与方法 gap）+ 内嵌 methodology_plugin YAML + 基于地图给 2-3 个研究设计方案对照表供选 + 可视化 HTML 自动打开。Trigger on："帮我做方法地图"、"扫一下这批文献都用什么方法"、"methods map"、"给我 2-3 个研究设计方案"、"survey the methodology of my literature"。
---

# Methods Map · 方法地图 + 研究设计方案

扫描文献语料的方法论，产出方法地图与 2-3 个研究设计方案，**末尾停下等用户选方案**（初稿由 `methodology-draft` 承接）。

## 调用约定（独立运行）

- 输入：① RQ / 研究问题描述（用户给 / `选题.md`）② 学科/领域 ③ 文献语料（Zotero 集合 / 本地 PDF 文件夹 / 文献清单，三选一；主数据通道 Zotero MCP / NotebookLM / 本地 PDF）。**完全没有文献语料时**：告知证据基础缺失，给两个选项——先跑 `literature-search` 建库，或降级为"Web 检索 + 领域常识"的方法综述（所有结论标 [低] 置信度）——让用户选，不默默降级。
- 用户偏好（可选，未给则按领域惯例建议并标 [建议]）：主数据方法倾向 / 分析软件 / 预期样本规模 / 预期时间线。
- 落盘（默认当前工作目录，文件名固定）：`方法地图.md` + `方法地图.html`。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。

## A1 · 文献扫描（逐篇提取 · map-reduce，不一次性拼全文）

对每篇提取：citation（作者-年份）/ research_type（theoretical / qualitative / quantitative / mixed / computational）/ design（具体研究设计）/ data_collection（方法+时间+地点）/ sample_corpus（样本规模+特征）/ sampling_strategy（purposive / quota / random / theoretical / …）/ analysis_method（分析方法+框架）/ measurement_level（定量：nominal / ordinal / interval / ratio）/ rq_link（方法如何服务该文 RQ · 1 句）。

## A2 · 方法地图（汇总判断）

方法分布（按 research_type 占比）/ 方法组合频率（经验研究里最常用）/ RQ-方法映射表 / 领域趋势（时间演变 / 新兴方法 / 方法空白 gap）。

## A3 · methodology_plugin（内嵌报告，不单独落盘）

在报告中以一个 YAML 代码块给出：field / corpus_size / scan_date / mainstream_methods[{name, share, exemplars(2-3 篇), typical_for_rq}] / rare_or_emerging / method_gap / sampling_conventions / analysis_conventions / measurement_level_distribution。这是 `methodology-draft` 的方法决策依据。

## A4 · 研究设计方案（给用户选）

基于 A2 + A3 + 用户 RQ + 偏好，给 **2-3 个可选方案**对照表，每个含：方案名 + 一句话定位 / 路径（定性主导 / 定量主导 / 混合 + 为什么贴合 RQ 类型）/ 结构形式（IMRaD 独立 / 嵌入式 / 半独立）/ 核心方法链（抽样→收集→分析各一句）/ 对标 exemplar 1-2 篇 / 走主流还是填 method_gap / trade-off·风险·与偏好契合度·排除了哪些方法及原因。最后给一句推荐（哪个 + 一句理由），**不替用户决定**。

## 可视化（方法地图.html）

单文件 HTML（内联 CSS/JS 无外部依赖；背景 #FAF7F2 + amber #B8834A）。至少含：① 方法分布条形图 ② 方法组合频率条形图 ③ RQ-方法映射表 ④ 方法 gap 高亮卡片 ⑤「研究设计方案」区（A4 摘要 + 推荐）。每个数字/结论旁标置信度色点（高/中/低）。渲染完自动打开（macOS `open` / Windows `start ""` / Linux `xdg-open`，路径带引号）。

## 硬约束

- 所有结论可追溯到 A1 具体文献（作者-年份）；每条标置信度 [高] 原文明示 / [中] 领域常识推 / [低] 推测；全 [高] 视为没认真判断（至少 30% 应有 [中]/[低]）。
- 不确定标"未明示"；不编造文献/数字（[待补] / [TBD-citation] 占位）。
- ⛔ 输出 A4 方案后**必须停下**问："选哪个方案？或要怎么改？"用户明确回复前不产出初稿。下一步 → `methodology-draft`。
