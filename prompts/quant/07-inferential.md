# 07 · 推断统计

> **Neuman 出处**：Ch 12, "Inferential Statistics" · p.422-426
>
> **何时用**：从样本结果**推论总体**, 做正式假设检验
>
> **前置**：要么有 univariate/bivariate 描述结果, 要么有回归输出, 要做显著性陈述

---

## 📖 Neuman 怎么讲

**核心区分**：
> Descriptive statistics describe... Inferential statistics build on probability theory to test hypotheses formally, permit inferences from a sample to a population, and test whether descriptive results are likely to be due to random factors or to a real relationship.

**关键概念**：
- **Statistical significance**: 结果由抽样误差产生的概率
- **Levels**: 通常 .05, .01, .001 (Neuman: .05 是社会科学约定俗成的妥协)
- **Type I error (α)**: 实际无关系但你说有 (false positive)
- **Type II error (β)**: 实际有关系但你说无 (false negative)

> "Tests for inferential statistics are useful but limited. The data must come from a random sample, and tests consider only sampling errors. Nonsampling errors (e.g., a poor sampling frame or a poorly designed measure) are not considered."

**重要警告**：
> "Statistical significance is not the same as practical, substantive, or theoretical significance. Results can be statistically significant but theoretically meaningless or trivial."

例：指甲长度和说法语能力可能 statistically significantly correlated, 但显然没意义。

---

## ⚠️ 必须你自己判断的部分

- **样本是不是 random sample**: 如果不是, 推断统计的前提就不成立 (但很多人不管也用)
- **多重检验校正**: 测了 10 个 IV 至少 1 个会偶然 p<.05, 要不要做 Bonferroni / FDR?
- **效应大小 vs 显著性**: 大样本里几乎所有效应都显著, 真正问题是 effect size
- **零结果怎么写**: 不显著 ≠ 没关系, 可能是样本量不够 (Type II error)

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 做推断统计。

【已有结果】[贴 univariate/bivariate/regression 的描述结果]
【样本来源】[填: random sample / convenience / 分层抽样 / 滚雪球]
【样本量 N】[...]

【请帮我做】

1. **检查推断前提**
   - 样本是不是 random? 如果不是, 警告我"推断统计的结论应有保留"
   - N 够不够? (Cohen 1988 的经验: 每个 IV 至少 20 个 case)
   - **不要硬跑——前提不满足就提示我**

2. **选合适的检验**
   按变量类型自动选:
   - 两个均值比较 → t-test (independent / paired)
   - 多个均值比较 → ANOVA F + post-hoc (Tukey HSD)
   - 两个 nominal/ordinal 关联 → Chi-square
   - 一个 interval × 一个 interval → 相关系数检验
   - 回归系数 → t-test on β

3. **报告完整结果**
   每个检验都要有:
   - 检验统计量 (t / F / χ² / r 等)
   - 自由度
   - p 值 (报精确值, 不只是 < .05)
   - **效应大小** (Cohen's d / η² / r / Cramér's V) — Neuman 没强调但现代标准必须报
   - 95% CI

4. **解读三段**
   - 统计层面: 是否拒绝 H0?
   - 实质层面: effect size 在你领域算大算小?
   - 限制: 推断的前提在多大程度上满足?

【硬约束】
- 显著性级别: [.05 / .01 / .001 三选一]
- 多重检验: [是否需要 Bonferroni / Holm / FDR?]
- 不要省略 p > .05 的结果——零结果也是结果
- 工具: [Python scipy.stats / R / SPSS]

【可疑点警示】
- p < .001 但 effect size 很小 (d < 0.2): 大样本伪显著, 强调实质不显著
- N 很小 (<30) 跑 t/F: 警告 power 不足
- p 接近 .05 (.04 或 .06): Neuman 警告这是任意切线, 报精确 p
- 多个检验全显著: 担心 fishing, 建议预注册或校正
```

---

## 💡 执行后的下一步

- 全部 plan 内的检验跑完 → 写 results 段
- 发现关键检验不显著但 effect size 不小 → 报告"指向 X 但 underpowered", 不说"没关系"
- 多重比较显著结果多 → 做 Bonferroni 或 FDR 校正再报
- 推断前提严重不满足 → 在 limitations 里诚实说出来

---

## 📌 通用警告（Neuman 强调）

> "Beginning researchers sometimes believe they have done something wrong if their results do not support a hypothesis. There is nothing wrong with rejecting a hypothesis. The goal of scientific research is to produce knowledge that truly reflects the social world, not to defend pet ideas or hypotheses."

零结果也是结果。**不要因为 p > .05 就不发**——这是 publication bias 的源头。

---

## 📌 WVS 演示填法

```
【已有结果】回归显示 knowledge_worker β ≈ +0.01, p ≈ 0.97; income_decile β ≈ -0.13, p < .001
【样本】WVS 中国 2018 分层抽样, N=1957 (listwise 后)

【关注的检验】
1. knowledge_worker 系数显著性: t-test on β (已在回归里报)
2. 收入十分位 vs Q159: 相关检验
3. 教育水平 (1/2/3) 之间 Q159 均值差异: ANOVA F + Tukey

【效应大小】算每个 finding 的 standardized effect (β/SD_DV)
【多重检验】在 9 个 IV 里有几个 p<.05? Bonferroni 校正后是否仍显著?
```
