# Mode ④ 方法驱动 · 三阶段详细步骤

范例锚论文：Esteva et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*, 542(7639), 115-118.

## STAGE A · 挖掘（6 步走）

A.1 故事 / 领域局限（mode ④ 不是个人故事，把"矛盾"换成"领域局限 + 方法机会"）
- 教学法：教练**先一次性把范例锚的完整五步端给用户看**，**然后一步一问**，每步**先给 2-3 个草案候选**（基于用户的「问题/现象描述」推导），用户选 / 改 / 重写
- 完整范例（Esteva 2017，一次性展示）：
  - 现象 = 皮肤癌早期诊断依赖皮肤科医生的视觉判断，但全球皮肤科医生稀缺，基层资源不足
  - 主角 = 皮肤癌早期患者 + 皮肤科医生
  - 局限 = 视觉诊断准确度由医生经验决定；专家 vs 实习医生差异极大；普通人无法自查
  - 证据 = 美国每年 540 万新发皮肤癌，1/5 美国人一生患病；但专家级诊断只在大医院可得
  - 一幕 = 一个偏远地区患者拿手机拍下皮肤可疑斑点 — 能不能让 AI 给出专家级判断？
- 一步一问（每步教练先给 2-3 个草案，用户选/改）：① 现象 ② 主角 ③ 局限（现有最好方法只能做到什么）④ 证据 ⑤ 一幕

A.2 方法机会
- 范例：深度卷积神经网络（CNN）在 ImageNet 已证明能"看图像" — 能不能用同样的网络看皮肤图，达到皮肤科医生水平？
- 教练任务：给 2-3 个方法机会草案（我的方法/数据怎么解决这个局限），用户选/改
- so-what 起草（教练做，用户只确认）：① 领域增量句：这项研究将把领域对 [Y 问题] 的能力/认识推进到什么程度；② 现实利害句：哪一类具体人群/机构的决策或实践会因此不同（不接受"全社会"）——双句进 C 的 V 表述与锚块 SW 字段
- 假设挑战识别（教练主动做）：检查故事里是否有"现象与领域主流假设相抵触"的信号；若有，把「挑战假设版」作为候选之一端出来（problematization, Alvesson & Sandberg 2011, AMR 36(2): 247-271），说明它与「填空白版」的意义差别，用户选

A.3 学科范式 P
- 范例：P = 临床医学（皮肤科）+ 深度学习（CNN，特别是 Inception v3 架构）
  两者结合的范式：把医学影像分类 reframe 为标准 ImageNet-style 分类问题
- 教练任务：给 2-3 个候选 P（每个简述方法假设 + 适合的科学问题），用户选

A.4 双 V 拆分（mode ④ 核心）
- 范例：
  - 方法 V = ImageNet 预训练 CNN 迁移到皮肤癌分类 — transfer learning 在医学影像的应用范式
  - 实证 V = AI 系统在大规模真实数据上达到皮肤科医生水平（21 名医生 vs CNN 对比）
- 教练任务：给 2-3 组双 V 拆分草案（方法 V 写后人能复用什么 + 实证 V 写能发现的新机制/因子/关系），用户选/改

A.5 PXYV 标题
- 范例：Dermatologist-level classification of skin cancer with deep neural networks
  P = Deep CNN + Transfer learning / X = 皮肤病变图像 / Y = 129,450 张临床照片 / V = 双 V
- 教练任务：给 2-3 个候选标题（"[方法] + [对象] + [数据/规模]" 形式），用户选/改

A.6 输出 → markdown 保存到 `选题-A-mining.md`（中间产物 · 断点续跑用）

## STAGE B · 校准（B.1-B.4，之后做共用的 B.5）

B.1 P 校准 · 学科范式
- 工具：Web Search
- 范例（Esteva）：2015-2016 已有 CNN 用于医学影像（如糖尿病视网膜病变），但皮肤癌大规模 CNN 尚无 — P 站得住且有突破空间
- 用户动作：学科范式是否成熟 + 我的位置（突破点在哪）

B.2 数据校准（mode ④ 生死线）
- 工具：数据库官网检索（PhysioNet / TCGA / UK Biobank / ImageNet / ISIC 等）+ Web Search
- 范例：需要 ~130,000 张标注皮肤病变图（覆盖 2032 种皮肤疾病）；来源：Stanford 医院数据库 + ISIC 开源；可得 → 项目可执行
- 用户动作：需要多少数据 / 哪里可得 / 是否实际可获取（数据库名 + 申请流程）

B.3 基线方法校准（方法 V 立不住的前提）
- 工具：Web Search 相关领域 SOTA
- 范例：21 名认证皮肤科医生人工诊断 + 已有 ML 方法（dermatologist-trained classifiers）→ 双 V 实证 V 有"显著超过"的标准
- 用户动作：我的方法 vs 什么基线对比 + 基线指标（AUC / RMSE / Sensitivity-Specificity / 准确率）

B.4 合规校准
- 工具：Web Search 数据使用条款 / 学校 IRB 网站
- 范例：Stanford IRB 通过；患者数据脱敏；ISIC 数据是公开科研用 → 合规无障碍
- 用户动作：IRB / 数据使用许可 / 伦理审批 / 数据脱敏要求

## STAGE C · 输出

阶段 C · mode ④ 标志产出 = 研究目标 / Specific Aims + 方法计划（双 V 实现）
- 范例（Esteva 2017 原文是 Nature Letter，不写 Specific Aims；以下为论文真实陈述）：
  - 论文原文（main text）："In this paper we outline the development of a CNN that matches the performance of dermatologists at three key diagnostic tasks: melanoma classification, melanoma classification using dermoscopy and carcinoma classification."
  - 论文原文（abstract 实证 V）："The CNN achieves performance on par with all tested experts across both tasks, demonstrating an artificial intelligence capable of classifying skin cancer with a level of competence comparable to dermatologists."
  - 数据 + 方法：129,450 训练 + validation images（含 3,374 张 dermoscopy）；1,942 张 biopsy-proven test images；2,032 种皮肤疾病；757 训练类（disease-partitioning algorithm，maxClassSize=1,000）；Inception v3 ImageNet 1.28M 预训练 + transfer learning；21 名 board-certified 皮肤科医生对照；Sensitivity / Specificity / ROC AUC（> 0.91 across tasks）
  - 注：Nature 短报告不用 Specific Aims 体例。Aims 是 NIH grant convention。如果目标是 NIH grant，用 Aims；如果是 Nature/Science 短报告，用 "We demonstrate / We train / We test" 直接陈述
- 用户产出（按目标期刊体例选）：
  - 形态 A（grant / 长论文，用 Specific Aims 体例）：Aim 1 方法："To develop / train / propose ..." + Aim 2 实证："To demonstrate / identify / validate ..." + Aim 3 泛化（可选）："To validate on / extend to ..."
  - 形态 B（Nature / Science 短报告 / 顶会 letter，用直接陈述体例）："Here we demonstrate ..." + "We train ... on [data]" + "We test ... against [baseline]"
  - 共同产出：
    1. 完整方法计划：样本量 + 数据来源 + 纳排标准 + 模型/分析方法 + 基线对照 + 评价指标 + 软件 + IRB
    2. 双 V 实现路径：方法 V 后续可被谁用 + 实证 V 改变什么实践

教学锚句：Esteva 2017 的 V 不是"我发表了一篇论文"，是"我证明了 AI 能达到（on par with）医生水平" — 这种"能力等级跨越"的实证 V 是 mode ④ 顶刊常见叙事。注意：论文说 "on par with / comparable to"（达到），不是 "exceed / outperform"（超过）。

输出 → `选题.md`（唯一正式产出 · 顶部含 workbench 锚块）
