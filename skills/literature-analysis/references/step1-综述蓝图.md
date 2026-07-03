# 步骤 1 · 跨文档分析（综述蓝图 + 知识模块清单 + 可视化）

基于「选题 context + 文献数据源的全部文献」做跨文档分析，产出两份 .md + 一份 .html 可视化。

【全文利用规则】本步骤只做"框架设计 + 模块分配"，用元数据 + 摘要即可，不要在这一步啃全文（会吃满上下文）——真正的全文深读发生在步骤 2。但摘要会省略/夸大，所以每个模块必须写明"证据假设"，留给步骤 2 读全文时核对。

调用工具：优先 Zotero MCP（本步不调 NotebookLM）。用 zotero_get_collection_items 拉元数据、zotero_get_item_metadata 拉单篇摘要。Zotero 不可用 → 以文献清单为元数据来源，按需读本地 PDF，产出顶部注明"数据源已降级"。

## Part A · 知识模块清单（输出：知识模块清单.md）

propose 覆盖 Section 1（XY 经验）与 Section 2（PV 理论）的知识模块。

硬约束：
- Section 1 至少 3 个、Section 2 至少 3 个"有区分度"的模块——每个模块回答一个不同的问题/对话，不能把同一个 argument 切成三块凑数。
- 若某 Section 凑不满 3 个有区分度的模块，不要硬凑：明确写"该 Section 论证密度不足，建议补充 XX 方向文献"。
- Section 3（Gap）不是知识模块，单独在 Part C 处理。

每个模块的标准结构：

```
## 模块 M_n · [模块主题]
- **归属 Section**：S1 / S2
- **主题**：围绕一个概念或 argument（不是单篇文献总结）
- **区分性问题**：本模块要回答、且其他模块不回答的那个问题
- **涉及文献**（2-5 篇）
  - Author Year | Zotero key（或 PDF 文件名） | 角色（理论根基 / 经验证据 / 对话伙伴 / ...）
- **证据假设**：基于摘要，预期这些文献在全文中能提供什么证据（confidence：高/中/低）——步骤 2 读全文时核对，对不上就回退本模块
- **该模块的生成 prompt**（独立可运行；围栏内是字面 spec，步骤 2 逐字抽取、原样执行）：
  ```
  关键问题：[这个模块要回答什么]

  期望输出结构：
  1. [子结构 1，如"概念定义/操作化对比表"]
  2. [子结构 2，如"3 个核心 finding 含 inline citation + 页码"]
  3. [子结构 3，如"该模块对综述 Section X 的具体贡献"]

  约束：所有引用含 Zotero key + 页码（找不到页码就标注，不要编造）；
        Author Year 标准格式；
        字数 ≈500 词英文 / 800 字中文（证据不足则标注偏薄，不灌水）。
  ```
```

约束：集合至少 90% 文献必须被分配；Classic + 全部 Key Texts 必含；容许 Key Texts 跨模块重复。

## Part B · 综述蓝图（输出：综述蓝图.md）

把框架与模块编排写成一份蓝图，每个 Section 下直接给：

```
# Section 1 · XY 维度 · 经验
- 标题（10-15 字）
- 核心 argument（一句话）
- 模块出场序列：M_a → M_b → M_c（按论证顺序，引用 Part A 的模块）
- 模块间逻辑（前置依赖 / 并列对照 / 对话张力，可用 ASCII 图）
- 段落写作提示：步骤 3 写这一节时怎么处理各模块

# Section 2 · PV 维度 · 理论
（同上结构；含理论谱系继承/冲突、与概念近邻的关系）

# Section 3 · Gap & 定位
（内容由 Part C 的 gap 扫描填入）
```

## Part C · Gap 识别（组合扫描 · 最后做，写入综述蓝图.md 的 Section 3）

Gap 识别必须在 Part A/B 完成后做——因为"新组合"要先知道已有组合。基本思路：选题关键词 P、X、Y 之间的新组合。

1. 展开 P 的近邻概念、X 的操作化变体、Y 的操作化变体。
2. 用一张组合表枚举集合已覆盖的 (X,Y) / (P,X) / (P,Y) 组合（依据 Part A 的模块）。
3. 标出空白 / 弱覆盖的格子 = 候选 gap。
4. 每个候选 gap 过"三问反驳"（防伪 gap）：
   a. 这是真空白，还是已被验证为无意义 / 已被否证？
   b. 本研究 RQ 是否正好落在这个格子？
   c. 文献里有没有人明确呼吁过这个方向？
5. 通过三问的，按类型归类：empirical / contextual（人群·情境）/ theoretical（取自 S2 理论冲突）/ methodological。
6. 输出 Section 3：核心 gap（3-5 个，具体且通过三问）+ 本研究 RQ 如何回应 + 定位陈述（1 段）。

## 额外产出 · 综述蓝图.html（可视化 · 自动打开）

自包含 HTML（所有 CSS 内联，无外部依赖），用于教学/讨论：
- 顶部 header：选题标题 + Section 数 / 模块数 / gap 数
- 三个 Section 区块，每个含：核心 argument + 模块卡片序列（M_n 标题 + 角色 + 区分性问题）+ 模块间箭头
- Section 3 单独展示 gap 列表（标注 empirical / contextual / theoretical / methodological 类型）
- 配色温和：背景 #fafaf7 / 纸面 #fff / 文字 #1a1a1a / 辅助 #6b6b6b / 边线 #e0ddd6；字体 PingFang SC 系；行高 1.7；max-width 1100px

渲染完成后自动在浏览器打开（路径含空格务必带引号）：macOS `open "…"`；Windows `start "" "…"`；Linux `xdg-open "…"`。

## 输出清单

1. 知识模块清单.md　2. 综述蓝图.md（含 Section 3 gap）　3. 综述蓝图.html（并自动打开）
