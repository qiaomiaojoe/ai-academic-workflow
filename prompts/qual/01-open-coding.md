# 01 · 开放编码 (Open Coding)

> **Neuman 出处**：Ch 14, "Coding Qualitative Data" → "Open coding" · p.481-482
>
> **何时用**：第一遍读原始定性数据 (访谈逐字稿 / 田野笔记 / 历史档案 / 公开文本), 让初步主题浮现
>
> **前置**：定性数据已收集 / 已转写

---

## 📖 Neuman 怎么讲

Strauss (1987) 定义了三种定性编码, **必须按顺序做**:
1. **Open coding** ← 本 prompt
2. Axial coding
3. Selective coding

> "You preform open coding during a first pass through recently collected data. You locate themes and assign initial codes in your first attempt to condense the mass of data into categories."

> "The themes are at a low level of abstraction and come from your initial research question, concepts in the literature, terms used by members in the social setting, or new thoughts stimulated by an immersion in the data."

**好的主题码 (Boyatzis 1998) 五要素**:
1. **Label** — 一到三词的名字
2. **Definition** — 主要特征
3. **Flag** — 怎么在数据里识别它
4. **Qualifications** — 边界条件 / 排除项
5. **Example** — 一个具体例子

**三个常见错误 (Schwandt 1997)**:
1. 停留在描述层, 不到分析
2. 把编码当机械流程
3. 编码僵化不可改

---

## ⚠️ 必须你自己判断的部分

- **理论关切**：什么算"重要"是研究者决定的, 不是 AI
- **抽象层级**：码停在描述还是上升到分析? 这是你的研究品味
- **保留 vs 舍弃 in-vivo 词汇**: 受访者用的原话有时是金子, 有时是误导

---

## ✂️ Prompt 模板

```
我要按 Strauss (1987) / Neuman (2014) Ch 14 的方法做开放编码。

【研究问题 RQ】
[填一句话]

【理论关切】
[一句话——你想看什么概念怎么呈现, 如:
"sociotechnical imaginary 怎么呈现" / 
"权力关系怎么在话语里体现" /
"留学生身份认同的协商策略"]

【数据来源】
[填: N 个访谈 / N 段田野笔记 / N 篇公开文本 / 历史档案]
数据形态: [中文/英文/混杂; 段落级/句子级]

【数据】
[贴: 全部数据, 或者每段加一个 ID 标号 (T01, T02...)]

【请按以下规则编码】

对每段数据 (或每个有意义的 chunk):

1. **In-vivo code** (1-3 个)
   - 用受访者/文本里的**原词**
   - 必须在原文找得到

2. **Analytic code** (1-2 个)
   - 你抽象出的概念
   - 比 in-vivo 更高一层
   - 与 RQ / 理论关切相关

3. **Boyatzis 五要素** (对每个 analytic code)
   - Label: 1-3 词
   - Definition: 1 句话
   - Flag: 怎么识别 (如 "出现 X 词或类似句式")
   - Qualifications: 边界 / 排除
   - Example: 这段里的具体证据

4. **Memo 提示** (一句话)
   - 这段让你想到了什么? (后面写 analytic memo 用)

【输出格式】
每段一个 JSON object:
{
  "id": "T01",
  "in_vivo": ["...", "..."],
  "analytic_codes": [
    {"label": "...", "definition": "...", "flag": "...", "example": "..."}
  ],
  "memo_seed": "..."
}

【硬约束】
- **每个 code 必须能在原文找到依据**
- 不许总结, 不许评价
- 不许编造数据里没有的细节
- 在描述层 (T01 说 "失业") 之外, 努力上升到分析层 (T01 例示 "代际机会断裂")
- 如果某段无法编码, 标 "uncodeable" + 写明原因

【可疑点警示】
跑完后主动告诉我:
- 哪些 code 只在 1 段出现 (可能是 fluke, 也可能是边缘信号)
- 哪些 code 在多段重复 (potential theme, 后面 axial coding 重点关注)
- 哪些段几乎全是描述层 (没产出 analytic code, 可能是数据稀薄或者你的关切对不上)
```

---

## 💡 执行后的下一步

- 全部数据编完一遍 → [02 · 轴心编码](02-axial-coding.md) 找概念之间的连接
- 同时写 → [04 · 分析备忘录](04-analytic-memo.md) 把 memo_seed 展开成理论备忘
- 如果发现数据稀薄 → 可能要回头补数据

---

## 📌 36kr 演示填法

```
【RQ】中国财经媒体 2025 年关于 AI×知识工作者的 sociotechnical imaginary 是什么?
【理论关切】"机会"和"威胁"两种话语如何被分配给不同位置的工作者
【数据】16 段 36kr 报道节选 (T01-T16, 已存 corpus.json)
【期望编码示例】
T01: 
  in_vivo: ["入职率掉了14%", "新人连门都摸不到"]
  analytic: [
    {label: "代际机会断裂", definition: "AI 不裁老员工但关闭新人入门通道", 
     flag: "提到入职/起薪/junior+负面", example: "新人连门都摸不到"}
  ]
  memo_seed: "这种'结构性挤压新人'的话语和 1980s 年代日本的 windfall 现象有平行?"
```
