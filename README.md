**[English](README.md)** | **[繁體中文](README.zh-TW.md)**

```
  ____            _                   ____            _                ____                 _
 / ___| _   _ ___| |_ ___ _ __ ___  |  _ \  ___  ___(_) __ _ _ __   / ___|___   __ _  ___| |__
 \___ \| | | / __| __/ _ \ '_ ` _ \ | | | |/ _ \/ __| |/ _` | '_ \ | |   / _ \ / _` |/ __| '_ \
  ___) | |_| \__ \ ||  __/ | | | | || |_| |  __/\__ \ | (_| | | | || |__| (_) | (_| | (__| | | |
 |____/ \__, |___/\__\___|_| |_| |_||____/ \___||___/_|\__, |_| |_| \____\___/ \__,_|\___|_| |_|
        |___/                                           |___/

              an AI-powered system design interview coach skill
```

> *Not flashcards. Not video lectures.*
> *Your AI becomes a Socratic mentor who derives every technique from physics — then makes you teach it back.*

An open-source skill for Claude Code (and 40+ AI editors) that turns your AI into a structured System Design interview coach. 63-day curriculum. First-principles derivation. RPG narrative. You don't memorize "use caching for reads" — you derive it from DRAM ~100ns vs SSD ~100μs vs Network ~1ms.

---

## How It Works

```
  You                     AI (小球)                  Your Terminal
  ---                     --------                   -------------

  "let's learn"  ----->   reads progress.md  -----> checks where
                          becomes 小球 (★‿★)         you left off
                          your mentor
                                |
                                v
                          "DRAM is 100ns.
                           SSD is 100μs.
                           That's 1000x slower.
                           What should we do?"
                                |
                                v
                          derive --> build --> teach --> gate --> next
```

1. Install the skill (see below)
2. Open Claude Code and say **"let's learn system design"**
3. Learn by deriving, not memorizing

---

## The Cast

Characters at **ScaleUp**, a fast-growing startup where everything breaks at scale:

| Character | Role | Catchphrase |
|-----------|------|-------------|
| **(★‿★) 小球** | Senior Architect | "Why does this work?" — your Socratic mentor, never gives answers directly |
| **(◎_◎;) Max** | CTO | "Just ship it" — makes bad architecture calls you learn to fix |
| **(╯°□°)╯ Karen** | PM | "Demo is Friday" — brings real business pressure and requirements |
| **(・_・?) Yuki** | Junior Dev (Phase 2+) | "Can you explain?" — you teach her to prove you truly understand |

---

## The Journey (63 Days)

| Phase | Days | At ScaleUp... | You'll Learn |
|-------|------|---------------|-------------|
| 0 | 1-3 | First week onboarding | Interview rubric, estimation, 4-step SD framework |
| 1 | 4-16 | Traffic spikes, DB debates | LB, caching, databases, queues, API, auth, consistent hashing |
| 2 | 17-26 | International expansion | CAP, consistency, replication, rate limiting, observability |
| 3 | 27-53 | Design review gauntlet | URL shortener, chat, news feed, payment + 8 more problems |
| 4 | 54-63 | Final boss interviews | Trade-off drills, brownfield/legacy migration, mocks, weak spot reinforcement |

Title progression: 🌱 Junior Engineer → ⚙️ Systems Engineer → 🌐 Distributed Engineer → 🏗️ Staff Architect → 👑 Principal Architect

---

## Derivation Chains (What Makes This Different)

Instead of pattern-matching ("see X scenario → use Y technique"), you derive from physics:

```
  Physical constraint              What you derive
  --------------------             ----------------

  DRAM ~100ns, SSD ~100μs    -->   Why caching exists, where to place it
  Single CPU has core limit   -->   Why load balancers exist
  Hardware fails 2-10%/year   -->   Why replication is non-negotiable
  Light speed = 150ms RTT     -->   Why CAP is a partition trade-off
  Sync call = fate coupling   -->   Why message queues decouple
  HTTP is plaintext            -->   Why every security layer exists
```

13 derivation chains cover all Phase 1-2 building blocks. Each chain defines:
- **Physical constraints** — concrete numbers (the anchors)
- **Derivation direction** — logical flow, not a script (the compass)
- **Micro-exercise** — ASCII diagram, pseudocode, or mental model (Build)
- **Transfer question** — explain to Yuki (Teach)

The AI uses these as a compass to guide you naturally — not as a script to read verbatim.

### Adaptive Mode

| Student Level | Derivation Mode | How It Works |
|---------------|----------------|-------------|
| Beginner / Medium Warm-Up | **Guided** | 小球 walks through constraints → derivation → conclusion |
| Strong Warm-Up / Phase 2+ | **Exploration** | 小球 shows only the numbers, you derive, then compare |

---

## Teaching Methods

Four methods, layered:

| Method | What It Does | In Practice |
|--------|-------------|-------------|
| **First Principles** | Derive from physics, not memorize | Step 0: "DRAM is 1000x faster than SSD — now what?" |
| **Feynman** | Explain in your own words to prove understanding | "Can you explain caching to Yuki?" not "Do you understand?" |
| **Simon (Chunking)** | Break topics into 5-10 chunks, master each | Can't move to chunk 3 until chunk 2 passes the gate |
| **Dan Koe (Learn→Build→Teach)** | Three-phase cycle per concept | Derive it → build ASCII diagram → teach it to Yuki |

---

## Session Flow

Each session follows 8 steps (~65-70 min). Pause anytime, resume next session.

```
A. Review          -- recall last session + check parked curiosity branches
B. Introduction    -- story hook + real-life analogy
C. Core Teaching   -- Step 0: Derivation → Step 1: Chunk Map → Step 2: Teach → Step 3: Feynman Gate
D. Hands-On        -- PoC in Go (or ASCII design exercise)
E. Simon Drill     -- close notes, recall from memory
F. Interview Drill -- mini mock with 4-step framework + tiered scorecard
G. Notes           -- structured notes + one-liner challenge + cross-verification
H. Progress        -- update mastery, achievements, streak, story summary
```

---

## Install

### Quick Install (recommended)

```bash
npx skills add jasontsaicc/system-design-coach
```

Works with Claude Code, Cursor, Copilot, and [40+ other agents](https://github.com/vercel-labs/skills).

### Manual Install

```bash
# Personal skill (all projects)
git clone https://github.com/jasontsaicc/system-design-coach.git
cp -r system-design-coach ~/.claude/skills/sd-coach

# Project skill (one project)
mkdir -p .claude/skills
git clone https://github.com/jasontsaicc/system-design-coach.git .claude/skills/sd-coach

# Temporary use (no install)
git clone https://github.com/jasontsaicc/system-design-coach.git ~/sd-coach
claude --add-dir ~/sd-coach
```

### Verify

```
What skills are available?
```

You should see `sd-coach` in the list. Invoke directly with `/sd-coach`.

---

## Language Support

- **English** (default) — all teaching in English
- **Bilingual** — English for technical content, your native language for plain explanations
- **English Polish** — after each response, shows an interview-ready version of what you said

---

## Project Structure

```
system-design-coach/
├── SKILL.md                       # Core skill — methods, gates, flow, RPG layer
├── references/
│   ├── first-principles-chains.md # 13 derivation chains + dependency graph
│   ├── curriculum.md              # 63-day curriculum + prerequisites + story triggers
│   ├── story.md                   # Character personality guides + story arcs
│   ├── achievements.md            # 25 achievements + unlock conditions
│   ├── progress-template.md       # Progress tracking + warm-up + curiosity branches
│   ├── notes-template.md          # Session notes format
│   ├── 8-block-skeleton.md        # Whiteboard diagram template
│   └── estimation-cheatsheet.md   # Back-of-envelope numbers
└── evals/
    └── evals.json                 # 36 test cases for skill validation
```

---

## License

MIT
