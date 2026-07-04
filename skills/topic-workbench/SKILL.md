---
name: topic-workbench
description: 「AI学术训练营」选题工作流总入口（乔淼PhD · AI学术工作流）。当用户想选题但没说用哪种模式时，先分诊：判断/确认最贴近的选题模式（①理论诠释 ②假设检验 ③概念建构 ④方法驱动），然后转入对应的独立 skill 执行；用户已有现成选题只需结构化时转 topic-pxyv-parse。Trigger on："帮我选题"、"选题工作流"、"我想做一个关于…的研究，帮我把选题磨出来"、"help me develop a research topic"、"topic coaching"。
---

# Topic Workbench · 选题分诊入口

用户想选题但没指定模式时，从这里进。本 skill 只做两件事：**判型 → 转对应 skill**。

## 分诊规则

先根据用户的输入（研究方向 / 问题描述 / 方法取向）判断最贴近的选题模式，给出你的判断 + 一句话理由，向用户确认（用户可改选）：

| 模式 | 适用信号 | 转入 skill |
|------|---------|-----------|
| ① 理论诠释 | 想用某个理论视角诠释一个现象；定性 / 批判取向 | `topic-theory-interpretation` |
| ② 假设检验 | 关心 X 对 Y 的影响、中介 / 调节；定量取向 | `topic-hypothesis-testing` |
| ③ 概念建构 | 现象是新的，现有理论命名不了，需要造概念 | `topic-concept-construction` |
| ④ 方法驱动 | 手里有方法 / 数据，想解决领域已知局限 | `topic-method-driven` |

特殊入口：
- 用户**已有现成选题 / 研究计划**，只需要结构化成 PXYV（好接文献搜索等下游）→ 转 `topic-pxyv-parse`，不必重跑三阶段。
- 用户说「续跑阶段 B / C」→ 问清（或从已存盘的 `选题-A-mining.md` 锚块读出）是哪个 mode，转对应 mode skill 的续跑入口。

## 判型提示

- 跨 mode 情况：选最贴近的一个走完，之后可补充另一 mode 视角。
- 用户完全说不清方向时，先用 2-3 个问题把「现象 / 疑问 / 手头资源」问出来再判型，不要凭空替用户选。
- 确认模式后，按对应 skill 的协议执行（读该 skill 的 SKILL.md 与 references/stages.md），不要在本 skill 里即兴发挥选题流程。
