# 03 · 选择编码 (Selective Coding)

> **Neuman 出处**：Ch 14, "Selective Coding" · p.484
>
> **何时用**：主要 themes 已稳定, 做最后一遍扫全部数据找代表证据
>
> **前置**：[02 · 轴心编码](02-axial-coding.md) 完成, themes 已不再大幅变动

---

## 📖 Neuman 怎么讲

> By the time you are ready for this last pass through the data, you have identified the major themes. Selective coding involves **scanning all the data and previous codes**, looking selectively for cases that **illustrate themes**, and making comparisons after most or all data collection has been completed.

> "Selective coding should begin after concepts have been well developed and several core generalizations or ideas have been identified."

**目的**:
1. 确认 themes 在全部数据里都站得住
2. 为每个 theme 找最强的代表证据 (representative quote / vignette)
3. 找出 theme 之间的细致区别
4. 准备写作素材

> "During selective coding, major themes or concepts ultimately guide the search process. You reorganize specific themes identified in earlier coding and elaborate more than one major theme."

---

## ⚠️ 必须你自己判断的部分

- **代表证据怎么选**: 锚定型 / 极端型 / 矛盾型——每种功能不同
- **theme 在数据里"够强"的标准**: 至少几段支持? 这是你的研究规范
- **是否要回到 axial coding**: 如果发现新的反例或张力, 不要硬上, 回头修

---

## ✂️ Prompt 模板

```
我要按 Strauss (1987) / Neuman (2014) Ch 14 做选择编码。

【主要 themes】[贴上一步定下的 3-7 个 themes + 定义 + 关系]
【全部数据】[贴]

【请按以下规则做】

对每个 theme:

1. **覆盖核查 (saturation check)**
   - 在全部数据里再扫一遍, 列出**所有**支持该 theme 的段落 ID
   - 不只看上一步标记过的——可能有遗漏
   - 报: 该 theme 涉及多少段 / 占比 X%

2. **代表证据挑选**
   每个 theme 挑 1-3 段, 标功能:
   - **锚定型 (anchor)**: 最核心地体现 theme 含义
   - **极端型 (extreme)**: theme 的极端表达
   - **矛盾型 (counter)**: theme 内部的张力 / 反例

3. **theme 之间的细致区分**
   - 边界模糊的 themes 之间, 找 1-2 个**只属于其中一个**的段落作为"分水岭"
   - 这帮助后面写作时分清

4. **未编码段处理**
   - 列出**没有被任何 theme 覆盖**的段落
   - 对每段判断:
     · 真的与 RQ 无关 (报告"discarded as off-topic")
     · 是新 theme 萌芽 (建议是否回到 axial coding)
     · 是反例 (建议进入 negative case 分析, 见 prompt 10)

【输出格式】
对每个 theme:
| Theme | Anchor quote | Function | Segment ID |

末尾:
- 全数据覆盖率: X% 段落 mapped to themes
- Saturation 评估: 是否还需更多数据?
- 未覆盖段落清单 + 处理建议

【硬约束】
- Quote 必须**逐字**, 不许改写
- 每段 quote 必须标 ID + 长度 (不超过 100 字, 太长就截短)
- 不许虚构段落
- 如某 theme 全数据扫完只有 1-2 段支持, 警告"saturation 不足"
```

---

## 💡 执行后的下一步

- 所有 themes saturation 都够 + quotes 都选好 → 开始写 findings 段落
- 某 theme saturation 不足 → 收集更多数据 OR 删掉该 theme OR 合并到其他
- 发现大量未覆盖段 → 回 [02 · 轴心编码](02-axial-coding.md), 是不是有遗漏的 theme
- 发现反例 → [10 · Negative Case](10-analytic-comparison-mill.md) 处理

---

## 📌 36kr 演示预期产出

```
Theme 1: 代际剪刀差
  覆盖: T01, T02, T03, T05 (5/16 = 31%)
  Anchor (锚定): T02 "完美替代——原本需要实习生整理的会议纪要 AI 秒出..."
    Function: 最核心地体现"初级岗位结构性消失"
  Extreme: T05 "金饭碗可能直接蒸发" (Amodei 警告 50% 入门白领消失)
    Function: theme 的极端预测形态

Theme 5: 个体适应主义
  覆盖: T16 (1/16 = 6%) ← saturation 不足!
  建议: 收集更多"成为 AI 需要的人"类讨论, 或合并到 Theme 3 (新职业涌现)
```
