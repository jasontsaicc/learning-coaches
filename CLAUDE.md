# learning-coaches

Claude Code plugin: learning coaches. Details in README.md.
k8s / sd / terraform / ca 共用 `engine/`。leetcode-coach 是 standalone(節奏不同,
一天 1 到 2 題;設計理由見 `docs/superpowers/specs/2026-08-28-leetcode-rebuild-design.md`)。

- Before commit: `./scripts/lint-all.sh` must pass.
- 掛 engine 的四個 coach:progress schema 是 engine-owned (engine/PROGRESS-SCHEMA.md),
  hook 照 engine/PLUGIN-INTERFACE.md。不要在 coach 裡 fork schema。
  leetcode-coach 不適用,它有自己的 schema。
- `workspaces/` is git-tracked learner state. Coaching sessions write it; dev work must not touch it.
- `legacy/`, `workspaces/*/archive/pre-migration/`, and `workspaces/leetcode/archive/pre-rebuild/`
  are frozen history. Read-only.
- New coach: `./scripts/new-coach.sh <name>` (scaffolds with TODO markers, fails lint until filled).
