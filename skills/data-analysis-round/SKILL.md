---
name: data-analysis-round
description: 数据分析「跑一轮」skill（源自 AI学术工作台 05 数据分析工作流，单品化）。三种分支：定量（调 analyze-quantitative-data，Neuman Ch12）/ 定性（调 analyze-qualitative-data，Neuman Ch14）/ 自定义 skill（完全按该 skill 自身规则执行，不稀释硬约束）。支持多轮多 skill 分析：每轮产出带前缀不覆盖（-R2/-R3）+ 分析日志.md 逐轮记账。RQ/变量/颗粒度可由用户直接给，不依赖研究设计文件。Trigger on："跑一轮定量/定性分析"、"用 XX skill 分析这份数据"、"数据分析工作流"、"分析这份问卷/访谈"、"run a quantitative/qualitative analysis round"、"analyze my data with skill X"。
---

# Data Analysis Round · 跑一轮（定量 / 定性 / 自定义 skill）

每次调用 = 跑**一轮**分析（多轮/多 skill 不覆盖、有记账）。三个分支：quant（`analyze-quantitative-data`）/ qual（`analyze-qualitative-data`）/ custom（任意用户指定 skill）。

## 单品调用约定（输入解耦）

**必填**：数据/材料文件路径（用户给；没有就先要，不开工）。custom 分支还需 skill 名。

**分析设定（RQ / DV / IV / 度量层级 / 编码方案 / 颗粒度 / 抽样加权）**按优先级解析：
1. 用户在会话里直接给的（或「额外指令/备注」写明的）→ 最高优先。
2. 工作台项目产出：`03_框架/研究设计初稿.md`（RQ/假设/变量定义）+ `03_框架/研究设计-设计说明.md`（B3 分析框架：抽样/加权/方法链/度量层级/编码方案/颗粒度）+ 备用 `01_选题/选题.md`；从中提取设定并与研究设计敲定的方案保持一致。
3. 都没有 → 问用户最小设定：本轮 RQ 一句话 +（定量）DV/IV 与度量层级 或（定性）编码取向；答不上就由所调 skill 的默认流程从头带（如 quant 从 codebook 步开始）。**不要因缺文件拒跑，也不要凭空假设。**

**额外指令/备注**（可选，一个通用入口）：本轮针对哪个子问题/假设、RQ 侧重、从哪步起、临时调整、注意点。留空 = 按设定 + skill 默认流程跑，由 skill 自行决定起步。备注优先于默认流程。

**输出落盘降级**：在项目里 → 产出写 `04_数据/`，记账写 `04_数据/分析日志.md`；不在项目里 → 当前目录 `./数据分析产出/` + `./数据分析产出/分析日志.md`。

## 分支 · 定量（quant）

用 `analyze-quantitative-data` skill，按 Neuman 7e Ch 12 步骤：Q1 codebook → Q2 cleaning → Q3 univariate → Q4 bivariate → Q5 elaboration → Q6 regression → Q7 inferential。

硬约束（skill 自动强制）：
- 度量层级正确（nominal × interval → ANOVA + eta²，拒绝 Pearson r）
- WVS / CGSS / GSS 负值 = missing，默认过滤
- 可疑点扫描（p > 0.05 / R² 异常高 / eta² < 0.01 都主动报）
- 零结果合法化（引 Neuman p.426）
- 加权回归（抽样调查必须用 sampling weight）
- 每个数值必须报 N

输出：描述统计 + 关联度量 + effect size + 显著性 + 可疑点扫描结果。产出文件前缀 `quant-`（如 quant-描述统计.md / quant-回归结果.md）。

## 分支 · 定性（qual）

用 `analyze-qualitative-data` skill，按 Neuman 7e Ch 14 步骤：L1 open coding → L2 axial coding → L3 selective coding；L4 analytic memo / L5 outcropping / L6 ideal types；L10 Mill 分析比较（如适用）。

硬约束（skill 自动强制）：
- 主题命名避免太宽泛（"power" "agency" 这种空词被拒）
- ground truth 验证：抽样 3 条访谈做人工编码对比
- 编码颗粒度一致性检查（不在同一份数据混用 fine / coarse）
- 每个主题必须 ≥ 3 个数据片段支持
- 选择性编码必须有清晰的核心范畴

输出：编码本（含频次 + 代表性引语）+ 轴心主题 + 逻辑关系图 + 选择性编码分类（如适用）+ analytic memo（理论思考，非数据笔记）。产出文件前缀 `qual-`。

## 分支 · 自定义 skill（custom）

完全按用户指定 skill 自身定义的步骤、硬约束与输出格式执行——**不要用本 skill 的说明覆盖或稀释该 skill 内部的方法论规则**。由该 skill 判断从哪步开始（除非备注指定起点）。

硬约束：
- 该 skill 内部声明的所有硬约束（CRITICAL / REFUSE / 度量层级 / 缺失值 / 显著性阈值 / 主题片段数门槛等）原样强制，不放宽。
- 每个结论必须可回溯到数据（数值报 N，定性主题报支持片段数 + 代表性引语）。
- 拿不准是不是该停下问用户的，先停下问，不要替用户做主。

输出：按该 skill 定义的结构化产出（具体到字段，不要只给一段 summary）+ 关键判断的依据 + 可疑点扫描。产出文件前缀 = skill 名（非法字符转 `-`）。

## 【本轮产出 + 多轮记账】（三分支共用 · 务必不要覆盖既有产出）

- 产出文件名带本轮前缀，且**不要覆盖之前轮次的同类文件**（已存在同名就加 -R2 / -R3…）。
- 在 分析日志.md 末尾**追加**一条本轮记录（文件不存在就新建并写表头，存在就续写，不要重写整表）：
  `| 轮次 | 日期 | skill | 针对的子问题/假设 | 关键发现（1-2 句 · 含 N + effect size 或主题支持数）| 产出文件 | 注意事项 |`
- 末尾「下一步建议」明确二选一：① 还要再跑一轮 / 换个 skill 补哪一块分析（说清补什么）；② 全部子问题已覆盖，调用 `findings-synthesis` skill 把各轮产出汇总成 研究发现.md。
