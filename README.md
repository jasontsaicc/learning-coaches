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
    │   └── SKILL.md         # Temporary probe to validate engine reads (human-triggered)
    ├── devops-iac-engineer/
    └── [other coaches to follow]
```

## Engine Read Mechanism

Engine read mechanism: PENDING human probe (Task 1 Step 5).
