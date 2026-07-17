---
name: research-design
description: 研究设计完整任务入口（乔淼PhD · AI学术训练营 · AI学术工作流）。编排两个步骤 skill 跑完一次完整研究设计：methods-map 方法地图 + 2-3 方案（末尾 CHECKPOINT 用户选）→ methodology-draft 展开为研究设计初稿 + 设计说明。只要单独某一步（只扫方法地图 / 已有方案只写初稿）时直接用对应步骤 skill。Trigger on："帮我做研究设计"、"研究设计工作流"、"design my study"、"from methods survey to methodology draft"。
---

# Research Design · 研究设计任务编排

一次完整的研究设计 = 两个步骤 skill 按序执行，中间一个必停 CHECKPOINT：

| 阶段 | 调用 skill | 产出 |
|------|-----------|------|
| A 方法地图 + 方案 | `methods-map` | 方法地图.md（含 methodology_plugin YAML + 2-3 方案）+ 方法地图.html |
| ⛔ CHECKPOINT | — | 停下等用户选方案 / 给修改意见，未回复不得进 B |
| B 展开初稿 | `methodology-draft` | 研究设计初稿.md（干净版）+ 研究设计-设计说明.md |

## 编排规则

- 开工前一次问齐：RQ（或读 `选题.md`）、学科、文献语料来源与主数据通道、方法/软件/样本/时间线偏好。参数透传给步骤 skill。
- 各阶段严格按对应 skill 协议执行；步骤 skill 不可用时读其 SKILL.md 内联执行。
- 全程硬约束以两个步骤 skill 内的为准（置信度标注 / 不编造 / 固定落盘路径）。
