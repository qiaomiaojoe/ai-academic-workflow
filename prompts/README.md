# 数据分析 Prompt 库 · 基于 Neuman 7e

> **来源**：W. Lawrence Neuman, *Social Research Methods: Qualitative and Quantitative Approaches*, 7e
> · Chapter 12 (Analysis of Quantitative Data, p.393-430)
> · Chapter 14 (Analysis of Qualitative Data, p.477-512)
>
> **目的**：把 Neuman 教科书的系统步骤转成可直接贴到 Claude/ChatGPT 的 prompt
>
> **用法**：找到你需要的步骤 → 打开对应 .md → 复制 `## Prompt 模板` 段落 → 替换 `[方括号]` → 贴给 AI

---

## 🎯 核心定位

**你不需要先成为统计学家／质性方法学家，才能开始做数据分析。**
Neuman 是权威教科书，AI 是执行助手。你的位置是把两者拼起来——
**让 AI 按教科书的步骤跑，你监督关键判断**。

每一个 prompt 都注明：
- 📖 **Neuman 出处**（哪一章哪一节、哪几页）
- ⚠️ **必须你自己判断的部分**（AI 顶不到的地方）
- 💡 **执行后的下一步**（接下来该用哪个 prompt）

---

## 📊 定量分析 · 基于 Ch 12

| # | Prompt | 对应 Neuman 节 | 何时用 |
|---|--------|----------------|--------|
| 01 | [建立 Codebook](quant/01-codebook.md) | Coding the Data, p.393-394 | 拿到原始数据, 还没整理成可分析格式时 |
| 02 | [清洗数据](quant/02-clean-data.md) | Cleaning Data, p.397 | Codebook 建好, 数据已录入, 跑分析前 |
| 03 | [单变量分析](quant/03-univariate.md) | Results With One Variable, p.397-403 | 看每个变量长什么样 |
| 04 | [双变量分析](quant/04-bivariate.md) | Results With Two Variables, p.403-416 | 看两个变量之间的关系 |
| 05 | [多变量 · 阐释模型](quant/05-multivariate-elaboration.md) | The Elaboration Paradigm, p.417-420 | 用控制变量看 bivariate 关系是否虚假 |
| 06 | [多变量 · 多元回归](quant/06-multivariate-regression.md) | Multiple Regression, p.420-422 | 多个自变量同时影响一个因变量 |
| 07 | [推断统计](quant/07-inferential.md) | Inferential Statistics, p.422-426 | 从样本推论总体, 做显著性检验 |

---

## 📝 定性分析 · 基于 Ch 14

### 编码三阶段（Strauss 1987）

| # | Prompt | 对应 Neuman 节 | 何时用 |
|---|--------|----------------|--------|
| 01 | [开放编码 (Open Coding)](qual/01-open-coding.md) | Coding Qualitative Data, p.481 | 第一遍读原始数据, 浮现初步主题 |
| 02 | [轴心编码 (Axial Coding)](qual/02-axial-coding.md) | Axial Coding, p.482-484 | 开放编码完成, 找概念之间的连接 |
| 03 | [选择编码 (Selective Coding)](qual/03-selective-coding.md) | Selective Coding, p.484 | 主要主题已确定, 扫全部数据找证据 |

### 边编码边写

| # | Prompt | 对应 Neuman 节 |
|---|--------|----------------|
| 04 | [分析备忘录 (Analytic Memo)](qual/04-analytic-memo.md) | Analytic Memo Writing, p.485-486 |
| 05 | [Outcropping 识别](qual/05-outcropping.md) | Outcroppings, p.486-487 |

### 七大分析策略 (Neuman 487-498)

| # | Prompt | 对应 Neuman 节 | 适用情境 |
|---|--------|----------------|---------|
| 06 | [Ideal Types](qual/06-ideal-types.md) | p.487-489 | 用 Weber 的理想类型对照现实 |
| 07 | [Successive Approximation](qual/07-successive-approximation.md) | p.489 | 反复迭代概念与证据 |
| 08 | [Illustrative Method](qual/08-illustrative-method.md) | p.489-490 | 用证据填充既有理论的"空盒子" |
| 09 | [Domain Analysis](qual/09-domain-analysis.md) | p.490-492 | Spradley 文化领域分析 |
| 10 | [Analytic Comparison · Mill 五法](qual/10-analytic-comparison-mill.md) | p.492-494 | 多案例比较, 找共同因果 |
| 11 | [Narrative Analysis](qual/11-narrative-analysis.md) | p.494-498 | 历史/过程性数据, 找路径依赖 |

---

## 🛠 使用建议

### 不需要全用
18 个 prompt 不是清单, 是**菜单**。一项研究通常只用其中 3-5 个：
- **入门定量研究**：codebook → clean-data → univariate → bivariate → regression（5 个）
- **入门定性访谈分析**：open-coding → axial-coding → selective-coding → analytic-memo（4 个）
- **历史/比较研究**：open-coding → ideal-types → analytic-comparison → narrative-analysis（4 个）

### Prompt 不是"问 AI"，是"指挥 AI"
Neuman 的步骤是科学方法学的成熟约定。Prompt 的作用 = 把这些约定**强制**给 AI 遵守, 防止它偷懒或瞎编。

### 第 6 步检查仍然必须
即使有 Neuman 的步骤 + AI 的执行, **关键判断仍然需要找比你懂的人帮看 30 分钟**。AI 让你能把研究**做出来**, 但通过审稿人这一关需要外部验证。

---

## 📁 也提供 Claude Skills 版本

如果你用 Claude Desktop 或 Claude Code, 可以直接把以下两个 skill 装到 `~/.claude/skills/`:
- [`analyze-quantitative-data`](../skills/analyze-quantitative-data/) — 把 Ch 12 全部 7 个步骤打包
- [`analyze-qualitative-data`](../skills/analyze-qualitative-data/) — 把 Ch 14 全部 11 个步骤打包

装好后, Claude 会在你提到"我要分析这份数据"时自动建议调用对应 skill。
