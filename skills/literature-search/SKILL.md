---
name: literature-search
description: 文献搜索完整任务入口（乔淼PhD · AI学术训练营 · AI学术工作流）。编排四个步骤 skill 跑完一次完整的文献搜索：pxyv-search 四维检索 → lit-verify 验真 → lit-pyramid 金字塔分层 → lit-pdf-zotero 获取 PDF + 入库 Zotero + 可视化，每阶段停下等确认。用户只要单独某一步（只检索/只验真/只分层/只入库）时直接用对应步骤 skill，不走本入口。Trigger on："帮我搜文献"、"完整跑一遍文献搜索"、"搜 30 篇文献入 Zotero"、"文献搜索工作流"、"search literature and import to Zotero"。
---

# Literature Search · 文献搜索任务编排

一次完整的文献搜索 = 四个步骤 skill 按序执行，**每阶段完成后输出结果表、停下等用户确认**（用户说"继续"就直接进下一阶段）：

| 阶段 | 调用 skill | 产出 |
|------|-----------|------|
| 1 检索 | `pxyv-search` | 四维候选清单（验真前） |
| 2 验真 | `lit-verify` | 验真报告 + 干净清单（含被引数） |
| 3 分层 | `lit-pyramid` | Classic / Key / Supporting 分层表 + 维度缺口表 |
| 4 落地 | `lit-pdf-zotero` | PDF 落盘 + 文献清单.md + Zotero 入库 + 可视化 HTML |

## 编排规则

- 开工前收齐参数一次问全：选题（PXYV 或一句话，一句话则先经 `topic-pxyv-parse`）、目标总篇数（默认 30）、Key 篇数（默认 5）、年限（默认近 5 年）、语言、Zotero Collection 名、额外检索要求。参数在各阶段透传给对应 skill。
- 各阶段严格按对应 skill 的 SKILL.md 协议执行，不要在本入口里即兴替代（对应 skill 不可用时，读其 SKILL.md 内容内联执行）。
- 阶段 3 出现维度缺口时，问用户是否回阶段 1 补搜（给关键词建议），补搜的增量走 2→3 再并入。
- 全程硬约束：**不编造文献，宁缺毋滥**；某维度验真后不足配额，明确说"仅找到 N 条可信文献，建议补搜"，不凑数。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。
