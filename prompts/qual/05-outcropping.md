# 05 · Outcropping 识别

> **Neuman 出处**：Ch 14, "Outcroppings" · p.486-487
>
> **何时用**：开放编码后, 想从表象数据找出深层社会结构
>
> **前置**：[01 · 开放编码](01-open-coding.md) 完成

---

## 📖 Neuman 怎么讲

> **Outcropping**: An aspect of qualitative data analysis that recognizes some event or feature as representing deeper structural relations.

地质学比喻: outcropping 是基岩在地表的露出。地质学家通过地表的 outcropping 推测地下结构。

> "We use the data to generate and evaluate theories and generalizations and simultaneously assume that **beneath the outer surface of reality lie deeper social structures or relationships**."

**逻辑**:
- 我们直接观察的 (一句话, 一个动作, 一段文本) = surface reality
- 它们是更深结构的"露出" = outcropping
- 分析任务 = 通过这些 outcropping 推断**下面**有什么结构

例子 (Neuman 给的): 
- 看到一个吻 = 表层
- 推断出"深沉的爱" = 深层关系
- 看到职业差异 = 表层  
- 推断出"社会阶级" = 深层结构

---

## ⚠️ 必须你自己判断的部分

- **什么算 deeper structure**：阶级 / 性别 / 制度 / 话语秩序? 这是理论选择
- **outcropping 是不是被过度解读**：避免把每个细节都说成"代表深层 X"
- **多个 outcropping 是不是指向同一结构**：判断 convergent validity

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 14 的 outcropping 概念分析数据。

【数据 + 已有 codes】[贴]

【我假设的 deeper structures】（选一个或多个理论框架）
[ ] 阶级 / 经济结构
[ ] 性别 / gender 秩序
[ ] 制度 / 权力关系
[ ] 文化话语秩序
[ ] 殖民 / 后殖民
[ ] 其他: [...]

【请帮我做】

1. **筛选 outcropping 候选**
   从数据里挑出 5-10 个最具体、最具体的"小细节"——
   一句话、一个动作、一个具体描述, 而不是抽象总结。
   对每个标 ID。

2. **outcropping → structure 推断**
   对每个候选, 写:
   - **表层 (surface)**: 这是什么直接观察?
   - **可能的深层结构**: 这指向我假设的哪个 structure?
   - **推断逻辑**: 为什么这个表层细节支持这个推断?
   - **替代解释**: 还有什么其他深层结构能解释? (不能只给一种)

3. **convergence 检查**
   - 多个 outcroppings 是否指向同一结构?
   - 如果是, convergent validity 强
   - 如果不是, 警告我"data 里可能有多个并行的 deeper structures, 不要硬合并"

4. **过度解读警告**
   对**每个**推断, 评分 1-3:
   - 1 = 推断牵强 (一个细节不足以支持)
   - 2 = 推断合理但不唯一
   - 3 = 推断有多重证据支持

【输出格式】Markdown 表格

【硬约束】
- 不许把所有细节都说成"代表 X"——保留怀疑
- 列替代解释, 不要单一框架走到黑
- 表层引用必须逐字, 不许改写
```

---

## 💡 执行后的下一步

- Outcropping 集中指向 1-2 个 structures → 写进 findings 的 "deeper structure" 段
- Outcropping 分散 → 可能数据里有多个并行 structures, 用 [10 · Mill 比较](10-analytic-comparison-mill.md) 区分
- 推断都靠不住 (都打 1 分) → 数据稀薄, 收集更多

---

## 📌 36kr 演示填法

```
【数据】16 段 36kr 报道
【假设的 deeper structures】阶级结构 + 文化话语秩序

期望产出 (示例 1 个):

Outcropping: T13 "AI 协作设计师 / 数字伦理解释师等新岗位正在爆发, 这些岗位通常薪资可观"
表层: 列举新职业 + 强调高薪
推断 1 (阶级): 指向"AI 红利向上层集中"——只有有跨域协作能力的高端劳动力受益
推断 2 (话语秩序): 指向"机会主义话语"——把结构转型描述为个人机遇
替代: 也可能只是行业前景的描述, 不必然是结构话语
评分: 2 (合理但不唯一)
```
