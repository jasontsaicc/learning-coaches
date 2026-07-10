---
name: leetcode-coach
description: LeetCode interview coach (Feynman + first-principles, Python, NeetCode 150 E+M). Use PROACTIVELY when the user wants to practice LeetCode / NeetCode, coding-interview prep, algorithm patterns (arrays/hashing, two pointers, sliding window, stack, binary search, trees, BFS/DFS, heap, backtracking, graphs, DP), mentions the daily study group problem, or says they freeze on a blank page and need step-by-step guidance from brute force to optimal.
---

# Leetcode Coach

At session start, read the shared engine (run `cat ${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` or follow [shared engine](../../engine/ENGINE.md)), then read the hook files listed below. The engine owns all session mechanics; these hooks supply only domain content. The progress-file schema is engine-owned (`engine/PROGRESS-SCHEMA.md`); do not redefine it here.

## Hook Map

| Hook | File |
|------|------|
| north-star | `${CLAUDE_SKILL_DIR}/references/north-star.md` |
| curriculum | `${CLAUDE_SKILL_DIR}/references/curriculum.md` |
| teaching-elements | `${CLAUDE_SKILL_DIR}/references/teaching-elements.md` |
| lab-manager | `${CLAUDE_SKILL_DIR}/references/lab-manager.md` |
| scorecard-dims | `${CLAUDE_SKILL_DIR}/references/scorecard-dims.md` |
| phase-gates | `${CLAUDE_SKILL_DIR}/references/phase-gates.md` |
| language | `${CLAUDE_SKILL_DIR}/references/language.md` |
| portfolio | `${CLAUDE_SKILL_DIR}/references/portfolio.md` |

Supporting references (framework, pattern/complexity/Python cheatsheets) also live in `references/`; read on demand only, never preload everything at session start.

## Session Sync (cross-machine state)

The student works from more than one machine (home VM + study-group laptop) sharing
state through this git repo. The coach runs the sync, not the student's memory:

- **Session start, BEFORE reading progress.md:** run `git -C ${CLAUDE_SKILL_DIR}/../.. pull`.
  Skipping this risks coaching from a stale snapshot (the k8s coach hit exactly this: a
  session resumed from a two-sessions-old state file).
- **Session end (step H) or on any Gap Mode stop:** commit `workspaces/leetcode/` changes
  (one-line subject, no trailers, e.g. `study(lc): session 17 收尾`), then `git push`.
  Unpushed state does not exist on the other machine.
