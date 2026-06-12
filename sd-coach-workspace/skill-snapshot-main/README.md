# System Design Coach

A Claude Code skill that transforms Claude into a structured System Design interview coach, using **Feynman Method** (deep understanding) + **Simon Method** (mastery through chunking).

## What It Does

- **61-day structured curriculum** covering core building blocks, distributed systems, and classic SD problems
- **Interactive teaching** — never lectures; asks you to explain concepts in your own words
- **Daily mock interviews** — practice the 4-step SD framework with AI feedback
- **Hands-on PoCs** — build proof-of-concept projects, not just memorize
- **Progress tracking** — weekly reviews with blind recall and gap analysis

## Teaching Flow (Every Session)

Each session follows an 8-step flow (A→H) taking ~65-70 minutes of learning content. Sessions can be paused and resumed across conversations via progress tracking.

See `SKILL.md` for the complete teaching flow.

## Curriculum Overview

| Phase | Days | Focus |
|-------|------|-------|
| Phase 0 | 1-3 | Thinking Framework — interview rubric, estimation, 4-step method |
| Phase 1 | 4-16 | Core Building Blocks — LB, caching, databases, queues, API, auth |
| Phase 2 | 17-26 | Distributed Systems — CAP, consistency, replication, rate limiting |
| Phase 3 | 27-53 | Classic SD Problems — URL shortener, chat, news feed, payment, etc. |
| Phase 4 | 54-61 | Mock Interviews — timed mocks, trade-off drills, weak spot reinforcement |

## Install

### Quick Install (recommended)

```bash
npx skills add jasontsaicc/system-design-coach
```

Works with Claude Code, Cursor, Copilot, and [40+ other agents](https://github.com/vercel-labs/skills). No extra setup needed.

### Manual Install

**Personal skill** (available in all your projects):

```bash
git clone https://github.com/jasontsaicc/system-design-coach.git
cp -r system-design-coach ~/.claude/skills/sd-coach
```

**Project skill** (one project only):

```bash
mkdir -p .claude/skills
git clone https://github.com/jasontsaicc/system-design-coach.git .claude/skills/sd-coach
```

**Temporary use** (no install):

```bash
git clone https://github.com/jasontsaicc/system-design-coach.git ~/sd-coach
claude --add-dir ~/sd-coach
```

### Verify

In Claude Code, type:
```
What skills are available?
```
You should see `sd-coach` in the list. You can also invoke it directly with `/sd-coach`.

## Key Features

### Feynman Method
Never asks "Do you understand?" — instead asks "Can you explain X in your own words?" If wrong, guides you to find the error rather than correcting directly.

### Simon Method (Chunking)
Every topic decomposed into 5-10 core chunks. Each chunk must pass the "explain in own words" test before moving on. No skipping — drill until breakthrough.

### 4-Step Interview Framework
Every design answer follows: Clarify Requirements → High-Level Design → Deep Dive → Scale & Trade-offs. Practiced daily to build muscle memory.

### Observability Mindset
Every building block includes SLIs, SLO targets, alerts, and dashboard definitions — training you to naturally weave monitoring into SD answers.

## Language Support

- **Default**: English
- **Bilingual mode**: English + student's native language for Feynman-style plain explanations
- Includes **English Polish** feature for non-native speakers practicing interview articulation

## Project Structure

```
system-design-coach/
├── SKILL.md                  # Core skill — teaching methods, gates, session flow
├── references/
│   ├── curriculum.md          # Full 61-day curriculum with prerequisites
│   ├── progress-template.md   # Student progress tracking format
│   ├── notes-template.md      # Standardized notes format + interview template
│   ├── 8-block-skeleton.md    # Whiteboard diagram template
│   └── estimation-cheatsheet.md # Back-of-envelope numbers
└── evals/
    └── evals.json             # 18 test cases for skill validation
```

## License

MIT
