---
name: skill-workshop-plan
description: 数据 Skill 工坊 · 规划 + 找料（乔淼PhD · AI学术训练营 · AI学术工作流）。诊断现成分析 skills（analyze-quantitative-data / analyze-qualitative-data）够不够、要不要造新 skill、造哪几个（带停点等确认）；确认后检索权威方法学源材料（教科书章节 / 方法学经典 / 官方手册）下载到源材料文件夹并写 源材料清单.md。造 skill 本身用 skill-forge。Trigger on："规划要造哪些数据分析 skill"、"我这个方法现成 skill 够不够"、"帮我找造 skill 的方法学材料"、"plan and source materials for a new analysis skill"。
---

# Skill Workshop Plan · 规划 + 找料

到"下料齐 + 写清单"为止，不直接造 skill（造 skill 用 `skill-forge`）。

## 调用约定（独立运行）

- 方法需求按优先级：用户直接说的方法链（如"我要跑 HLM"）> `研究设计初稿.md` + `研究设计-设计说明.md`（B3 分析框架）+ 备用 `选题.md` > 都没有 → 问用户手动给方法关键词，**不凭空假设方法**。
- 落盘：源材料与清单进 `skill源材料/`（用户指定或当前工作目录）。

## 阶段 1 · 诊断要不要造、造哪几个

1. 从方法需求抽出实际要用的分析方法链（具体到统计模型 / 编码流派 / 特定流程，不要泛泛说"做回归"）。
2. 对照现成 skills 判断覆盖度：
   - `analyze-quantitative-data`（Neuman 7e Ch12：codebook→cleaning→univariate→bivariate→elaboration→regression→inferential）
   - `analyze-qualitative-data`（Neuman 7e Ch14：开放/轴心/选择性编码 + analytic memo + outcropping + 理想型 + Mill 比较）
3. 诊断结论：**现成够用** → 指明用哪个 + 从哪步起 + 为什么够用，结束（不必造，不必下料）；**需要新建** → 逐个列：skill 主题 + 建议名（小写连字符 + 方法论锚，如 analyze-hlm-by-raudenbush）+ 一句话定位 + 现成 skill 缺在哪。

→【停】把诊断结论给用户确认：用现成的还是造新的？造哪几个？确认后再进阶段 2。

## 阶段 2 · 找料 + 下载（确认要造之后才做）

对每个确认要造的 skill，找**权威方法学源材料**（教科书章节 / 方法学经典论文 / 官方手册）：
1. 先列候选清单给用户点头：标题 / 作者·年 / 类型 / 为什么权威（领域公认度）/ 拟用章节。**不要先下载**。
2. 点头后，用环境里实际可用的检索与下载工具（`literature-search` / `scansci-pdf` / Zotero / Web 搜索；不可用的明确告知并给手动获取方式）下载到源材料文件夹，命名 `方法锚-AuthorYear.pdf`。下不到全文的记来源链接 + 替代获取方式，**绝不编造内容**。
3. 写 `源材料清单.md`：每份材料 → 对应要造的哪个 skill → 拟保留章节 → 获取状态（已下载 / 待手动）。

## 产出

skill 规划表（造不造 / 造哪几个 / 每个的主题 + 建议名 + 对应源材料）+ 已下载源材料 + 源材料清单.md + 下一步指引（用 `skill-forge`，源材料默认读本文件夹）。
