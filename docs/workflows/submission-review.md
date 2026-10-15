# 投稿与审稿工作流 · 安装与使用

本工作流面向已有稿件的人文社科作者，提供材料核实、初稿诊断、改稿、期刊要求核对、投稿包整理、审稿意见决策和返修回复七个方法。导航见 [主库 README](../../README.md)。

## 来源与版本

2026-10-15，从 [qiaomiaojoe/ai-submission-review-skills](https://github.com/qiaomiaojoe/ai-submission-review-skills) 的提交 [`7cb506e`](https://github.com/qiaomiaojoe/ai-submission-review-skills/tree/7cb506e71f77d4cd3904d50bfd5ad2935aa5054d) 合入七个 skill 目录与全部支持文件。本次保持内容和方法版本一致，未迁入业务项目或运行产物；旧仓库保留原状。

| Skill | 方法版本 | 原场景 |
|-------|----------|--------|
| `submission-task-intake` | 1.0.1 | s01 共用前置，随 s02–s07 使用 |
| `manuscript-diagnosis` | 1.1.0 | s02 初稿诊断 |
| `manuscript-revision` | 1.0.1 | s03 批准范围内改稿 |
| `journal-requirements-check` | 1.0.1 | s04 期刊要求核对 |
| `submission-package-preparation` | 1.0.1 | s05 投稿包整理 |
| `review-response-planning` | 1.0.1 | s06 审稿意见与回应决策 |
| `review-revision-response` | 1.0.1 | s07 返修改稿与逐条回复 |

原场景编号保留在方法正文中，方便已有工作台继续调用。`manuscript-diagnosis` 1.1.0 保留 Stenius et al. (2017, pp.159–161) 质性三标准及适用边界。

## 安装到论文项目

主库 `install.sh` 会遍历 `skills/`，因此全局安装时也会安装这七个完整目录。六个业务方法还明确读取**当前论文项目**中的 `skills/submission-task-intake/SKILL.md`；全局可发现不代表项目依赖已就位。

从主库取回后，将以下七个完整目录放入论文项目的 `skills/`，包括所有 `references/`。已有同名目录先比较；有差异时由用户决定跳过或更新，更新前保留备份，不自动覆盖项目定制版。

下面命令中的两个路径需替换为实际已存在的仓库与论文项目目录。命令只复制缺失目录，已有目录会跳过并提示比较。

```bash
task_repo_dir="/path/to/ai-academic-workflow"
task_project_dir="/path/to/paper-project"

test -d "$task_repo_dir/skills" || exit 1
test -d "$task_project_dir" || exit 1
mkdir -p "$task_project_dir/skills"

for skill_name in \
  submission-task-intake \
  manuscript-diagnosis \
  manuscript-revision \
  journal-requirements-check \
  submission-package-preparation \
  review-response-planning \
  review-revision-response
do
  if [ -e "$task_project_dir/skills/$skill_name" ] || [ -L "$task_project_dir/skills/$skill_name" ]; then
    printf '已有目录，先比较后决定是否更新：%s\n' "$skill_name"
    continue
  fi
  cp -R "$task_repo_dir/skills/$skill_name" "$task_project_dir/skills/"
done
```

每个业务方法都读取自身的 `references/source-basis.md`；质性诊断另读 `manuscript-diagnosis/references/qualitative-criteria.md`。不要只复制单个 `SKILL.md`。

首次调用可对执行 AI 说：

> 先核实我的论文项目根目录，实际读取项目 skills/submission-task-intake/SKILL.md、本次业务场景的 SKILL.md 及其支持文件，再按我的材料和已批准范围执行。若输入、版本或批准记录有缺项，按方法规则说明受影响步骤。

## 入口与交接

- **初稿改稿**：共用核实 → 初稿诊断 → 作者决定问题与修改范围 → 批准范围内改稿 → 作者确认稿件。
- **投稿准备**：共用核实 → 指定期刊要求核对 → 作者确认适用要求 → 投稿包整理 → 作者终审。
- **返修**：共用核实 → 审稿意见台账与回应建议 → 作者逐项决定 → 实际返修 → 据修订稿撰写回复 → 作者确认 → 期刊要求复核 → 返修包整理。

可从当前实际阶段进入，已有有效登记与明确决定按方法规则复用。AI 建议、最新轮次或材料路径存在均不能代替作者批准与实际读取。

期刊初稿或综述文章工作流的产出可作为基准稿输入，需明确具体文件、版本与确认记录。业务结果写入论文项目的 `产出/<任务标识>/`，多轮使用下一空闲 `-R<n>`，日志按原方法写入项目 `日志/分析日志.md`。本 skill 库只保存方法。

项目中的 `AGENTS.md`、`CLAUDE.md` 和 `投稿与审稿规范.md` 指使用者自己的规则文件。缺少时如实说明，依据方法的缺项规则处理；支持文件中的旧项目文件名只说明历史来源，不要求复制原作者的完整项目指令，也不能据文件名脑补内容。

## 验证边界

来源仓库记录：1.0.0 项目版做过 YAML / 结构检查、工作台生成机制及 Codex 顺序处理的模拟材料和关键边界验证；1.0.1 为发布整理；初稿诊断 1.1.0 新增质性三标准，来源记录为方法读取与缺稿件边界验证。上述为来源仓库的历史记录，本次合并不把它们记为新完成的测试。

本次合并核对范围是文件完整性、来源内容一致性、名称与版本、支持文件和共用入口依赖、README 导航，以及远端取回。没有以真实稿件验证诊断质量、改稿效果或期刊接受结果；最终提交与对外发送仍由作者决定。
