# learning-coaches

A Claude Code plugin providing a family of first-principles learning coaches built on a shared teaching engine. Each coach uses Feynman and Simon methods (incremental layering, asking you to articulate understanding, teaching by breaking down complex topics into foundational pieces) to guide deep learning in DevOps domains. Initial focus: Terraform/Infrastructure-as-Code, with kubernetes, system design, and leetcode to follow.

## Repository Structure

```
learning-coaches/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── .gitignore
├── README.md
├── engine/
│   ├── ENGINE.md            # Shared teaching engine (stub, read by each coach)
│   └── references/          # Engine reference materials
└── skills/
    ├── _probe/
    │   └── SKILL.md         # Temporary probe to validate engine reads (removed at Task 8)
    └── terraform-coach/     # first coach (to follow)
```

## Engine Read Mechanism

A coach reads the shared engine via `${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` (bash
injection), with markdown link `../../engine/ENGINE.md` as a human-readable backup.
`${CLAUDE_SKILL_DIR}` is the skill's own directory and resolves regardless of the session
working directory (per official Claude Code skills docs). `${CLAUDE_PLUGIN_ROOT}` does not
exist for skills. Local testing: `claude --plugin-dir <repo>`, reload with `/reload-plugins`.
