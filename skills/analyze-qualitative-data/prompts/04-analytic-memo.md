# 04 · 分析备忘录 (Analytic Memo)

> **Neuman 出处**：Ch 14, "Analytic Memo Writing" · p.485-486
>
> **何时用**：贯穿整个定性分析过程——边编码边写, 不是等到最后
>
> **前置**：开始做 [01 · 开放编码](01-open-coding.md) 时就同步开始

---

## 📖 Neuman 怎么讲

> The analytic memo is **a special type of note**. It is a memo or discussion of thoughts and ideas about the coding process that you write to yourself. Each coded theme or concept forms the basis of a separate memo.

> "The analytic memos have a **conceptual, theory-building intent**. They do not report data but comment on how data are tied together or how a cluster of data is an instance of a general theme or concept."

**关键**: memo 不是数据笔记 (data note), 是**理论思考**笔记。

**Neuman 给 10 条建议** (Expansion Box 3, p.486):
1. 数据收集开始时就写, 一直到最终报告完成
2. 写日期, 方便看思考演化
3. 灵感来了就立刻写——不要等
4. 定期重读, 看看哪些 memo 可以合并 / 区分
5. 每个 concept/theme 一个独立 memo 文件
6. memo 和 data note 分开存
7. memo 之间互相引用
8. 两个想法同时来——拆成两个 memo
9. 写不出新的——标"saturation reached on this theme"
10. 维护一个 memo 标签清单

---

## ⚠️ 必须你自己判断的部分

- **写多深**：是粗略想法还是接近段落初稿?
- **何时停止某 memo**：饱和 = 你已经能流畅地讨论它, 没有新想法涌出
- **memo 之间的 link**: 哪些 memos 在后期会拼成一个章节?

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 14 / Strauss 的方法写 analytic memo。

【上下文】
- 编码阶段: [open / axial / selective]
- 关注的 theme/concept: [一个]
- 已有数据支持: [贴 2-5 段相关数据]

【上一次写这个 memo 是什么时候】[日期; 没有就填"首次"]

【请帮我写一份 analytic memo】, 包含:

1. **Concept 名 + 当前定义**
   (一句话, 比 axial coding 时更精炼)

2. **理论 anchor**
   - 这个 concept 接近文献里哪些既有概念?
   - 我和文献的概念有什么细微差异? 我的更精细 / 更宽 / 不同?
   - 引 1-2 个潜在对话文献 (用 [作者年份] 形式, 我后面验证)

3. **数据如何支持**
   - 列 3-5 段最强证据
   - 说明每段证据**怎么**支持这个 concept (不只是引用)

4. **内部张力 / 矛盾**
   - 数据里有没有反例?
   - 如果有, 是 concept 不准, 还是反映 concept 的 boundary?

5. **与其他 themes 的关系**
   - 这 concept 因果先于哪些其他 themes?
   - 是另一个的子集吗?
   - 有张力关系吗?

6. **下一步要查的数据 / 文献**
   - 哪类新数据能进一步检验这 concept?
   - 哪些文献我还没看但应该看?

7. **写作 implication**
   - 如果这 concept 进入 final paper, 它出现在哪一节? (intro / lit review / findings / discussion)
   - 大概几段?

【格式】Markdown, 标题就用 concept 名, 日期写在第一行
【长度】400-800 字 (memo 不是论文, 别写太长)

【硬约束】
- 不许虚构数据里没有的细节
- 引文献时, 如果不确定, 标 [作者年份-待验证]
- memo 是给我自己看的, 可以用第一人称
```

---

## 💡 执行后的下一步

- 同一 theme 多次回来重写 memo——看 memo 序列怎么演化, 是 axial coding 的输入
- memo 充裕到能拼一段 → 直接转化为 findings 段落初稿
- memo 进入"想不出新东西"状态 → 标 saturation, 进入 [03 · 选择编码](03-selective-coding.md) 找代表证据

---

## 📌 36kr 演示填法 (示意 memo)

```
# Analytic Memo: 代际剪刀差
Date: 2026-04-28

## Concept 当前定义
AI 在中国 2025 话语场中被建构为"不裁老员工但关闭新人入门通道"的力量,
形成代际间机会结构的剪刀差——老一代守住既有位置, 新一代失去入门资格。

## 理论 anchor
- 接近 Beck (1992) "individualization risk society" 但更具代际形态
- 与 Standing (2011) "precariat" 概念相似但聚焦白领/知识工作者新一代
- 我的概念**更精细**: 强调是 AI 这种特定技术造成的代际不对称, 不是一般化的不安全

## 数据支持
- T01 "新人连门都摸不到": 直接的入职率数据 (-14%)
- T02 "完美替代": 列举了具体被替代的工作类型 (实习生整理纪要等)
  → 关键: AI 替代的是**任务**, 但任务集中在初级岗位 → 形成代际效应
- T05 "金饭碗可能直接蒸发": Amodei 50% 预测, 极端形态

## 内部张力
T13 (新职业涌现) 似乎是反例——AI 也创造新岗位 (协作设计师等)。
但仔细看: 这些新岗位也是给**有经验的人**, 不是给应届生。
所以 T13 不是反例, 而是 reinforcement: 代际剪刀差在新机会分配上同样存在。

## 与其他 themes 的关系
- 因果先于 Theme 2 (阶层流动通道封闭): 没有入门就没有上升
- 与 Theme 5 (个体适应主义) 张力: "学 AI 工具" 的解药假设个体能跨过门槛, 但这门槛本身就是被关闭的

## 下一步
- 数据: 找年轻群体的访谈数据, 看他们自己怎么描述这个困境 (现在数据都是媒体外部观察)
- 文献: 查 Putnam 1995 / Massey 2007 关于代际不平等的经典理论

## 写作 implication
进入 findings 第一节 (~2-3 段), 也是 paper 的 hook. 
T01+T02+T05 三段交织呈现, 然后用 T13 做 turn (反例其实是同一逻辑).
```
