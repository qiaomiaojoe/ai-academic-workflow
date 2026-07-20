---
name: skill-forge
description: 数据 Skill 工坊 · 源材料 → 成品 skill（乔淼PhD · AI学术训练营 · AI学术工作流）。单次会话从方法学源材料造出可用 skill 的 5 阶段 2 停点链路：①提议筛选准则【停】→ ②筛选 + 7 字段结构化提取 + 自查 3 类 AI 偏差 → ③按平台规范造 skill 草稿（Claude Code 用 skill-creator + prompts/；Codex 用 init_skill.py + references/）→ ④4 控制点诊断（description 防乱触发/步骤颗粒度/硬约束/输出格式）→ ⑤落盘前总审【停】+ 落盘全局 skills 目录。Trigger on："把这本教科书 PDF 做成 skill"、"源材料造 skill"、"造一个 XX 分析 skill"、"turn this textbook chapter into a skill"、"forge a skill from these materials"。
---

# Skill Forge · 源材料 → 成品 skill（5 阶段 2 停点）

一次性完成从源材料到可用 skill 的全过程。全程只有 **2 个【停】点**等用户拍板（阶段 1 锁筛选准则、阶段 5 落盘前总审），其余阶段自动连跑。

## 调用约定（独立运行）

- 最小输入：目标 skill 主题 + 目标 skill 名（小写连字符）+ 源材料（`skill源材料/` 或用户给的任意文件/文件夹，不限格式 PDF/md/txt/docx/epub；含 源材料清单.md 时先读它了解各份定位）+ 目标平台（Claude Code / Codex，默认 Claude Code）。源材料文件夹不存在或为空 → 停下提醒先跑 `skill-workshop-plan` 或手动放料。
- 落盘：全局 skills 目录（Claude Code → `~/.claude/skills/<name>/`；Codex → `${CODEX_HOME:-$HOME/.codex}/skills/<name>/`），**独立于 paper 项目，跨项目复用，不落进项目文件夹**。
- **调用方覆盖约定**：调用方（工作台 prompt / 用户）显式给出的参数、输入路径、落盘路径与工具选择，一律覆盖本 skill 的默认；但本 skill 的方法步骤、硬约束与停点不可被省略或稀释——调用方若要求跳过某硬约束，以本 skill 为准并提示冲突。

## 全局硬约束

- ⚠️ 只在 2 个【停】点停下等回复，其余一口气连跑，不要每步都问。
- ⚠️ 分清"明显的"和"需拍板的"：明显改动（术语统一、笔误、准则的机械应用、控制点的常规改写）直接处理，总审时列清单；只有真歧义（留剔边界、真伪硬约束、破坏性拆分）才拎出来拍板。
- ⚠️ 软约束词（consider / may / could / typically / often）一律保留原词，不擅自升级为 must / CRITICAL。
- ⚠️ 脚注 / 表格说明里的硬约束必须单独列一条，不能并进正文。
- ⚠️ 页码必须实测，不允许"约 p.XXX"。
- ⚠️ 唯一不可逆的动作是写入磁盘——只发生在停 2 批准之后。

## 阶段 1 · 提议筛选准则

读全部源材料全文，结合目标主题，提议**针对这些材料 + 这个主题**的筛选准则（每条说清针对什么内容/章节模式、为什么有用或无用，不给通用准则）。多份材料时：先标各份定位（主锚 / 补充 / 对照），准则注明适用于哪份；方法论主张冲突的单独列出等拍板。输出：保留准则 5-8 条 / 剔除准则 5-8 条 / 拿不准 ≥2 条（含倾向与担心）。

→【停 1】等"按这个跑"或"改：xxx"。改了就复述改后准则再继续；确认后的准则原样写进最终素材开头存档。

## 阶段 2 · 筛选 + 结构化提取 + 自查偏差（确认准则后自动跑）

- A 相关性筛选：按准则判断每个段落 → 保留段落清单（章节|起止页|段落主题|命中准则）+ 剔除段落清单 + 段落级拿不准（≥3 条，宁可多列也别替用户做主）。
- B 结构化提取：保留段落里每个分析步骤整理成 7 字段：`## Q[编号] · [步骤名称]`——触发条件 / 输入要求 / 操作流程（1.2.3.）/ 输出标准 / 易错点（≥1 条 + 怎么防）/ 页码引用（[书名] p.XXX-XXX 实测）。
- C 自查 3 类 AI 提取偏差，分两类处理、不停：明显的（术语不一致、笔误）→ 直接改并记"我改了啥"清单；有歧义的（must/consider 误读、漏读脚注/表格小字/章末注释里的样本量门槛、显著性阈值、置信区间默认值）→ 挂起待拍板留到停 2。

在内存里把素材定稿，直接进阶段 3。

## 阶段 3 · 造 skill 草稿（自动跑，按目标平台）

- **Claude Code**：用 `anthropic-skills:skill-creator` 把定稿素材转成 skill。产物：SKILL.md（frontmatter: name + description）+ prompts/*.md（每个分析步骤一个文件）。要求：① 从素材提炼学科 context、数据类型、方法论锚（多本时主锚写主、其余列补充来源）② 按素材步骤数拆文件，**不合并相邻步骤** ③ description 含学科 context + 数据类型/输入形式 + 方法论锚 + 触发例句（中英各 ≥2-3）④ 保留素材原有硬约束，CRITICAL / REFUSE 原样不稀释 ⑤ 输出格式具体到字段（不写 "summary"）。
- **Codex**：用 Codex skill-creator 标准流程：`scripts/init_skill.py <name> --path "${CODEX_HOME:-$HOME/.codex}/skills" --resources references,scripts --interface display_name=... short_description=... default_prompt=...`（先确认落盘目录）；SKILL.md frontmatter 只含 name + description（Codex 只读 frontmatter 决定是否调用，description 必须写全触发语中英各 ≥2-3 + 学科 context + 数据类型 + 方法论锚）；步骤拆成 `references/*.md`（Codex 用 references/ 而非 prompts/），SKILL.md 正文 <500 行、渐进式披露点名引用各文件；生成/校验 `agents/openai.yaml`（`scripts/generate_openai_yaml.py`）；**不要**创建 README / INSTALLATION_GUIDE / CHANGELOG；跑 `scripts/quick_validate.py` 校验（小写+连字符，<64 字符）。

本阶段是**草稿版**，不声称完成。跑完简述：description 草稿 + 文件列表 + 最不确定的 3 个判断。直接进阶段 4。

## 阶段 4 · 4 控制点一次性诊断（自动跑，只改内存草稿，不写磁盘）

① description：诊断乱触发风险 → 给窄/中/宽 3 版，草稿直接采用推荐版（具体到学科 context、显式列数据类型、引方法论锚写 "use when … per [书名]"、触发例 ≥3 中 +3 英），另两版留停 2 切换。
② 步骤颗粒度：是否合并了多个原步骤？合并处若"输入要求"不一致或"判断准则"冲突 → **拆分属破坏性动作，不直接做，挂起到停 2** 给拆分方案。
③ 硬约束：逐文件扫软约束词——原方法论里**明确**是硬约束的直接改 CRITICAL（带判断条件+拒绝规则）；拿不准的挂起。检查是否漏掉度量层级/缺失值/显著性阈值/样本量门槛。
④ 输出格式：找抽象词（summary/result/overview），按下游场景反推结构化字段，草稿直接改写为带字段名+短示例的 markdown（末尾必有"下一步建议"字段），并给一段模拟跑通的示例输出。

完成后进阶段 5，带上全部"我改了啥"和"挂起待拍板"。

## 阶段 5 · 落盘前总审 + 落盘

一屏给用户看四样：一、草稿 skill 文件树（一层 tree）+ 最终 description 一句话；二、我自作主张改了啥（# | 在哪 | 原来 | 改成 | 类型）；三、需要拍板的存疑项（只列真歧义，没有写"无"；# | 类型 | 我的倾向 | 拿不准在哪 | 选项）；四、description 备选版（窄/宽）。

→【停 2】问："① 存疑项怎么定 ② description 用哪版 ③ 可以落盘吗？"

按回复应用最终决定，**得到落盘指令后**写到目标平台 skills 目录（同名已存在先停下问覆盖还是换名；Codex 落盘后重跑 quick_validate.py 通过才算完成）。落盘后输出：① 最终路径 + 文件树 ② 怎么用（触发例句 ≥3 中 +3 英）③ 三个后续值得自测的点。（不做 GitHub、不生成 install.sh、不写 README——本链路到落盘为止。）
