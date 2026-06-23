# AI 学术工作流 · Neuman 方法 × AI Prompt

> **18 个 prompt + 2 个 Claude Skill**, 把社科研究方法教科书 (Neuman 7e) 的成熟步骤翻译成可直接跑的 AI 工作流。
>
> **谁在用**：AI 学术训练营 (乔淼 PhD) 学员; 自学的社科 PhD 申请者 / 研究生新手; 任何不是统计学家但又必须做数据分析的研究者。

---

## 这是什么

数据分析是一个学科——光 Neuman 教科书的两章 (Ch 12 + Ch 14) 就 70 页, 任何细节展开都能讲一学期。

但**入门者的真实处境**是: 你 RQ 想得动, 数据收得了, 但具体到回归怎么跑、主题怎么编码, 教科书里那些专业细节都不是日常熟练的工具。

这个工作流把 **Neuman 教科书 × AI prompt × 你的判断** 拼起来:
- 📖 **教科书** — 步骤的权威来源
- 🤖 **Prompt** — 把教科书步骤翻译成 AI 能执行的指令
- 👤 **你** — 理论判断 / 度量层级 / 实质性意义

三者拼起来 → 你能开始动手做研究, 不必先学完一个学期的 stats 课。

---

## 18 个 Prompt 菜单

### 📊 定量分析 · 基于 Neuman Ch 12 (7 个)

| # | Prompt | 何时用 |
|---|--------|--------|
| 01 | [建立 Codebook](prompts/quant/01-codebook.md) | 拿到原始数据, 还没整理成可分析格式时 |
| 02 | [清洗数据](prompts/quant/02-clean-data.md) | Codebook 建好, 跑分析前 |
| 03 | [单变量分析](prompts/quant/03-univariate.md) | 看每个变量长什么样 |
| 04 | [双变量分析](prompts/quant/04-bivariate.md) | 看两个变量之间的关系 |
| 05 | [多变量阐释模型](prompts/quant/05-multivariate-elaboration.md) | 用控制变量看 bivariate 是否虚假 |
| 06 | [多元回归](prompts/quant/06-multivariate-regression.md) | 多个自变量同时影响一个因变量 |
| 07 | [推断统计](prompts/quant/07-inferential.md) | 从样本推论总体, 显著性检验 |

### 📝 定性分析 · 基于 Neuman Ch 14 (11 个)

**编码三阶段** (Strauss 1987):

| # | Prompt | 何时用 |
|---|--------|--------|
| 01 | [开放编码 Open Coding](prompts/qual/01-open-coding.md) | 第一遍读数据, 浮现初步主题 |
| 02 | [轴心编码 Axial Coding](prompts/qual/02-axial-coding.md) | 找概念之间的连接和轴心 |
| 03 | [选择编码 Selective Coding](prompts/qual/03-selective-coding.md) | 主要主题已确定, 扫全部数据找代表证据 |

**边编码边写**:

| # | Prompt |
|---|--------|
| 04 | [分析备忘录 Analytic Memo](prompts/qual/04-analytic-memo.md) |
| 05 | [Outcropping 识别](prompts/qual/05-outcropping.md) |

**七大分析策略**:

| # | Prompt | 适用情境 |
|---|--------|---------|
| 06 | [Ideal Types](prompts/qual/06-ideal-types.md) | 用纯净模型对照现实 |
| 07 | [Successive Approximation](prompts/qual/07-successive-approximation.md) | 反复迭代概念与证据 |
| 08 | [Illustrative Method](prompts/qual/08-illustrative-method.md) | 用证据填充既有理论的空盒子 |
| 09 | [Domain Analysis](prompts/qual/09-domain-analysis.md) | Spradley 文化领域分析 |
| 10 | [Mill 分析比较](prompts/qual/10-analytic-comparison-mill.md) | 多案例比较, 找共同因果 |
| 11 | [Narrative Analysis](prompts/qual/11-narrative-analysis.md) | 历史/过程性数据, 找路径依赖 |

---

## 怎么用 (两条路径)

### 🟢 路径 A · 直接复制 prompt（推荐, 任何 LLM 都行）

不需要装任何东西。

1. 在 GitHub 浏览本仓库的 `prompts/` 目录
2. 找你需要的步骤, 打开 .md 文件
3. 复制 `## ✂️ Prompt 模板` 段落
4. 粘贴到 Claude Code/Codex, 按提示填空

### 🟡 路径 B · 装成 Claude Skill（适合 Claude Desktop / Code 用户）

让 Claude 在你说"分析这份数据"时**主动建议**用合适的 prompt。

#### 一行命令安装

```bash
curl -fsSL https://raw.githubusercontent.com/qiaomiaojoe/ai-academic-workflow/main/install.sh | bash
```

#### 或手动安装

```bash
# 1. clone 本仓库
git clone https://github.com/qiaomiaojoe/ai-academic-workflow.git

# 2. 复制 skill 到 Claude 配置目录
cp -r ai-academic-workflow/skills/analyze-quantitative-data ~/.claude/skills/
cp -r ai-academic-workflow/skills/analyze-qualitative-data ~/.claude/skills/

# 3. 重启 Claude Desktop / Code 即可
```

装好后 Claude 在如下场景会主动推荐 skill:
- "我要分析这份调查数据" → `analyze-quantitative-data`
- "帮我编码这些访谈" → `analyze-qualitative-data`

---

## 推荐套餐 (按研究类型)

不需要 18 个全用。常见组合:

| 研究类型 | 用哪几个 prompt |
|---------|---------------|
| 入门**定量**研究 (回归型) | 01 → 02 → 03 → 04 → 06 (5 个) |
| 入门**定性访谈**分析 | 定性 01 → 02 → 03 → 04 (4 个) |
| **历史/比较**研究 | 定性 01 → 06 → 10 → 11 (4 个) |

---

## 设计原则

每个 prompt 都遵循以下结构:

1. **Neuman 出处** — 教科书章节 + 页码 + 原文要点
2. **必须你自己判断的部分** — AI 顶不到的边界 (理论判断 / 度量层级 / 实质性意义)
3. **Prompt 模板** — 含硬约束 (如"不许虚构数据")  + 可疑点警示 (如"R² > 0.9 可能是过拟合")
4. **执行后的下一步** — 指向工作流里其他 prompt
5. **演示填法** — 用真实数据示范怎么填空

---

## 边界声明

**这套工作流不替代**:
- 研究问题的设计 (是 RQ 阶段的工作)
- 因果识别 (需要研究设计 + 域内专家)
- 复杂方法 (mediation / SEM / multilevel) 的最终把关

> 第 6 步（检查）必须找比你懂的人帮看 30 分钟——这是入门者的现实。AI + 教科书框架能把你从"完全不会"推到"能问出有质量的问题"。

---

## 引用

如果这套工作流帮到了你的研究, 引用:

```
乔淼 (2026). AI 学术工作流: 基于 Neuman 方法的 AI Prompt 库.
https://github.com/qiaomiaojoe/ai-academic-workflow
```

教科书原始出处:
```
Neuman, W. L. (2014). Social Research Methods: Qualitative and Quantitative
Approaches (7th ed.). Pearson Education Limited.
```

## License

[CC BY 4.0](LICENSE) — 可以自由使用 / 修改 / 再分发, 保留原作者署名即可。
