# 04 · 双变量分析

> **Neuman 出处**：Ch 12, "Results With Two Variables" · p.403-416
>
> **何时用**：单变量已看过, 想看两个变量之间的关系
>
> **前置**：[03 · 单变量分析](03-univariate.md) 完成

---

## 📖 Neuman 怎么讲

Bivariate 比 univariate **有用得多**——再简单的假设也至少要两个变量。两个核心概念：

> **Covariation**: Things go together or are associated.
> **Statistical independence**: No association between variables.

Neuman 给三种工具：

**1. Scattergram（散点图）**
- 适用：两个变量都是 interval/ratio
- 看三件事：**form (linear/curvilinear/independence) · direction (positive/negative) · precision (是不是紧贴一条线)**

**2. Percentaged Tables（百分比表）**
- 适用：两个变量是 nominal/ordinal
- **关键规则**：通常 IV 放列, 按列百分化; 然后**横着读** (跨行比较)
  - "Compare across rows if the table is percentaged down (by column)"
- Neuman 还讲了 **circle-the-largest-cell rule** 看关系强度

**3. Measures of Association（关联度量）**
| 度量 | 适用变量 | 范围 | 解读 |
|------|---------|------|------|
| Lambda (λ) | nominal | 0 to 1 | PRE 逻辑, 用众数预测 |
| Gamma (γ) | ordinal | -1 to +1 | 配对比较, 0.25-0.49 弱, 0.50-0.74 中, 0.75+ 强 |
| Tau (τ Kendall's) | ordinal | -1 to +1 | 比 gamma 更严 |
| Rho (ρ Pearson) | interval/ratio | -1 to +1 | 最常用的"相关系数" |
| Chi-square (χ²) | nominal/ordinal | 0 to ∞ | 还可作推断统计 |

---

## ⚠️ 必须你自己判断的部分

- **谁是 IV 谁是 DV**：理论判断, AI 给不了
- **变量的度量层级是否真的支持这种关联度量**：把 ordinal 当 interval 跑 Pearson 是常见错误
- **关系强度的实质性意义**：γ=0.25 在统计上"弱", 但在你领域可能很重要

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 的方法做双变量分析。

【数据】[路径]
【变量对】(每对填: IV, DV, IV 度量层级, DV 度量层级)
1. [IV 名 — 度量层级] × [DV 名 — 度量层级]
2. ...

【请对每对变量做以下三件】

1. **图形展示**
   - 两个 interval/ratio: scattergram + 标注 form/direction/precision
   - 两个 nominal/ordinal: 百分比表 (列 = IV, 按列百分化)
   - 一个 nominal + 一个 interval: 分组 boxplot

2. **关联度量**
   - 选**正确的**度量 (按 Neuman Table 4):
     · 都 nominal → Lambda + Chi-square
     · 都 ordinal → Gamma 或 Tau
     · 都 interval/ratio → Pearson rho + scatter
     · nominal × interval → ANOVA F 或 eta²
   - 报 r/γ/λ + 95% CI (如适用)

3. **实质性解读**
   - 关系是 weak/moderate/strong?
   - 方向 positive/negative?
   - 给我 1-2 句**学术风格**的描述, 类似:
     "There is a moderate positive ordinal association between X and Y (γ = 0.45)..."

【硬约束】
- 度量层级搞错绝对不允许——选错度量直接拒绝, 让我重选
- 工具: [Python / R]
- 不要直接跳到 multivariate; **先把 bivariate 看清楚**

【可疑点警示】
- 关系**强到离谱** (|r| > 0.85, γ > 0.85): 可能是同义重复 (两个变量本质同义)
- 关系**完全为 0**: 警惕样本量不够 / 变量编码反向
- **非线性**: scattergram 显示 U 型, 不能只看 r
```

---

## 💡 执行后的下一步

- Bivariate 关系存在 → [05 · 多变量阐释](05-multivariate-elaboration.md) 控制混淆变量看是否虚假
- 关系不存在但理论上应该存在 → 检查样本/测量, 也可能是真的零结果
- 关系存在且很想做因果 → [06 · 多元回归](06-multivariate-regression.md) + [07 · 推断统计](07-inferential.md)

---

## 📌 WVS 演示填法

```
【变量对】
1. knowledge_worker (nominal) × Q159 科技机会 (interval) → ANOVA / 分组均值
2. Q287 收入十分位 (ordinal) × Q159 (interval) → Pearson r (实操常用) 或 Spearman ρ
3. Q275 教育 (ordinal) × Q281 职业 (ordinal) → Gamma

【预期发现 (基于已跑过的版本)】
- knowledge_worker × Q159: 几乎 0 关联 (零结果)
- Q287 × Q159: 显著负 (高收入更悲观)
- Q275 × Q281: 应该正向 (教育越高职业越偏专业类)
```
