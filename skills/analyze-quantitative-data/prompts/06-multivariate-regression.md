# 06 · 多变量分析 · 多元回归

> **Neuman 出处**：Ch 12, "Multiple Regression Analysis" · p.420-422
>
> **何时用**：多个 IV 同时影响一个 DV, 想知道每个 IV 在控制其他变量后的净效应
>
> **前置**：[04 · 双变量分析](04-bivariate.md) 完成

---

## 📖 Neuman 怎么讲

> Multiple regression is a popular statistical technique whose calculation is beyond the level of this book. ... Multiple regression results tell the reader two things:
>
> 1. **R² (overall fit)**: 这组 IV 一共能解释 DV 多少变异
> 2. **Beta (β) coefficients**: 每个 IV 的标准化效应大小 + 方向

> "We use the beta regression coefficient to determine whether control variables have an effect. For example, the bivariate correlation between X and Y is 0.75. ... If the beta remains at 0.75, the four control variables have no effect. However, if the beta for X and Y becomes smaller (e.g., drops to 0.20), the control variables have an effect."

**关键约束**：
- IV 必须是 interval/ratio (或哑变量化的 nominal)
- DV 必须是 interval/ratio (否则用 logistic 回归)
- 不能有完全共线
- 残差最好正态 + 同方差

---

## ⚠️ 必须你自己判断的部分

- **哪些变量进模型**：理论驱动, 不是看哪个显著就放哪个
- **是否做加权回归**：调查数据 (如 WVS) **必须**用样本权重, 否则估计有偏
- **是否需要变量变换**：log(收入)? 是否标准化?
- **β 的实质性意义**：β=0.05 在统计上可能显著但在你领域可能不重要

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 跑多元回归。

【数据】[路径]
【DV】[变量名 + 度量层级] (必须 interval/ratio, 如不是请改用 logistic)

【IV 列表】（按理论关切排序——核心 IV 在前）
1. 核心 IV: [名]
2. 控制变量: [名 1], [名 2], ...

【控制变量为什么要放】（每个一句话理由——这是理论判断）
- [控制变量名]: 因为 [理论 / 文献 / 常识]
- ...

【特殊处理】
- 加权: [数据是否需要 sampling weight? 如 WVS / GSS 必须加, 普通自调样本通常不加]
- 哑变量: [哪些 nominal 变量需要 one-hot? (列出基准类别)]
- 缺失: [listwise / pairwise / 多重填补?]
- 工具: [Python statsmodels.formula.api / R lm() / Stata reg]

【请按以下顺序输出】

1. **诊断阶段** (先做, 别直接跑回归)
   - 多重共线检查 (VIF, 阈值 5 或 10)
   - 残差诊断 (正态性 QQ plot, 同方差 Breusch-Pagan)
   - 影响点 (Cook's D)
   - **如果有问题, 主动告诉我, 不要硬跑**

2. **基础模型** (Model 1: 仅核心 IV)
   - 报告: β, SE, t, p, 95% CI, R²
   - 写一句白话解读

3. **完整模型** (Model 2: 加全部控制变量)
   - 同样报告
   - **对比 Model 1 和 Model 2 里核心 IV 的 β**——变了多少? 这告诉我们什么?

4. **稳健性** (建议但不强制)
   - 如样本量够, 跑一次去掉影响点的版本对照
   - 如怀疑非线性, 加二次项试试

【硬约束】
- **不要替我说"研究成功"或"假设被验证"**——只报数字
- 输出 Stargazer/texreg 风格的对照表 (Model 1 vs Model 2)
- 报告 N (有多少 case 进入分析)
- 报告任何 listwise 删除的样本

【可疑点警示】
- R² > 0.9: 可能是过拟合或同义重复
- R² < 0.05: 模型基本没解释力, 重新想理论
- VIF > 10: 严重共线, 必须处理
- 某 β 的 p 值非常小但 β 接近 0: 大样本伪显著, 看 effect size
```

---

## 💡 执行后的下一步

- 模型稳健, 核心 IV 显著 → 写 results 段, 报实质性效应大小
- 核心 IV 在控制后变成不显著 → bivariate 关系是虚假的, 写进 discussion
- 核心 IV 仍然显著但 R² 很小 → 关系真但解释力有限
- 想做正式因果推断 → 看 [07 · 推断统计](07-inferential.md), 但**因果识别需要研究设计**, 不只是回归

---

## 📌 WVS 演示填法

```
【DV】Q159 (科技机会, 1-10)
【IV 列表】
1. 核心 IV: knowledge_worker (0/1)
2. 控制: age (continuous), female (0/1), edu (3 dummies), income_decile, urban

【加权】**必须**——WVS 是分层抽样, 用 W_WEIGHT
工具: Python statsmodels with freq_weights=W_WEIGHT

【预期】
Model 1: knowledge_worker β ≈ -0.13, p ≈ 0.50
Model 2 (加控制): knowledge_worker β ≈ +0.01, p ≈ 0.97 ← 几乎完美零
但 income_decile β ≈ -0.13, p < 0.001 ← 意外的显著负向
R² ≈ 0.011 (解释力非常弱)
```
