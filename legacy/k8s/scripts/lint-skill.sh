#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$ROOT/SKILL.md"
err=0
grep -q '^name: k8s-coach' "$SKILL" || { echo "FAIL: frontmatter name"; err=1; }
grep -q '^description:' "$SKILL" || { echo "FAIL: frontmatter description"; err=1; }
for s in "North Star" "Feynman Gate" "Phase Gates" "Teaching Flow" "Chaos Lab" "Curriculum Map"; do
  grep -q "$s" "$SKILL" || { echo "FAIL: missing section $s"; err=1; }
done
# referenced files 存在
grep -oE 'references/[a-z0-9-]+\.md' "$SKILL" | sort -u | while read -r f; do
  [ -f "$ROOT/$f" ] || echo "WARN: referenced $f not found (可能是後續 phase)"
done
[ "$err" = 0 ] && echo "LINT PASS" || exit 1
