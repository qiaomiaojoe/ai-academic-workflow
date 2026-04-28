# 07 · Successive Approximation (逐次逼近)

> **Neuman 出处**：Ch 14, "Successive Approximation" · p.489
>
> **何时用**：你的 concept 还不稳, 数据和理论还在互相调整——要反复迭代
>
> **前置**：至少跑过一轮 [01 · 开放编码](01-open-coding.md) 和 [02 · 轴心编码](02-axial-coding.md)

---

## 📖 Neuman 怎么讲

> **Successive approximation**: A method of qualitative data analysis that **repeatedly moves back and forth between the empirical data and the abstract concepts, theories, or models**, adjusting theory and refining data collection each time.

> "You begin with research questions and a framework of assumptions and concepts. You then probe into the data, asking questions of the evidence to see how well the concepts fit the evidence and reveal features of the data. **You also create new concepts by abstracting from the evidence and adjusting concepts to fit the evidence better.** You then collect additional evidence to address unresolved issues and then repeat the process."

**关键节奏**: 概念 → 看数据 → 修概念 → 收新数据 → 再修

> "Each pass through the evidence is provisional or incomplete... you can refine generalizations and linkages to reflect the evidence better."

类比: 雕塑家不是一刀到位, 是反复打磨。

---

## ⚠️ 必须你自己判断的部分

- **什么时候停**：饱和 = 新数据不再改变概念
- **修概念 vs 修数据**：发现不一致, 是修 concept 还是质疑数据? 
- **几轮迭代算够**: 没有标准, 看 saturation

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 14 的 successive approximation 做迭代分析。

【当前 concept (来自上一轮)】
名: [...]
定义: [...]
来源 (理论 / 数据驱动?): [...]

【上一轮编码后的状态】
- 这个 concept 在多少段数据里得到支持? [N 段]
- 哪些段不支持 / 反例? [列出]
- 哪些段似乎相关但归不进? [列出]

【新数据 / 想纳入对照的额外数据】[贴新数据, 如有]

【请帮我做一轮迭代】

1. **审视 concept 与数据的拟合**
   - 列出当前 concept 的核心特征 (3-5 条)
   - 对每条, 看新数据怎么支持 / 挑战
   - **三种处理**:
     · 数据完全支持 → 保留, 但记下证据
     · 数据部分支持 → 修改特征 (变更精确 / 更宽 / 更狭)
     · 数据反对 → drop 这条特征 OR 把它变成"边界条件"

2. **修改 concept 定义**
   - 给一个 v2 定义 (不要完全推倒, 是迭代)
   - 标 v2 与 v1 的差异 (用 strikethrough + 新加)
   - 解释为什么这样改

3. **未解决问题清单**
   - 哪些数据还没有被解释?
   - 这些 unresolved 是边界情况, 还是真正的反例?
   - 下一轮要找什么新数据来 probe?

4. **是否饱和判断**
   1-5 评分:
   - 1 = 概念基本不稳, 还要多轮迭代
   - 3 = 大体稳了, 但还有边界要明确
   - 5 = 饱和, 新数据基本不改变 concept

【输出格式】
- v1 → v2 对比表
- 数据-理论拟合度报告
- 未解决问题清单
- 饱和评分 + 理由

【硬约束】
- 不要把 concept 改得面目全非——是迭代不是推倒
- 每个修改都要有数据依据
- 标记每轮迭代的日期, 方便后面 trace
```

---

## 💡 执行后的下一步

- 评分 ≤ 3 → 收新数据, 再来一轮
- 评分 = 4-5, concept 接近饱和 → [03 · 选择编码](03-selective-coding.md) 找代表证据 + [04 · Memo](04-analytic-memo.md) 整理
- 反复迭代很多轮 concept 还在大改 → 可能 RQ 本身需要重新想 (回 第4讲 研究设计)

---

## 📌 36kr 演示填法

```
【concept v1】"代际剪刀差"
v1 定义: AI 不裁老员工但关闭新人入门通道

跑了第一轮编码后发现:
- T13 (新职业涌现) 似乎是反例
- 但仔细读, T13 里的"新岗位"也是给有经验的人

迭代 v2:
v2 定义: AI 在中国 2025 话语中被建构为"机会的代际不对称分配"——
      ~~不裁老员工但关闭新人入门通道~~ 
      新增: 不只是关闭旧通道, 也阻碍新岗位向年轻人开放

差异: v1 强调"关闭", v2 强调"分配的代际不对称"——更宽
未解决: 找年轻人自己的访谈, 而不是只看媒体外部叙述
饱和评分: 3 (基本稳了, 但需要 actor's voice 数据补充)
```
