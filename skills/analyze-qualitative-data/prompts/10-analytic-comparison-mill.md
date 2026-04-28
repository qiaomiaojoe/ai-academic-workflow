# 10 · Analytic Comparison · Mill 五法

> **Neuman 出处**：Ch 14, "Analytic Comparison" · p.492-494
>
> **何时用**：你有**多个 cases** (3-10 个), 想找出导致某个共同结果的因果因素
>
> **前置**：多 case 数据已收集 + 每 case 已基本编码

---

## 📖 Neuman 怎么讲

来自 J.S. Mill (1806-1873) 的两种比较法:

**Method of Agreement (求同法)**
> Focuses attention on what is common across cases. You establish that cases share a common outcome and then try to locate a common cause, although other features of the cases may differ. The method proceeds by **a process of elimination**.
>
> 逻辑: 多个 cases 都有结果 Y, 它们也都共享因素 X, 而其他因素都不同——X 可能是 Y 的原因。

**Method of Difference (求异法)**
> Compares characteristics among cases in which some share a significant outcome but others do not; focuses on the differences among cases.
>
> 逻辑: 一些 cases 有 Y 一些没 Y, 比较二者差异——差的因素 X 可能解释 Y。

**Mill 的"双重应用"**:
> The method of difference is usually stronger and is a "double application" of the method of agreement.

例 (Skocpol Theory of Revolution): 
- France/Russia 1917/China — 都有 state breakdown + peasant revolt → 都革命
- England/Russia 1905/Germany/Prussia/Japan — 缺一个或都缺 → 都没革命
- 推断: state breakdown + peasant revolt 是革命的必要条件

**警告**:
> Analytic comparison sometimes is called nominal comparison because the factors in the qualitative data are often at a nominal level of measurement... organized as a chart that looks similar to a Guttman scale.

通常用 QCA (Qualitative Comparative Analysis) 软件正式化做。

---

## ⚠️ 必须你自己判断的部分

- **case 怎么选**: 选 case 是"理论抽样"——不是随机, 要让对照组之间因素差异最大化
- **factors 怎么列**: 不能太多 (case 数 ≥ factor 数), 不能漏掉关键因素
- **是 necessary 还是 sufficient cause**: Mill 法本身只能说 "associated with", 因果需要理论判断

---

## ✂️ Prompt 模板

```
我要按 Mill / Neuman (2014) Ch 14 的 analytic comparison 比较多个 cases。

【cases 列表】(3-10 个)
1. Case 1: [名]
2. Case 2: [名]
...

【共同关心的 outcome (Y)】
[一句话, 如 "组织生存 / 革命发生 / 社会运动成功"]
对每 case 标 Y 是 / 否 / 部分:
- Case 1: Y = [yes/no/partial]
- Case 2: Y = [...]
...

【可能的 causal factors (X)】
列 3-7 个理论上相关的因素, 每个标可观察的 indicator:
- Factor A: [...]
- Factor B: [...]
...

【数据】[贴每 case 的关键描述, 至少能让 AI 判断每个 X 在该 case 是 yes/no/partial]

【请按以下顺序做】

1. **建 truth table**
   每行一个 case, 每列一个 factor + outcome
   
   | Case | Factor A | Factor B | ... | Outcome Y |
   |------|----------|----------|-----|-----------|
   | 1    | Y        | N        | ... | Y         |

2. **Method of Agreement 分析**
   - 在所有 Y=yes 的 cases 里, 哪些 factors 都共有?
   - 这些 candidate causes 在 Y=no 的 cases 里也共有吗?
     · 如果也共有 → 不是 cause
     · 如果**只**在 Y=yes 出现 → 候选 necessary cause

3. **Method of Difference 分析**
   - 找一组**配对 cases**: 一个 Y=yes 一个 Y=no, 但**只有 1-2 个 factors 不同**
   - 那些不同的 factors 是 candidate sufficient causes

4. **double application**
   把 1 + 2 综合: 哪些 factors 既在 agreement 里出现, 又在 difference 里出现?

5. **逻辑组合 (truth-table 风格)**
   - 是否有 factor combinations 解释 Y? (如 "A AND B → Y")
   - 是否有 factor 单独足够? (sufficient)
   - 是否有 factor 不可或缺? (necessary)

6. **稳健性警示**
   - cases 数够吗? (Neuman: 通常 3-10 个)
   - factors 太多吗? (factor 数应 < case 数)
   - 有没有遗漏的 factor? (replicate 比较时换不同 factor 看结果是否变)

【输出】
- Truth table
- Agreement 分析结果
- Difference 分析结果
- 最终 candidate causal claim
- Limitations + 进一步研究方向

【硬约束】
- 不要直接说"X 因果导致 Y"——Mill 法只能说"X is associated with Y"
- 因果判断需要 + 理论 + 时间顺序 + 排除替代
- factor 编码必须有数据依据, 不许猜
```

---

## 💡 执行后的下一步

- 找到强候选因素 → 写 comparative findings 章
- factor 数远超 case 数 → 减少 factor 或增 cases
- 想做更严的逻辑分析 → 用 QCA 软件 (Ragin)
- Mill 比较结果与既有理论冲突 → [07 · Successive Approximation](07-successive-approximation.md) 修正

---

## 📌 Skocpol 演示 (Neuman Example Box 2)

```
Cases: France / Russia 1917 / China / England / Russia 1905 / Germany / Prussia / Japan

Factors:
- Factor A: State Breakdown (Y/N)
- Factor B: Peasant Revolt (Y/N)
Outcome: Revolution? (Y/N)

Truth table:
| Case        | A | B | Y |
|-------------|---|---|---|
| France      | Y | Y | Y |
| Russia 1917 | Y | Y | Y |
| China       | Y | Y | Y |
| England     | Y | N | N |
| Russia 1905 | N | Y | N |
| Germany     | N | N | N |
| Prussia     | N | N | N |
| Japan       | N | N | N |

Agreement: 所有 Y=yes 都有 A=yes 和 B=yes
Difference: England (A=Y, B=N → Y=N) 和 Russia 1905 (A=N, B=Y → Y=N) 显示 A 或 B 单独不够
推断: A AND B → Y (revolution requires BOTH state breakdown AND peasant revolt)
```
