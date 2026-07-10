# LeetCode Coach

A Claude Code skill that coaches you for coding interviews with one goal: **you can write the code yourself, cold, under interview pressure — including on problems you've never seen.**

Most prep tools teach problems beautifully and leave you able to *recognize* a solution. That's not the same as being able to *produce* one from a blank page. This skill is built around closing that recognition-to-recall gap (手感), not around lecturing.

## How it works — four modes, two axes

You pick **which problem** (next in the curriculum, or a specific one you name) and **how to train** it:

| Mode | For | What it trains |
|------|-----|----------------|
| **Drill** (default) | A pattern you understand but freeze on | Cold blind-skeleton reps; scaffold only when stuck; next-day cold re-do as the real test |
| **Learn** | A genuinely new pattern | Deep teaching: analogy, live diagrams, brute → clearest-optimal |
| **Cold Solve** | An unseen problem | Articulating a discussable approach (brute force + complexity, map to a pattern) *before* coding |
| **Mock** | Interview rehearsal | Think-aloud on an unseen problem, interviewer follow-ups |

Common combo: "I'm presenting Valid Parentheses at study group tomorrow" → that problem + **Learn** (+ Fast mode if you're short on time).

## What makes it different

- **Measures fluency, not coverage.** Progress is "how many patterns can you write cold and 0-bug," not "how many problems you've seen."
- **An articulable approach is itself the goal.** On unseen problems, a clear plan + brute force beats a blank screen. That skill is trained directly.
- **Stuck at zero? Worked example first.** When you can't produce even a first line, the coach shows one narrated think-aloud, then fades the scaffold — it doesn't just re-tell you to "try."
- **The tool stays clean.** Your solutions, notes, and progress live in *your* practice directory, never inside the skill.

## Install

```bash
git clone https://github.com/jasontsaicc/leetcode_coach.git
ln -s "$(pwd)/leetcode_coach" ~/.claude/skills/leetcode-coach
```

Then in Claude Code, start with anything like *"let me drill sliding window, I keep blanking"* or *"test me on a problem I haven't seen."* The skill triggers on coding-interview practice automatically.

## Project structure

```
leetcode-coach/
├── SKILL.md                      # The skill: modes, router, drill loop, fluency bar
├── references/                   # Read on demand, not preloaded
│   ├── curriculum.md             #   NeetCode 150 (E+M) + interview extras
│   ├── pattern-cheatsheet.md     #   the ~8-10 core skeletons Drill is built on
│   ├── problem-solving-framework.md  # the 4-question articulation bridge
│   ├── complexity-cheatsheet.md  #   Big-O reference
│   ├── progress-template.md      #   3-block progress format
│   └── notes-template.md         #   per-problem notes (Learn mode)
├── evals/                        # test cases for skill validation
└── docs/                         # design history
```

Your practice artifacts (`progress.md`, `workspace/`, `notes/`) are written into your own practice directory and are gitignored here.

## License

MIT
