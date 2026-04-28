# 02 · 清洗数据

> **Neuman 出处**：Ch 12, "Cleaning Data" · p.397
>
> **何时用**：codebook 建好, 数据已录入, 跑任何分析之前
>
> **前置**：[01 · 建立 Codebook](01-codebook.md) 完成

---

## 📖 Neuman 怎么讲

数据从录入到分析, **错误是常态**。Neuman 给两种检查方法：

**1. Possible code cleaning (wild code checking)**
> Checking the categories of all variables for impossible codes.
>
> 例：性别编码为 1=男 / 2=女, 出现 4 → 编码错误。

**2. Contingency cleaning (consistency checking)**
> Cross-classifying two variables and looking for logically impossible combinations.
>
> 例：某受访者编码为"从未上过 8 年级", 但同时编码为"医生" → 逻辑不可能。

> "If you have a perfect sample, perfect measures, and no errors in gathering data but make errors in the coding process or in entering data into a computer, **you can ruin an entire research project**."

---

## ⚠️ 必须你自己判断的部分

- **错误如何修复**：发现 wild code 后, 是去原问卷查 / 标记为缺失 / 推断? 这是研究者的伦理判断
- **是否丢弃这条记录**：1 处错误 vs 多处错误的处理标准
- **缺失模式是否系统性**：随机缺失 vs 与 IV/DV 相关的缺失 (后者会偏估计)

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 的方法清洗这份数据。

【数据】[贴数据路径或前 5 行]
【Codebook】[贴 codebook 表格, 来自上一步]

【请帮我做三件事】

1. **Possible code cleaning (wild code 检查)**
   - 对每个变量, 列出: 期待范围 vs 实际出现的值
   - 标出所有不在期待范围内的值 + 它们出现在哪些 case
   - 不要直接修复, 列出来让我决定

2. **Contingency cleaning (一致性检查)**
   - 列出 3-5 对**逻辑上有约束**的变量组合 (如: 教育水平 vs 职业等级 / 年龄 vs 是否退休 / 婚姻 vs 配偶变量)
   - 对每对, 找出逻辑不可能的组合 + 涉及的 case
   - 不要直接处理, 列出来让我决定

3. **缺失值汇总**
   - 每个变量缺失多少 (绝对数 + 百分比)
   - 缺失模式: 是不是某些变量同时缺? 是不是某类受访者更容易缺?
   - **不做缺失填补**——只汇报情况

【硬约束】
- 不要"自动修复"任何错误
- 不要 drop 任何数据
- 工具: [Python pandas / R / Stata, 选一个]
- 输出代码 + 检查结果表格
```

---

## 💡 执行后的下一步

- Wild code 都修完了 → [03 · 单变量分析](03-univariate.md)
- 如果 contingency 错误很多 (>5%) → 暂停分析, 去看原始数据收集流程是不是有问题
- 如果某变量缺失 >30% → 考虑是不是要在分析里 drop 这个变量, 或者用更稳健的缺失处理方法

---

## 📌 WVS 演示填法

```
【数据】data/WVS_Wave_7_China_Csv_v5.1.csv (3036 × 346)
【Codebook】见 codebook.md (上一步产出)

【一致性检查重点对】
1. Q260 (出生年 1948-2000) vs 假设的成年门槛 (≥18 岁) — 应无矛盾
2. Q281 (职业, 1-10) vs Q275 (教育, 1-3) — 高级管理 (Q281=2) 但只有小学 (Q275=1)?
3. Q287 (收入十分位) vs Q288R (...) — 是否一致

【缺失码声明】WVS 用 -1, -2, -3, -4, -5 表示不同类型的缺失
```
