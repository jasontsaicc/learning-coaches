# learning-coaches

Claude Code and Codex learning coaches. Repository structure and setup live in `README.md`.

- Before committing, run `./scripts/lint-all.sh`.
- Coach skills live in `skills/`; Codex discovers the same directories through
  `.agents/skills/`. Resolve skill-relative paths from the real directory containing
  `SKILL.md`, after following symlinks.
- `k8s`, `sd`, `terraform`, and `cloud-architect` share `engine/`. `leetcode-coach` is
  standalone.
- Course sessions may update `workspaces/`. Development work must leave it unchanged.
- Treat `legacy/`, `workspaces/*/archive/pre-migration/`, and
  `workspaces/leetcode/archive/pre-rebuild/` as read-only history.
- Scaffold a coach with `./scripts/new-coach.sh <name>`; all generated TODO markers must
  be resolved before lint passes.
