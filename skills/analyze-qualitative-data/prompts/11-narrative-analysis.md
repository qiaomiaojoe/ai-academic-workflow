# 11 · Narrative Analysis (叙事分析)

> **Neuman 出处**：Ch 14, "Narrative Analysis" · p.494-498
>
> **何时用**：数据是过程性的、有时间顺序的——访谈生命史 / 事件序列 / 历史档案
>
> **前置**：叙事数据已收集

---

## 📖 Neuman 怎么讲

> Narrative analysis... A method for analyzing data and providing an explanation, takes several forms. It is called analytic narrative, narrative explanation, narrative structural analysis, or sequence analysis.

**叙事六要素 (Expansion Box 6)**:
1. 讲一个故事 (展开的事件 from a point of view)
2. 有运动 / 过程感 (前后状态变化)
3. 含相互关系 / 复杂语境
4. 涉及个体或群体的行动和选择
5. 有连贯性 (whole 站得住)
6. 时间顺序 (chain of events)

**三个 analytic tools** (p.497-498):

**1. Path Dependency (路径依赖)**
> The way that a unique beginning can trigger a sequence of events and create a deterministic path.
>
> - 起点很关键, 后面的事件被前面约束
> - 例: QWERTY 键盘——早期机械限制 → 形成路径 → 后面就算更优方案也难替代
> - 两种: self-reinforcing (惯性增强) / reactive sequence (摆锤式反应)

**2. Periodization (分期)**
> Dividing the flow of time in social reality into segments or periods.
>
> - 时间不是线性流动, 而是断裂的"时期"
> - 分期不是事实, 是必要假设——但**必须看证据再调整**
> - 注意: "the breaks between periods are artificial; they are not natural in history, but they are not arbitrary"

**3. Historical Contingency (历史偶然性)**
> Refers to a unique combination of particular factors or specific circumstances that may not be repeated.
>
> - 解释一个**结局**为什么发生 = 找出当时的特殊组合
> - 不是律理 (law-like), 而是"在那个特定时空下"
> - **Critical juncture (关键节点)**: 历史叉路口, 选择一条后另一条就难走了

---

## ⚠️ 必须你自己判断的部分

- **起点选哪里**：影响 path dependency 的解读
- **分期的边界**: 1980-1989 vs 1985-1995, 不同分期讲不同故事
- **是 historical contingency 还是普遍因果**: 这是元理论判断

---

## ✂️ Prompt 模板

```
我要按 Neuman (2014) Ch 14 / Mahoney 的 narrative analysis 分析数据。

【RQ】[一句话, 必须涉及"过程"/"序列"/"为什么这样发展"]

【数据类型】[ ] 生命史访谈 [ ] 历史档案 [ ] 事件年表 [ ] 多源混合
【数据】[贴, 每事件标 ID + 时间]

【关注的 outcome / 终点】[一句话——你想解释什么的发生]

【请按以下三件做】

1. **Path Dependency 分析**
   - 找 starting point (trigger event): 哪个事件触发了后续序列?
   - 描述 chain of events: trigger → event 2 → event 3 → ... → outcome
   - 标注每一环的"约束力": event N 怎么限制 event N+1 的可能性?
   - 类型判断: 是 self-reinforcing (惯性) 还是 reactive sequence (摆锤)?

2. **Periodization (分期)**
   - 提议 2-5 个 period
   - 每 period 给一个名 + 起止时间
   - 每 period 的"organizing logic": 这段时期主导逻辑是什么?
   - 跨 period 的"break": 什么事件标志着 period 切换?
   - **警告**: 如果几个 period 看起来是连续的 (找不到 break), 是不是不该分?

3. **Historical Contingency 识别**
   - 哪个时点是"critical juncture" (关键叉路口)?
   - 在那个 juncture, 还有哪些 alternative paths 没走?
   - 走了这条而不是那条, 是因为什么 unique combination?
   - 这种组合是 reproducible 还是 idiosyncratic?

4. **整合 narrative explanation**
   把上述拼成一段叙事:
   - 起点 (trigger)
   - 序列 (chain)
   - 关键节点 (critical juncture) + 选择
   - 路径锁定 (path dependency)
   - outcome

【输出】
- 时间线 (ASCII 或 Mermaid timeline)
- Periodization 表
- Critical juncture 标注
- 一段 200-400 字的整合叙事

【硬约束】
- 事件必须有数据依据 (引用原文 / 段落 ID)
- 不许"事后诸葛亮"——避免线性归因 (X 一定导致 Y, 如果只是后面发生)
- "alternative path" 必须有证据支持 (如 "当时讨论过 alternative B 但被否决"), 不许凭空想
- Periodization break 要有具体证据 (某事件后讨论方式 / 行动者明显变化)
```

---

## 💡 执行后的下一步

- 叙事完整 → 写历史/过程章节
- 多个 cases 想做比较叙事 → [10 · Mill 比较](10-analytic-comparison-mill.md)
- 叙事核心是某文化群体的 sense-making → [09 · Domain Analysis](09-domain-analysis.md) 看他们的语言
- 想用既有过程理论检验 → [08 · Illustrative Method](08-illustrative-method.md)

---

## 📌 演示填法 (假设案例)

```
【RQ】中国某高校"国际化"政策 2010-2025 是怎么演变到现状的?
【数据】15 份政策文件 + 8 个高管访谈 (按时间排序)

Path Dependency:
- Trigger: 2010 教育部"双一流"动议
- Chain: 2010 政策 → 2012 招收外籍学生指标 → 2015 设立 IEC → 2018 中外合办项目 → 2020 疫情期间国际网络断 → 2023 转向"在地国际化"

Periodization:
- Period 1: 2010-2015 "总量扩张期" (organizing logic: 国际生数量 KPI)
- Period 2: 2015-2020 "结构升级期" (logic: 项目质量 + 排名)
- Period 3: 2020-2025 "在地国际化期" (logic: 替代物理流动)
Break: 2020 疫情, 既有 KPI 失效

Historical Contingency:
- Critical juncture: 2020 春季初疫情爆发
- Alternative path: 暂停国际化指标 (有讨论但被否决)
- 实走路径: 重新定义"国际化"为虚拟+本地
- 这是 unique combination of: 疫情 + 既有 IEC 团队 + 双一流压力 + 数字技术成熟
```
