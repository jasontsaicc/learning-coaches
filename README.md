# learning-coaches

A Claude Code plugin providing a family of first-principles learning coaches built on a shared teaching engine. Each coach uses Feynman and Simon methods (incremental layering, asking you to articulate understanding, teaching by breaking down complex topics into foundational pieces) to guide deep learning in DevOps domains. Live coaches: Terraform/Infrastructure-as-Code, Kubernetes/SRE, System Design interview prep, and LeetCode coding-interview prep.

## Repository Structure

```
learning-coaches/
├── .claude-plugin/
│   └── plugin.json                          # Plugin manifest
├── .gitignore
├── README.md
├── engine/
│   ├── ENGINE.md                            # Shared teaching engine
│   ├── PLUGIN-INTERFACE.md                  # Coach hook contract
│   ├── PROGRESS-SCHEMA.md                   # Engine-owned progress-file schema (shared by all coaches)
│   └── references/                          # Engine reference materials
│       ├── anti-sycophancy.md
│       ├── feynman-gate.md
│       ├── gap-mode.md
│       ├── scorecard-frame.md
│       ├── spaced-repetition.md
│       ├── teach-to-learn.md
│       └── weekly-review.md
├── scripts/
│   ├── lint-all.sh
│   ├── lint-coach.sh
│   ├── lint-engine.sh
│   └── new-coach.sh                         # Scaffold a new coach from templates/
├── templates/
│   └── coach/                               # Fill-in-the-blank hook templates (TODO markers)
│       ├── SKILL.md.tmpl
│       └── references/*.md.tmpl
├── skills/
│   ├── terraform-coach/
│   │   ├── SKILL.md
│   │   ├── references/                      # 7 hook files
│   │   └── scripts/                         # lab-iac.sh + test
│   ├── k8s-coach/
│   │   ├── SKILL.md
│   │   ├── references/                      # 8 hook files + subject material
│   │   │                                    #   (phase-0..6, foundations, chaos-drills,
│   │   │                                    #    real-world-scenarios, interview-bank, term-glossary)
│   │   ├── scripts/                         # lab-cluster.sh (kind lifecycle) + test
│   │   └── evals/                           # behavioral evals + fixtures
│   ├── sd-coach/
│   │   ├── SKILL.md
│   │   ├── references/                      # 8 hook files (incl. language + narrative) + subject
│   │   │                                    #   material (curriculum-detail, first-principles-chains,
│   │   │                                    #    follow-up-bank, answer-comparisons, story, rpg-rules)
│   │   └── evals/                           # behavioral evals + fixtures
│   └── leetcode-coach/
│       ├── SKILL.md
│       ├── references/                      # 8 hook files (incl. language) + cheatsheets
│       │                                    #   (problem-solving-framework, pattern,
│       │                                    #    complexity, python-dsa)
│       ├── scripts/                         # lab-lc.sh (pytest + large-N tripwire) + test
│       └── evals/                           # behavioral evals + fixtures
├── workspaces/                              # per-coach learner state — git-TRACKED
│   ├── k8s/                                 # progress.md (engine schema), term-registry,
│   │                                        #   story-bank, session-log, environment,
│   │                                        #   curriculum-plan, clusters/, notes/
│   ├── sd/                                  # progress.md (engine schema), one-liner-library,
│   │                                        #   rpg-state, session-log, coaching-brief,
│   │                                        #   curriculum-plan, pattern-map
│   └── leetcode/                            # progress.md (engine schema), one-liner-library,
│                                            #   skeleton-registry, patterns.md,
│                                            #   <phase>/<slug>/ problem folders
└── portfolio/                               # recruiter-facing artifacts
    ├── k8s/                                 # notes/ + manifests/ (+ observability/,
    │                                        #   gitops/, terraform-eks/ as phases grow)
    └── sd/                                  # notes/ (day01+ topic notes + mindmaps)
                                             #   + projects/ (Go PoCs, one dir per topic)
```

## Tracked Workspaces

`workspaces/` holds per-student learning state (progress file, registries, session log) and
is deliberately git-tracked: the student syncs it across machines by committing after each
session and pulling before the next. This differs from `skills/*/workspace/`, which stays
untracked scratch space. `portfolio/` is the curated, shareable output area; only artifacts
that clear the coach's quality bar land there. The k8s learner state was migrated from the
standalone `k8s-mastery-lab-skill` repo (history merged via git subtree; pre-migration
originals kept verbatim in `workspaces/k8s/archive/pre-migration/`). The sd learner state,
notes, and Go PoCs were migrated the same way from the standalone `system-design-coach` +
`system-design-notes` repos (originals in `workspaces/sd/archive/pre-migration/`). The
leetcode learner state (16 sessions of progress, mistake registry, one-liner library,
solved problems) was migrated from the standalone `leetcode-notes` repo, and the coach's
teaching philosophy from the standalone `leetcode_coach` skill repo (originals in
`workspaces/leetcode/archive/pre-migration/`; full histories under `legacy/leetcode/`).

## Engine Read Mechanism

A coach reads the shared engine via `${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` (bash
injection), with markdown link `../../engine/ENGINE.md` as a human-readable backup.
`${CLAUDE_SKILL_DIR}` is the skill's own directory and resolves regardless of the session
working directory (per official Claude Code skills docs). `${CLAUDE_PLUGIN_ROOT}` does not
exist for skills. Local testing: `claude --plugin-dir <repo>`, reload with `/reload-plugins`.
