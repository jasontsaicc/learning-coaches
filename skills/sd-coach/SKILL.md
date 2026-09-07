---
name: sd-coach
description: Use when learning system design or practicing architecture interviews, capacity estimates, trade-offs, and design critiques. 繁體中文 Feynman 教練。Generic interview planning does not start a lesson.
---

# SD Coach

Resolve relative paths from the real directory containing this `SKILL.md`, after following
symlinks. This rule is shared by Claude Code and Codex.

For planning or skill maintenance, read [governance](../../engine/GOVERNANCE.md)
and the relevant evidence without starting a lesson or writing learning state.
For a learning session, read the [shared engine](../../engine/ENGINE.md) and governance
once per available context, then load hooks using governance's **Context loading contract**.
The Hook Map is an on-demand index. Preserve domain safety and teaching rules before
acting; the progress schema remains engine-owned (`engine/PROGRESS-SCHEMA.md`).

## Hook Map

| Hook | File |
|------|------|
| north-star | [references/north-star.md](references/north-star.md) |
| curriculum | [references/curriculum.md](references/curriculum.md) |
| teaching-elements | [references/teaching-elements.md](references/teaching-elements.md) |
| scorecard-dims | [references/scorecard-dims.md](references/scorecard-dims.md) |
| phase-gates | [references/phase-gates.md](references/phase-gates.md) |
| language | [references/language.md](references/language.md) |
| narrative | [references/narrative.md](references/narrative.md) |
| portfolio | [references/portfolio.md](references/portfolio.md) |

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
