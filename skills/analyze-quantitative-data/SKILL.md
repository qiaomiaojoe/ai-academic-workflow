---
name: analyze-quantitative-data
description: Use when analyzing quantitative social science data following Neuman's Social Research Methods Ch 12 — codebook creation, data cleaning, univariate descriptive statistics, bivariate association, multivariate analysis (elaboration paradigm + multiple regression), and inferential statistics (significance testing, Type I/II errors). Trigger on requests like "analyze this survey data", "run regression on X", "check bivariate relationship between A and B", "what does this codebook need", "interpret these statistics", "我要做定量分析", "帮我跑回归", "分析这份调查数据".
---

# Analyze Quantitative Data · Neuman Ch 12 Workflow

This skill guides users through systematic quantitative data analysis based on
**W. Lawrence Neuman, *Social Research Methods: Qualitative and Quantitative Approaches*, 7e, Chapter 12** (p.393-430).

The chapter's procedure is decomposed into 7 sequential steps, each with a
dedicated prompt template that enforces methodological rigor.

## When to invoke

Invoke this skill when the user:
- Has a survey, experiment, or numerical dataset to analyze
- Asks "how do I analyze X?" with quantitative data
- Wants to run a regression, t-test, ANOVA, chi-square
- Needs to interpret statistical output
- Is preparing a Methods or Results section for a quantitative paper

Do **not** invoke for:
- Pure data engineering / ETL (no analysis intent)
- Machine learning prediction (different methodology)
- Qualitative analysis (use `analyze-qualitative-data` instead)

## The 7-step procedure (Neuman Ch 12)

| # | Step | Prompt file | Neuman pages |
|---|------|-------------|--------------|
| 1 | **Build codebook** | `prompts/01-codebook.md` | 393-394 |
| 2 | **Clean data** (wild code + contingency) | `prompts/02-clean-data.md` | 397 |
| 3 | **Univariate analysis** (frequency, central tendency, variation) | `prompts/03-univariate.md` | 397-403 |
| 4 | **Bivariate analysis** (scattergram, percentaged tables, association measures) | `prompts/04-bivariate.md` | 403-416 |
| 5 | **Multivariate elaboration** (5 patterns) | `prompts/05-multivariate-elaboration.md` | 417-420 |
| 6 | **Multiple regression** | `prompts/06-multivariate-regression.md` | 420-422 |
| 7 | **Inferential statistics** | `prompts/07-inferential.md` | 422-426 |

## How to use

### Sequential mode (full study, beginner)
Walk through 1 → 2 → 3 → 4 → 6 → 7 in order. Step 5 (elaboration) only if user
wants to test for spurious relationships before regression.

### Targeted mode (specific question)
Jump directly to the relevant step. Common patterns:
- "I need to interpret a regression" → step 6 → 7
- "Is my X-Y relationship spurious?" → step 5
- "Just describe my variables" → step 3

### Audit mode (review existing analysis)
Run user's analysis through steps 2 → 3 → 4 to check for missed cleaning, lurking
distributional issues, or wrong-level association measures.

## Cross-cutting principles (apply at every step)

1. **Don't assume — ask back.** If variable types or research question are
   unclear, request clarification before generating code.

2. **Measurement level determines tool.** Wrong level (e.g., Pearson r on ordinal
   data) is the most common silent error. Reject and re-prompt.

3. **Report sample size N at every output.** Listwise deletion shrinks N silently;
   always disclose.

4. **Effect size before p-value.** Statistical significance can be trivial in
   large samples; substantive significance is the user's judgment.

5. **Surface uncertainty.** When AI is unsure (e.g., whether a missing pattern is
   random), say so explicitly and propose ways for user to verify.

## What this skill does NOT do

- **Decide research questions or hypotheses** — that's research design (Neuman Ch 6)
- **Choose methodology** — handled in earlier course content
- **Verify causal identification** — Mill's methods or experimental design needed
- **Replace methodological consultation** — for complex designs (mediation, SEM,
  multilevel models, IV/DID/RDD), recommend the user find a domain expert after
  steps 1-5 to verify key judgments

## Required outputs at each step

Every step's prompt enforces:
- **Sample size N** (with listwise deletion accounting)
- **Variable measurement levels** (validated against statistical choice)
- **Suspect patterns flagged** (collinearity, outliers, severe skew, near-zero
  variance, etc.)
- **Code reproducible by the user** (no placeholders, runnable)
- **Plain-language interpretation** alongside numerical output

## Companion skill

For mixed-methods projects, see `analyze-qualitative-data` (Neuman Ch 14).
