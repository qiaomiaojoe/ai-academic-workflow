---
name: review-blueprint
description: 综述蓝图（乔淼PhD · AI学术训练营 · AI学术工作流 · 文献分析步骤）。把知识模块清单编排成综述的逻辑结构：每个 Section 的标题 + 核心 argument + 模块出场序列 + 模块间逻辑（前置依赖/并列对照/对话张力）+ 段落写作提示，并渲染成自包含 HTML 可视化自动打开。Section 3 的 gap 内容由 research-gap-scan 填入。Trigger on："帮我编综述蓝图"、"把知识模块编排成综述结构"、"review blueprint"、"organize my modules into a review outline"。
---

# Review Blueprint · 综述蓝图

把知识模块编排成综述的逻辑结构（框架 + 模块映射）。

## 调用约定（独立运行）

- 输入：知识模块清单（项目 `02_文献/知识模块清单.md`，或用户给的模块列表——没有就先跑 `knowledge-module-list`）+ 选题 context（RQ / PXYV，一句话即可）。
- 落盘：项目内 `02_文献/综述蓝图.md` + `02_文献/综述蓝图.html`；项目外当前目录同名。

## 蓝图结构

每个 Section 下直接给：

```
# Section 1 · XY 维度 · 经验
- 标题（10-15 字）
- 核心 argument（一句话）
- 模块出场序列：M_a → M_b → M_c（按论证顺序，引用清单里的模块）
- 模块间逻辑（前置依赖 / 并列对照 / 对话张力，可用 ASCII 图）
- 段落写作提示：组装初稿时怎么处理各模块

# Section 2 · PV 维度 · 理论
（同上结构；含理论谱系继承/冲突、与概念近邻的关系）

# Section 3 · Gap & 定位
（调用 research-gap-scan 产出后填入；用户不需要 gap 时此节标注"待 gap 扫描"）
```

## 可视化（综述蓝图.html · 自动打开）

自包含 HTML（所有 CSS 内联，无外部依赖），用于教学/讨论：
- 顶部 header：选题标题 + Section 数 / 模块数 / gap 数
- 三个 Section 区块：核心 argument + 模块卡片序列（M_n 标题 + 角色 + 区分性问题）+ 模块间箭头
- Section 3 单独展示 gap 列表（标注类型）
- 配色：背景 #fafaf7 / 纸面 #fff / 文字 #1a1a1a / 辅助 #6b6b6b / 边线 #e0ddd6；PingFang SC 系；行高 1.7；max-width 1100px

渲染完自动打开（路径含空格带引号）：macOS `open "…"` / Windows `start "" "…"` / Linux `xdg-open "…"`。

## 下一步建议

① Section 3 还空着 → 跑 `research-gap-scan`；② 蓝图定了 → 跑 `knowledge-module-gen` 逐模块生成，再 `review-draft-assembly` 组装初稿。
