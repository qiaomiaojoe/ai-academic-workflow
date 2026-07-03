---
name: research-design
description: 研究设计 skill（源自 AI学术工作台 04 研究设计工作流，单品化）。分两阶段：阶段 A 文献方法扫描（map-reduce 逐篇提取 9 字段）→ 方法地图 + 内嵌 methodology_plugin YAML + 2-3 个研究设计方案（含可视化 HTML）→ CHECKPOINT 用户选方案 → 阶段 B 敲定方案 + 方法论段骨架 + 研究设计清单（抽样/工具/编码书/信效度/伦理/时间线）+ 干净版 Sec 4 方法论 draft。文献语料支持 Zotero 集合 / 本地 PDF / 文献清单；RQ 可由用户直接给，不依赖选题或综述文件。Trigger on："帮我做研究设计"、"方法论地图"、"研究设计工作流"、"设计我的研究方法"、"写方法论初稿"、"design my study methodology"、"methods map from my literature"、"research design options"。
---

# Research Design · 方法地图 → 方案选择 → 研究设计初稿

整个流程分两阶段：**阶段 A** 一次连续产出（方法地图 → 研究设计方案），在阶段 A 末尾**停下**等用户选定方案 / 给修改意见；用户回复后才进入 **阶段 B**（敲定 + 初稿）。

## 单品调用约定（输入解耦）

按优先级解析输入：
1. **用户直接给的**：RQ / 假设 / 变量 / 领域描述（可替代选题.md）；综述要点或"直接扫文献"均可（可替代综述初稿.md）。
2. **工作台项目**：`01_选题/选题.md`（PXYV + RQ + 5 近邻）+ `02_文献/综述初稿.md`（Section 1/2/3 · 含 gap 与定位）存在则自动读。
3. **最小必需输入**（都没有时一次问齐）：① RQ 或研究问题描述（必）② 学科/领域（必）③ 文献语料来源（必，下面三选一）。

**文献语料（方法扫描的对象，三选一）**：Zotero 集合名 / 本地 PDF 文件夹 / 文献清单 md。主数据通道同样三选（Zotero MCP 读原文 / NotebookLM 严格 citation / 本地 PDF 页码最可靠），逐篇 map-reduce 抽取，不要一次性拼接全部全文。**若用户完全没有文献语料**：告知方法地图的证据基础会缺失，给两个选项——先跑 `literature-search` skill 建库，或降级为"Web 检索 + 领域常识"的方法综述（所有结论标 [低] 置信度）——让用户选，不要默默降级。

**用户偏好（可选，未给则 AI 按领域惯例建议并标 [建议]）**：主数据方法倾向 / 分析软件偏好 / 预期样本规模 / 预期时间线。

**输出落盘降级**：在项目里 → `02_文献/方法地图.md` + `02_文献/方法地图.html`、`03_框架/研究设计初稿.md` + `03_框架/研究设计-设计说明.md`（固定文件名与位置，不要改名/换目录/加日期后缀——下游 06 全文初稿按固定路径读）；不在项目里 → 当前目录同名文件。

**工具适配**：以环境实际可用为准，不可用时明确说并给替代，不要编造工具结果。

## 阶段 A · 方法论地图 + 研究设计方案（给用户选）

**A1 · 文献扫描（逐篇提取 · map-reduce）**。对每篇文献提取：
- citation（作者-年份）
- research_type（theoretical / qualitative / quantitative / mixed / computational）
- design（具体研究设计）
- data_collection（方法 + 时间 + 地点）
- sample_corpus（样本规模 + 特征）
- sampling_strategy（purposive / quota / random / theoretical / ...）
- analysis_method（分析方法 + 框架）
- measurement_level（定量：nominal / ordinal / interval / ratio）
- rq_link（方法如何服务该文 RQ · 1 句）

**A2 · 方法地图（汇总判断）**：方法分布（按 research_type 占比）/ 方法组合频率（经验研究里最常用）/ RQ-方法映射表 / 领域趋势（时间演变 / 新兴方法 / 方法空白 gap）。

**A3 · 方法论外挂 methodology_plugin**（内嵌方法地图报告，不单独落盘）：在报告中以一个 YAML 代码块给出：field / corpus_size / scan_date / mainstream_methods[{name, share, exemplars(2-3 篇), typical_for_rq}] / rare_or_emerging / method_gap / sampling_conventions / analysis_conventions / measurement_level_distribution。作为阶段 B 的方法决策依据。

**A4 · 研究设计方案（给用户选）**：基于 A2 + A3 + 用户的 PXYV/RQ + 方法偏好，给 **2-3 个可选研究设计方案**对照表，每个方案含：
- 方案名 + 一句话定位
- 路径：定性主导 / 定量主导 / 混合（+ 为什么贴合 RQ 类型）
- 结构形式：IMRaD 独立 / 嵌入式 / 半独立
- 核心方法链：抽样 → 收集 → 分析（每环节一句）
- 对标 methodology_plugin 里哪 1-2 篇 exemplar（最接近 RQ 的参照）
- 走主流路径 还是 填补 method_gap
- 主要 trade-off / 风险 / 与样本规模·时间线·软件偏好的契合度 / 该方案排除了哪些方法及原因

最后给一句**推荐**（推荐哪个 + 一句理由），但不要替用户决定。

**阶段 A 落盘**（文件名与位置固定）：
1. `方法地图.md`（主报告 · 含 A1-A4 + 内嵌 methodology_plugin YAML · 给人读）
2. `方法地图.html`（可视化 · 单文件无外部依赖，内联 CSS/JS；浅色背景 #FAF7F2 + amber #B8834A。至少含：① 方法分布条形图 ② 方法组合频率条形图 ③ RQ-方法映射表 ④ 方法 gap 高亮卡片 ⑤「研究设计方案」区（A4 摘要 + 推荐）。每个数字/结论旁标置信度色点（高/中/低）。渲染完自动打开：macOS `open "…"` / Windows `start "" "…"` / Linux `xdg-open "…"`，路径含空格带引号）

**⛔ CHECKPOINT · 必须停下**：输出 A4 方案后，停下来问："选哪个方案？或要怎么改？" 用户明确回复前，**不要进入阶段 B，不要产出初稿**。

## 阶段 B · 敲定方案 + 研究设计初稿（待用户回复后再做）

按用户敲定/修改后的方案展开为完整研究设计：

**B1 · 全局方法决策**：路径 / 结构形式 / 对标 exemplar（承接选定方案，补全理由）。

**B2 · 方法论段骨架（5-7 段）**，每段输出 6 维度表：
`| 功能（Rationale/Context/Sampling/Collection/Variable/Analysis/Ethics/Limit） | 方法决策（选什么 · 从 mainstream_methods 里排除什么 · 为什么 trade-off） | 外挂对照（methodology_plugin 路径 · 主流/小众/新趋势/gap） | 统计决策（定量段才填：测量层级 → 合法工具链） | 引用候选（来自综述初稿 + 5 近邻，不自造） | 要写什么（3-5 句段落 outline） |`

**B3 · 研究设计清单（把决策变可执行）**：
1. 抽样设计：抽样矩阵（维度 × 标准 × 目标 N）+ 纳入/排除标准 + 招募路径 + 饱和判定（定性）/ 样本量合规（定量）
2. 数据收集工具：定性 → 访谈提纲（4-5 个 block，每 block 3-5 问）；定量 → 问卷结构（按 section）；录音 / 转录 / 软件细节
3. 分析框架：定性 → 编码书（演绎层框架 + 归纳层 Braun-Clarke 六步 + 整合规则）；定量 → 统计方法链（测量层级 → 工具）
4. 信度 / 效度 / 伦理：Trustworthiness 四维（Lincoln-Guba 操作化）+ Ethics 清单（IRB / 知情同意 / 匿名 / 数据存储 / 退出权利 / 风险披露）+ Reflexivity（作者立场 + bracketing）
5. 时间线：从 IRB 到 draft 的阶段 × 时间估计（结合用户预期时间线）

**B4 · Sec 4 方法论 draft（合成）**：基于 B2 骨架 + B3 清单合成 Research Methodology draft。
- 语体：按产出语言约定（英文/双语时用学术语体，正文约 1200-1500 词）
- 所有具体数字（N / κ / 时间线）来自 B3；关键节点写成"选 A 排除 B"的方法决策叙事；引用 author-date 格式
- ⚠️ B4 正文是要落盘到「干净初稿」的内容，正文里**不要夹** [骨架对照] / [外挂引用] / [教学点] 等批注——这些放进辅助文档

**一致性检查（最后必做）**：Sec 4 是否呈现 operationalisation 过程（虚→实）；每段是否都有外挂对照；每段方法决策是否能追溯到选定方案。

## 硬规则

- 所有结论可追溯到 A1 具体文献（作者-年份）；每条结论/方法决策标置信度 [高] 原文明示 · [中] 领域常识推 · [低] 推测；全 [高] 视为没认真判断（至少 30% 应有 [中]/[低]）
- 不确定标"未明示"；不编造文献/数字：缺数字用 [待补]、缺引用用 [TBD-citation: 角色] 占位
- 排除的备选方法必须从 methodology_plugin.mainstream_methods 里选
- 不用综述/外挂完全没涉及的方法；limitation 不写成诉苦
- 阶段 A 末尾必须停下等用户确认，再做阶段 B

## 阶段 B 落盘（两份文件分离 · 固定文件名与位置）

1. `研究设计初稿.md` —— **干净版 · 下游输入**：只放 B4 的 Sec 4 方法论 draft 正文（连续可读的成稿），不夹批注。这是「全文初稿」工作流方法论节的输入文件。
2. `研究设计-设计说明.md` —— **辅助文档**：B1 全局决策 + B2 段骨架表 + B3 设计清单 + 每段 [教学点]（方法论写作技法 1-2 句）+ 每段 [骨架对照]/[外挂引用] 对照 + 一致性检查（所有解释性/脚手架内容集中在此）。

两份文件顶部各写一行互相指引（初稿 ←→ 设计说明）。交付前自检：文件名与位置是否与上面完全一致；正文是否真的"干净"（无批注）；设计说明里每段操作是否与初稿每段对应；占位符是否都标了 [待补] / [TBD-citation]。
