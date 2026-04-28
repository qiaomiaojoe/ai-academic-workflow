---
name: analyze-qualitative-data
description: Use when analyzing qualitative social science data following Neuman's Social Research Methods Ch 14 — three-stage coding (open/axial/selective), analytic memo writing, outcropping detection, and seven analytic strategies (ideal types, successive approximation, illustrative method, domain analysis, Mill's analytic comparison, narrative analysis). Trigger on requests like "code these interviews", "analyze field notes", "thematic analysis", "narrative analysis", "compare these cases", "我要做定性分析", "帮我编码这些访谈", "做主题分析".
---

# Analyze Qualitative Data · Neuman Ch 14 Workflow

This skill guides users through systematic qualitative data analysis based on
**W. Lawrence Neuman, *Social Research Methods: Qualitative and Quantitative Approaches*, 7e, Chapter 14** (p.477-512).

The chapter is decomposed into 11 prompts spanning three sub-domains:
coding, memo writing, and analytic strategies.

## When to invoke

Invoke this skill when the user:
- Has interview transcripts, field notes, historical documents, or text data
- Asks "how do I code these?" or "how do I find themes?"
- Wants thematic / narrative / domain / comparative analysis
- Is preparing Methods or Findings for a qualitative paper

Do **not** invoke for:
- Quantitative data (use `analyze-quantitative-data` instead)
- Pure transcription / formatting tasks (no analytic intent)
- Generating fictional content / interviews (this skill works on real data only)

## The 11 prompts (Neuman Ch 14)

### Block A · Coding (the spine — Strauss 1987 three stages)

| # | Step | Prompt file | Neuman pages |
|---|------|-------------|--------------|
| 1 | **Open coding** (1st pass — initial themes emerge) | `prompts/01-open-coding.md` | 481-482 |
| 2 | **Axial coding** (2nd pass — connect codes, find core categories) | `prompts/02-axial-coding.md` | 482-484 |
| 3 | **Selective coding** (final pass — scan all data for theme support) | `prompts/03-selective-coding.md` | 484 |

### Block B · Continuous theory-building (parallel to coding)

| # | Step | Prompt file | Neuman pages |
|---|------|-------------|--------------|
| 4 | **Analytic memo writing** | `prompts/04-analytic-memo.md` | 485-486 |
| 5 | **Outcropping detection** (surface → underlying structure) | `prompts/05-outcropping.md` | 486-487 |

### Block C · Seven analytic strategies (pick by data type and RQ)

| # | Strategy | When to use | Prompt file |
|---|----------|-------------|-------------|
| 6 | **Ideal types** (Weber) | Compare reality against pure model | `prompts/06-ideal-types.md` |
| 7 | **Successive approximation** | Iteratively refine concepts and data | `prompts/07-successive-approximation.md` |
| 8 | **Illustrative method** | Fill empty boxes of existing theory | `prompts/08-illustrative-method.md` |
| 9 | **Domain analysis** (Spradley) | Find culture's own classification system | `prompts/09-domain-analysis.md` |
| 10 | **Analytic comparison** (Mill's methods) | Multi-case causal factor identification | `prompts/10-analytic-comparison-mill.md` |
| 11 | **Narrative analysis** | Process / temporal / sequence data | `prompts/11-narrative-analysis.md` |

## How to use

### Sequential mode (typical study)
Run **1 → 2 → 3** for coding (most studies need all three).
Run **4** continuously while coding (memos generate theory).
Pick **one or two** from Block C based on your RQ:
- Compare cultures / contexts → 6 (ideal types)
- Concepts still evolving → 7 (successive approximation)
- Theory-driven test → 8 (illustrative method)
- Folk classification → 9 (domain analysis)
- Multi-case causal → 10 (Mill's methods)
- Process / history → 11 (narrative analysis)

### Quick mode (small-scale study)
For a thesis chapter or small qualitative study, **1 → 2 → 4 → 3** is often enough.

### Comparative mode (multi-case)
For 3+ cases: **1 → 2 → 10 → 3** (or **11** if temporal).

## Cross-cutting principles (apply at every step)

1. **Codes must be grounded in data.** Every code/theme must have a textual
   anchor. AI should never invent quotes or codes not derivable from input.

2. **In-vivo terms preserve actor's voice.** When using folk/mixed domains or
   open coding, retain original wording — don't paraphrase prematurely.

3. **Theme naming demands specificity.** Reject vague themes like "AI's impact".
   Push toward "intergenerational scissors of opportunity" or similar.

4. **Saturation is judged, not assumed.** Each step's prompt asks the user to
   evaluate whether more data is needed.

5. **Iteration is normal.** Successive approximation logic applies across all
   stages — moving back to earlier coding when later analysis reveals gaps.

6. **AI inter-coder reliability ≠ human inter-coder reliability.** Run prompts
   in fresh sessions to check stability, but real reliability requires a second
   human coder.

## What this skill does NOT do

- **Decide what's interesting** — researcher's theoretical commitment leads
- **Validate the research question** — that's research design (earlier in course)
- **Replace IRB ethics review** — for human subjects data, separate review needed
- **Substitute for methodological mentorship** — the more interpretive the
  strategy (especially narrative, ideal types), the more value a domain
  consultant adds

## Required outputs at each step

Every prompt enforces:
- **Textual evidence** for every code, theme, or analytic claim
- **Saturation status** at coding stage transitions
- **Alternative explanations** flagged (avoid single-frame tunnel vision)
- **Negative cases / counter-evidence** highlighted explicitly
- **Researcher voice separated from actor voice** in folk/mixed domains

## Companion skill

For mixed-methods projects, see `analyze-quantitative-data` (Neuman Ch 12).
