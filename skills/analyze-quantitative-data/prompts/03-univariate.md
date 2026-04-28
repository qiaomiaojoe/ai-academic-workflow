# 03 · 单变量分析

> **Neuman 出处**：Ch 12, "Results With One Variable" · p.397-403
>
> **何时用**：数据已清洗, 在做 bivariate 之前必须先看每个变量长什么样
>
> **前置**：[02 · 清洗数据](02-clean-data.md) 完成

---

## 📖 Neuman 怎么讲

单变量分析是**所有定量分析的起点**——你必须先知道每个变量的"形状"。Neuman 列了三类工具：

**1. Frequency Distribution（频率分布）**
> A table that shows the dispersion of cases into the categories of one variable.
>
> 三种呈现：raw count / percentage / grouped (适用于连续变量分箱)
> 三种图：histogram / bar chart / pie chart / frequency polygon

**2. Measures of Central Tendency（集中趋势）**
| 度量 | 适用变量 | 含义 |
|------|---------|------|
| Mode (众数) | nominal+ | 最常出现的值 |
| Median (中位数) | ordinal+ | 50th 百分位 |
| Mean (均值) | interval+ | 算术平均 |

**关键**：分布形状决定用哪个——
- 正态分布: 三者相等
- 偏态分布: 三者不同, 且**中位数对极端值更稳健**

**3. Measures of Variation（离散趋势）**
| 度量 | 含义 |
|------|------|
| Range | 最大值 − 最小值 |
| Percentile | 25th, 50th, 75th, 90th |
| Standard Deviation | 平均"距离"到均值 |
| z-score | 标准化分数, 跨变量可比 |

---

## ⚠️ 必须你自己判断的部分

- **看哪个集中趋势量**：偏态严重时不能只报 mean
- **分箱策略**：连续变量分组, 组距怎么定？(Neuman: 组必须互斥且穷尽)
- **图表的轴范围**：见 Neuman Chart 1 (p.405)——同样数据不同 Y 轴范围会"撒谎"

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 的方法做单变量分析。

【数据】[路径]
【Codebook】[贴]
【关注的变量列表】[列出 5-10 个核心变量名 + 度量层级]

【请按以下顺序对每个变量】

1. **Frequency Distribution**
   - Nominal/ordinal: raw count + percentage 表
   - Interval/ratio: 给两版——分箱表 + histogram

2. **Central Tendency**（按度量层级选）
   - Nominal: 只报 mode
   - Ordinal: 报 mode + median
   - Interval/ratio: 报 mode + median + mean
   - **如三者差异 > 10%, 主动告诉我"这是偏态分布, 建议主用 median"**

3. **Variation**（同样按度量层级）
   - Ordinal+: range + percentile (25/50/75)
   - Interval+: 加 standard deviation
   - 如果做跨变量对比, 计算 z-score

4. **可视化**
   - 每个变量出 1 张图 (histogram / bar chart, 按度量层级选)
   - **Y 轴必须从 0 开始** (Neuman Chart 1 警告: 不要选择性截断)

【硬约束】
- 工具: [Python (pandas + matplotlib) / R (tidyverse) / SPSS]
- 不要直接做相关性或回归——这是 univariate
- 输出代码 + 表格 + 图

【可疑点警示】
跑完后主动告诉我:
- 哪些变量分布**严重偏态** (mean vs median 差 >10%)
- 哪些变量**方差几乎为 0** (没有 variation, bivariate 就不能用)
- 哪些变量**有明显异常值** (outlier, 在均值 ±3 SD 之外)
```

---

## 💡 执行后的下一步

- 所有变量都看过了, 没异常 → [04 · 双变量分析](04-bivariate.md)
- 发现严重偏态 → 考虑变量变换 (log / 分箱) 再继续
- 发现某变量方差几乎为 0 → 这变量在分析里没用, 可能要 drop

---

## 📌 WVS 演示填法

```
【关注变量】
- Q159 (科技带来更多机会, 1-10, interval)
- knowledge_worker (0/1 哑变量, nominal)
- age (连续, ratio)
- Q275 (教育, 1-3, ordinal)
- Q287 (收入十分位, 1-10, ordinal/interval 边缘)
- urban (1/2, nominal)

【预期会发现】
- Q159 可能轻偏态 (5-7 区间集中)
- knowledge_worker 极不平衡 (~13% 是, 87% 否)
- age 接近正态
```
