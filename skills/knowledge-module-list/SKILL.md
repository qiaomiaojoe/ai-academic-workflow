---
name: knowledge-module-list
description: 知识模块清单（乔淼PhD · AI学术训练营 · AI学术工作流 · 文献分析步骤）。跨文档分析一批文献（Zotero 集合 / 本地 PDF / 文献清单），用元数据+摘要提出覆盖 Section 1（XY 经验）与 Section 2（PV 理论）的知识模块：每个模块 = 一个概念/argument + 区分性问题 + 涉及文献与角色 + 证据假设 + 独立可运行的生成 prompt。产出 知识模块清单.md，是知识模块生成与综述蓝图的输入。Trigger on："帮我做知识模块清单"、"把这批文献分成知识模块"、"跨文档分析出模块"、"propose knowledge modules from my collection"。
---

# Knowledge Module List · 知识模块清单

跨文档分析，propose 知识模块。**只用元数据 + 摘要做框架设计与模块分配，不在这一步啃全文**（全文深读发生在 `knowledge-module-gen`）——但摘要会省略/夸大，所以每个模块必须写明"证据假设"，留给生成步骤读全文时核对。

## 调用约定（独立运行）

- 选题 context：用户给的 RQ / PXYV 一句话 > `选题.md`（选题产出）> 请用户用 1-3 句说清（研究问题 + 理论视角 + 现象语境）。
- 文献数据源（三选一）：Zotero 集合（`zotero_get_collection_items` 拉元数据、`zotero_get_item_metadata` 拉单篇摘要；本步不调 NotebookLM）/ 本地 PDF 文件夹 / 文献清单 md。Zotero 不可用 → 以清单为元数据来源、按需读本地 PDF，产出顶部注明"数据源已降级"。
- 落盘：`知识模块清单.md`（默认当前工作目录）。

## 硬约束

- Section 1（XY 经验）至少 3 个、Section 2（PV 理论）至少 3 个**有区分度**的模块——每个模块回答一个不同的问题/对话，不能把同一个 argument 切成三块凑数。
- 某 Section 凑不满 3 个有区分度的模块 → 不硬凑，明确写"该 Section 论证密度不足，建议补充 XX 方向文献"。
- Gap 不是知识模块，不在本 skill 处理（用 `research-gap-scan`）。
- 集合至少 90% 文献必须被分配；Classic + 全部 Key Texts 必含；容许 Key Texts 跨模块重复。

## 每个模块的标准结构

````
## 模块 M_n · [模块主题]
- **归属 Section**：S1 / S2
- **主题**：围绕一个概念或 argument（不是单篇文献总结）
- **区分性问题**：本模块要回答、且其他模块不回答的那个问题
- **涉及文献**（2-5 篇）
  - Author Year | Zotero key（或 PDF 文件名） | 角色（理论根基 / 经验证据 / 对话伙伴 / ...）
- **证据假设**：基于摘要，预期这些文献在全文中能提供什么证据（confidence：高/中/低）——生成步骤读全文时核对，对不上就回退本模块
- **该模块的生成 prompt**（独立可运行；围栏内是字面 spec，生成步骤逐字抽取、原样执行）：
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
````

## 下一步建议

清单产出后二选一（可都做）：① 交 `review-blueprint` 编排综述蓝图；② 直接交 `knowledge-module-gen` 逐模块读全文生成。
