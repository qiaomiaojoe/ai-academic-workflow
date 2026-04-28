# 06 · Ideal Types (Weber 理想类型)

> **Neuman 出处**：Ch 14, "Ideal Types" · p.487-489
>
> **何时用**：你想用一个**纯净的概念模型**对照现实数据, 看现实和模型有多远 / 哪里偏离
>
> **前置**：定性数据已收集

---

## 📖 Neuman 怎么讲

> **Ideal type**: A model or mental abstraction of social relations or processes. **Ideal types are pure standards against which the data or "reality" can be compared.**
>
> An ideal type is an artificial device used for comparison **because no reality ever fits an ideal type**.

例: Weber 的"理想科层制" = 纯净的层级 + 规则 + 非人格化 + 专业分工——但**现实中没有任何组织完全符合**, 这正是它的用途——作为**对照基准**。

**两种用法**:

**1. Contrast contexts (对照语境)**
- 你不想做普遍化, 想突出**每个 case 的独特性**
- ideal type 作为 sensitizing device, 让你看到每个 case 怎么"偏离"标准
- 例: Bendix (1956) 比较 Czarist Russia vs industrial England 的工业管理关系

**2. Analogies (类比)**
- 用一个 ideal type 把陌生现象**翻译成**熟悉的形态
- 例: "气氛突然冷下来, 像一阵冷风扫过房间"——不是真有风, 是 ideal type 类比
- 例: "性别关系像奴隶制"——不是真奴隶制, 是 ideal type 帮你看出权力深度

---

## ⚠️ 必须你自己判断的部分

- **构造哪个 ideal type**：选定一个值得对照的纯净模型, 这是理论判断
- **ideal type 不必符合任何 case**：不要因为没 case 100% 符合就放弃
- **ideal type 不是 hypothesis**：不能"验证", 只能用作"对照"

---

## ✂️ Prompt 模板

```
我要按 Weber / Neuman (2014) Ch 14 的 ideal types 方法分析数据。

【RQ】[一句话]
【数据】[贴]

【我想构造的 ideal type】（选一）

[ ] **构造一个纯净模型**, 然后看现实数据怎么偏离
   要构造的 type 名: [...]
   核心特征 (3-5 条, 每条一句话): [...]

[ ] **借用一个文献中的 ideal type**, 用作对照
   ideal type 名: [...]
   文献来源: [作者年份]

[ ] **不知道, 让我推荐**
   基于我的数据和 RQ, 推荐 1-2 个值得用作对照的 ideal types
   (例如: Weber 科层制 / 礼物经济 vs 商品经济 / 公共领域 / 个人主义 vs 集体主义)

【请帮我做】

1. **构造 / 借用 ideal type**
   - 写出 3-5 条核心特征 (每条一句话)
   - 这些特征要是**纯净**的——不必照顾任何具体 case

2. **对照现实数据**
   对每个数据 case (或 segment), 标注:
   - 哪些方面**符合** ideal type
   - 哪些方面**偏离**
   - 偏离方向: 强 / 弱 / 反向 / 完全不在量表上
   
   输出表格:
   | Case | 特征1 | 特征2 | 特征3 | ... | 总体 fit |

3. **解读偏离 pattern**
   - 偏离是不是有规律? (某类 case 系统性偏向 X 方向)
   - 偏离最大的 case 揭示了什么? (boundary 在哪?)
   - 如果几乎所有 case 都偏离同一方向, ideal type 可能要修正

4. **写作建议**
   - 怎么把 ideal type + 偏离写进 paper
   - 推荐 1-2 个最戏剧性的对照例子

【硬约束】
- 不许说"case X 不符合 ideal type 所以是错的"——ideal type 不是评价标准
- 偏离的描述必须有数据依据
- 不要把 ideal type 当成"理想状态"——它是分析工具
```

---

## 💡 执行后的下一步

- Ideal type 与现实对照写出来了 → 接 [04 · Analytic Memo](04-analytic-memo.md) 写理论 implication
- 不同 case 偏离方向不同 → [10 · Mill 比较](10-analytic-comparison-mill.md) 找系统性差异
- 偏离揭示了既有 ideal type 的不足 → [07 · Successive Approximation](07-successive-approximation.md) 修正

---

## 📌 36kr 演示填法

```
【RQ】中国财经媒体怎么叙述 AI×知识工作者?
【ideal type】Habermas 的 "理性公共领域" (Public Sphere)
特征:
1. 平等参与 (任何人都能发声)
2. 理性论辩 (基于事实和逻辑)
3. 公共利益导向 (不是私人利益)
4. 批判性 (敢挑战权力)

对照 16 段 36kr 报道:
- T01-T05 偏离方向: 平等参与×, 主要是经济学家/创始人发声; 理性论辩√, 引用数据
- T13 偏离: 公共利益×, 偏 individual 励志话语
- T16 偏离: 批判性×, 是 conformity 话语 ("成为 AI 需要的人")

发现: 几乎全部 segments 在 "平等参与" 和 "批判性" 维度严重偏离
解读: 中国财经话语场不是 Habermas 意义上的公共领域, 而是 expert-led, 
      conformity-oriented——这本身就是有意思的发现
```
