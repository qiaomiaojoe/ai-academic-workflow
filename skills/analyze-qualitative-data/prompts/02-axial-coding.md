# 02 · 轴心编码 (Axial Coding)

> **Neuman 出处**：Ch 14, "Axial Coding" · p.482-484
>
> **何时用**：开放编码完成后, 找概念之间的连接和"轴心"
>
> **前置**：[01 · 开放编码](01-open-coding.md) 完成

---

## 📖 Neuman 怎么讲

> This is a "second pass" through the data. During open coding, you focus on the actual data and assigning code labels for themes. You are little concerned about making connections among themes or elaborating the concepts that the themes represent. **In contrast, you begin axial coding with an organized set of initial codes or preliminary concepts.** In this second pass, you focus on the initial coded themes more than on the data.

> "While axial coding, you ask about **causes and consequences, conditions and interactions, strategies and processes**."

**目的**:
1. 把分散的初级码组织成 themes
2. 找 themes 之间的关系
3. 识别"轴心概念"——其他概念围绕它转

> "Axial coding not only stimulates thinking about linkages between concepts or themes, but also raises new questions. It can suggest dropping some themes or examining others in more depth. It also reinforces the connections between evidence and concepts."

---

## ⚠️ 必须你自己判断的部分

- **哪个概念是轴心**: 这是理论判断
- **关系类型怎么命名**: causal? sequential? oppositional? hierarchical?
- **删 vs 留 themes**: 出现频次低 ≠ 不重要; 高 ≠ 重要

---

## ✂️ Prompt 模板

```
我要按 Strauss (1987) / Neuman (2014) Ch 14 做轴心编码。

【上一步产出】[贴开放编码的全部 codes + memo seeds]

【研究问题 RQ】[再次贴一遍]

【请按以下顺序做】

1. **聚类**
   - 把语义相近的 analytic codes 合并成 3-7 个 themes
   - 每个 theme 给一个**具体名字** (避免 "AI 影响" 这种太空的; 偏好 "代际剪刀差" / "阶层流动通道封闭")
   - 每个 theme 一句话定义
   - 列出该 theme 下的初级 codes + 段落 ID

2. **关系图**
   按 Neuman 的提示问 6 类问题:
   - **Causes**: 哪个 theme 在因果上先于其他?
   - **Consequences**: 某 theme 的后果是什么?
   - **Conditions**: 某 theme 在什么条件下成立?
   - **Interactions**: themes 之间怎么互相影响?
   - **Strategies**: 行动者用什么策略应对?
   - **Processes**: 是不是有时间顺序的过程?

3. **关系类型标注**
   themes 之间的关系标为以下之一:
   - 因果 (A → B)
   - 互斥 (A ⊥ B, 不能同时成立)
   - 嵌套 (A ⊃ B, A 包含 B)
   - 对立 (A ↔ B, 张力关系)
   - 并列 (A || B, 并行存在但不直接关联)

4. **识别"轴心"**
   - 哪 1-2 个 themes 是"轴心"——其他 themes 围绕它? 
   - 给一句话理论解释为什么它是轴心

5. **drop vs keep 建议**
   - 哪些 themes 证据弱 (< 3 段支持)? 建议 drop / 收集更多数据 / 合并到其他 theme?
   - 哪些 themes 极强 (> 50% 段落涉及)? 是不是过宽, 需要拆?

【输出格式】
- Markdown: 每 theme 一段, 含定义/包含 codes/段落 ID/与其他 theme 关系
- 然后一张关系图 (用 Mermaid 或 ASCII 画)
- 末尾: drop/keep 建议表

【硬约束】
- 不许凭空发明数据里没有的 theme
- Theme 的命名要避免太宽泛 (Schwandt 警告: 概念要有抓力)
- 关系判断必须有数据依据 (列出支持的段落)
```

---

## 💡 执行后的下一步

- Themes 稳定, 准备做 final pass → [03 · 选择编码](03-selective-coding.md)
- 概念关系还在动 → 做 [07 · Successive Approximation](07-successive-approximation.md), 反复迭代
- 想用既有理论指导编码 → [08 · Illustrative Method](08-illustrative-method.md)
- 关系是过程性的 → [11 · Narrative Analysis](11-narrative-analysis.md)

---

## 📌 36kr 演示预期产出

```
Theme 1: 代际剪刀差 (轴心)
  定义: AI 不裁老员工但关闭新人入门通道
  包含 codes: 入职率下降, 完美替代, 金饭碗蒸发
  段落: T01, T02, T03, T05
  
Theme 2: 阶层流动通道封闭
  定义: 蓝领→白领传统升级路径被堵死
  包含: 大量简单工作失业, 中产困境
  段落: T14, T15
  
Theme 3: 新职业涌现话语
  定义: 新岗位 (AI 协作设计师等) 被叙述为机会
  段落: T13
  
Theme 4: 系统危机话语
  定义: AGI 推动经济体系根本变革
  段落: T09, T10, T11, T12
  
Theme 5: 个体适应主义
  定义: 把结构问题转译为个人责任
  段落: T16

关系:
  Theme 1 → Theme 2 (代际断裂导致流动停滞)
  Theme 1 ↔ Theme 5 (结构性威胁 vs 个人化解药, 张力)
  Theme 4 ⊃ Theme 1+2 (系统危机包含前两者)
  
轴心: Theme 1 (代际剪刀差)
理由: 其他 themes 都在回应"这一代年轻人怎么办"这个问题
```
