# 05 · 多变量分析 · 阐释模型 (Elaboration Paradigm)

> **Neuman 出处**：Ch 12, "The Elaboration Model of Percentaged Tables" · p.417-420
>
> **何时用**：bivariate 看到关系后, 想知道这关系**是不是虚假的** (引入控制变量)
>
> **前置**：[04 · 双变量分析](04-bivariate.md) 完成, bivariate 关系已确认

---

## 📖 Neuman 怎么讲

**核心问题**：bivariate 显示 X 与 Y 相关, 但**会不会是因为某个第三变量 Z 同时影响 X 和 Y**？

**做法**：把 bivariate 表按控制变量 Z 拆成几个 partial tables, 然后看每个 partial 里 X-Y 关系**怎么变**。

Neuman 说有 **5 种 pattern**:

| Pattern | partial 表里 X-Y 关系 | 含义 |
|---------|----------------------|------|
| **Replication** | 所有 partial 都和原 bivariate 一样 | 控制变量**没影响**, 原关系成立 |
| **Specification** | 只有某一个 partial 里关系存在 | 关系只在 Z 的特定取值下成立 |
| **Interpretation** | partial 里关系消失 (Z 在 X 和 Y 之间) | Z 是**中介变量**, 解释了 X 怎么导致 Y |
| **Explanation** | partial 里关系消失 (Z 在 X 之前) | 原 bivariate **是虚假的**, Z 才是真原因 |
| **Suppressor** | bivariate 显示无关, 但 partial 里有关系 | Z 抑制了真实关系 |

> **Interpretation 和 Explanation 长得一样**——区别在 Z 在因果链的位置 (中间 vs 前面)。这要靠**理论判断**, 不靠数据。

---

## ⚠️ 必须你自己判断的部分

- **Z 在因果链哪个位置**：在 X 前面 (explanation) 还是在 X 和 Y 之间 (interpretation)? 这是理论判断
- **样本量是否够拆**：每个 partial 至少要 ~50 个 case (Neuman: avg 5 per cell)
- **控制变量怎么选**：选的是真混淆变量, 还是后果变量? 后者会过度控制

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 12 的 elaboration paradigm 做多变量分析。

【已确认的 bivariate 关系】
IV: [X 名]
DV: [Y 名]
关联度量值: [γ = 0.X / r = 0.X / 等]
方向: [positive / negative]

【控制变量 Z】[填一个, 一次只控一个]
Z 名: [...]
Z 的度量层级: [nominal / ordinal / interval]
Z 的类别数: [如 2 / 3 / 4 — Neuman 建议不超过 4]

【Z 在因果链的位置】（理论判断, 必填）
[ ] Z 在 X 之前 (potential confounder, 测试 explanation pattern)
[ ] Z 在 X 和 Y 之间 (potential mediator, 测试 interpretation pattern)
[ ] 不确定 (两种都跑, 由我判断)

【请帮我做】

1. 跑 bivariate 关系 in 每个 Z 的类别 (即 partial tables)
2. 报告每个 partial 的关联度量 + 样本量
3. 根据 5 种 pattern 判断哪个最匹配:
   - Replication: 所有 partial 与 bivariate 一致
   - Specification: 只有某 partial 显著
   - Interpretation/Explanation: partial 里关系消失
   - Suppressor: bivariate 无关但 partial 有关
4. **明确告诉我**:
   - Pattern 名
   - 这意味着什么 (一句话学术解读)
   - **如果是 Interpretation 或 Explanation, 提醒我"区分这两个需要理论判断, 不能靠数据"**

【硬约束】
- 每个 partial 至少 50 case, 否则警告样本量不足
- 不要直接说"X 因果导致 Y"——elaboration 不能证明因果
- 工具: [Python / R / 跑回归 with interaction term]

【可疑点警示】
- 如果 Z 类别 > 4: 警告我 partial 太多难解读
- 如果 partial 之间样本量极不均衡: 警告 selection bias
```

---

## 💡 执行后的下一步

- Replication → bivariate 关系稳健, 可以写进 results
- Specification → 写"X-Y 关系仅在 Z=... 时成立", 这是有趣发现
- Interpretation → 进一步做正式的 mediation analysis (Baron-Kenny / PROCESS / lavaan)
- Explanation → 原 bivariate 是虚假的, 要重写理论
- Suppressor → 罕见但重要, 报告出来
- 控制多个 Z 同时 → [06 · 多元回归](06-multivariate-regression.md)

---

## 📌 WVS 演示填法

```
【bivariate 关系】
IV: knowledge_worker
DV: Q159 (科技机会)
γ ≈ -0.02 (基本没关系)

【控制变量 Z】Q287 (收入十分位)
Z 在因果链位置: **不确定**——
- 可能在 KW 之前 (家庭背景影响职业 + 影响态度) → explanation
- 可能在 KW 之后 (KW 决定收入 + 影响态度) → interpretation
两种都跑, 看 pattern

【预期】可能是 explanation pattern——KW 与 Q159 在 partial 里也很弱, 因为 Q287 才是真正驱动力
```
