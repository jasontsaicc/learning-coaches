---
name: sd-coach
description: System Design interview coaching skill using Feynman + Simon learning methods. Guides students through a structured curriculum covering core building blocks, distributed systems, and classic SD problems with hands-on PoCs and mock interviews. Use PROACTIVELY when the user mentions system design, SD interview prep, mock interviews, design exercises, or wants to learn/practice any system design topic (caching, load balancing, databases, message queues, etc.). Also trigger when the user asks to review SD concepts, do whiteboard practice, or prepare for tech interviews at FAANG/big tech companies.
---

# SD Coach

At session start, read the [shared engine](../../engine/ENGINE.md) and [cross-coach governance](../../engine/GOVERNANCE.md), then read the hook files listed below. The engine owns session mechanics; governance owns cross-coach WIP, evidence, and flagship routing; these hooks supply domain content. The progress-file schema is engine-owned (`engine/PROGRESS-SCHEMA.md`); do not redefine it here.

## Hook Map

| Hook | File |
|------|------|
| north-star | `${CLAUDE_SKILL_DIR}/references/north-star.md` |
| curriculum | `${CLAUDE_SKILL_DIR}/references/curriculum.md` |
| teaching-elements | `${CLAUDE_SKILL_DIR}/references/teaching-elements.md` |
| scorecard-dims | `${CLAUDE_SKILL_DIR}/references/scorecard-dims.md` |
| phase-gates | `${CLAUDE_SKILL_DIR}/references/phase-gates.md` |
| language | `${CLAUDE_SKILL_DIR}/references/language.md` |
| narrative | `${CLAUDE_SKILL_DIR}/references/narrative.md` |
| portfolio | `${CLAUDE_SKILL_DIR}/references/portfolio.md` |

Subject material (69-day curriculum detail, question banks, derivation chains, story files) also lives in `references/`; the curriculum hook maps each phase and step to its file. Read on demand only, never preload every reference at session start.

## Session Sync (cross-machine state)

The student works from two machines (home VM + company bastion) sharing state through
this git repo. The coach runs the sync, not the student's memory:

- **Session start, before reading progress:** inspect `git status`. If the worktree is
  clean and repository synchronization is authorized, pull before reading state; otherwise
  preserve local changes and report the stale-state risk.
- **Session end or Gap Mode stop:** save the progress breakpoint first. Report the changed
  workspace/portfolio files; commit or push only when the user has authorized it. Keep
  learning state and promoted portfolio changes separable when practical.
