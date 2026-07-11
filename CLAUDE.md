# learning-coaches

Claude Code plugin: learning coaches sharing one teaching engine. Details in README.md.

- Before commit: `./scripts/lint-all.sh` must pass.
- Progress schema is engine-owned (engine/PROGRESS-SCHEMA.md); coach hooks follow engine/PLUGIN-INTERFACE.md. Never fork the schema inside a coach.
- `workspaces/` is git-tracked learner state. Coaching sessions write it; dev work must not touch it.
- `legacy/` and `workspaces/*/archive/pre-migration/` are frozen history. Read-only.
- New coach: `./scripts/new-coach.sh <name>` (scaffolds with TODO markers, fails lint until filled).
