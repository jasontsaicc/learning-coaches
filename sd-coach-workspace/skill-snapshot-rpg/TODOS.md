# TODOS

## Framework Extraction (P2, after SD coach improvements complete)

**What:** Extract domain-independent teaching patterns (marked with `<!-- FRAMEWORK: Reusable -->` comments) from SD coach into a reusable `teaching-framework/` directory.

**Why:** User plans to build LeetCode coach and Go language coach. Shared patterns: Feynman Gate, Phase Gates, progress tracking, tiered scoring, session breakpoints, mistake registry.

**When:** After SD coach improvements are stable and tested. Start when building the second skill.

**How:** Find all `<!-- FRAMEWORK: Reusable -->` markers in SKILL.md and references/. Extract those sections into `teaching-framework/` with placeholder slots for domain-specific content.

**Depends on:** All CEO review improvements complete + eval passing.

## LLM-as-Judge Eval Automation (P3, when building second skill)

**What:** Build an automated eval runner that uses Claude API as a judge to score each eval case pass/fail, replacing manual review.

**Why:** Manual review of 18+ eval cases per skill is manageable for one skill. When expanding to LeetCode coach and Go coach (each with their own eval suites), manual review becomes impractical. Automated eval enables regression testing after SKILL.md changes.

**How:** Script that runs each eval prompt through the skill, then sends the response + expected_output to a Claude judge that returns pass/fail + reasoning.

**Depends on:** At least 2 skills sharing the teaching framework. Not needed while only SD coach exists.
