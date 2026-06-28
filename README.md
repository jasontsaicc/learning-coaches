# learning-coaches

A Claude Code plugin providing a family of first-principles learning coaches built on a shared teaching engine. Each coach uses Feynman and Simon methods (incremental layering, asking you to articulate understanding, teaching by breaking down complex topics into foundational pieces) to guide deep learning in DevOps domains. Initial focus: Terraform/Infrastructure-as-Code, with kubernetes, system design, and leetcode to follow.

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
│   └── references/                          # Engine reference materials
│       ├── feynman-gate.md
│       ├── gap-mode.md
│       ├── scorecard-frame.md
│       ├── spaced-repetition.md
│       ├── teach-to-learn.md
│       └── weekly-review.md
├── scripts/
│   ├── lint-all.sh
│   ├── lint-coach.sh
│   └── lint-engine.sh
└── skills/
    └── terraform-coach/
        ├── SKILL.md
        ├── references/
        │   ├── curriculum.md
        │   ├── lab-manager.md
        │   ├── north-star.md
        │   ├── phase-gates.md
        │   ├── portfolio.md
        │   ├── scorecard-dims.md
        │   └── teaching-elements.md
        └── scripts/
            ├── lab-iac.sh
            └── lab-iac.test.sh
```

## Engine Read Mechanism

A coach reads the shared engine via `${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` (bash
injection), with markdown link `../../engine/ENGINE.md` as a human-readable backup.
`${CLAUDE_SKILL_DIR}` is the skill's own directory and resolves regardless of the session
working directory (per official Claude Code skills docs). `${CLAUDE_PLUGIN_ROOT}` does not
exist for skills. Local testing: `claude --plugin-dir <repo>`, reload with `/reload-plugins`.
