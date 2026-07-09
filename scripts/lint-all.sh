#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== plugin manifest =="
python3 -c "import json,sys; json.load(open('.claude-plugin/plugin.json')); print('plugin.json OK')"
echo "== engine =="
./scripts/lint-engine.sh && echo "engine OK"
echo "== coaches =="
for d in skills/*/; do
  name="$(basename "$d")"
  [ "$name" = "_probe" ] && continue
  ./scripts/lint-coach.sh "$name" && echo "$name OK"
done
# NOTE: set -e does not fire on the left side of an && list, so lab tests use
# explicit if/else — otherwise a failing (or non-executable) test is silently swallowed.
echo "== terraform lab =="
if ./skills/terraform-coach/scripts/lab-iac.test.sh >/dev/null; then echo "lab-iac OK"; else echo "lab-iac FAIL"; exit 1; fi
echo "== k8s lab =="
if ./skills/k8s-coach/scripts/lab-cluster.test.sh >/dev/null; then echo "lab-cluster OK"; else echo "lab-cluster FAIL"; exit 1; fi
echo "== templates =="
tmpl_fail=0
for t in templates/coach/SKILL.md.tmpl \
         templates/coach/references/{north-star,curriculum,teaching-elements,scorecard-dims,phase-gates,portfolio,lab-manager,language,narrative}.md.tmpl; do
  [ -s "$t" ] || { echo "MISSING template: $t"; tmpl_fail=1; }
  grep -qF "TODO:" "$t" || { echo "template lost its TODO sentinels: $t"; tmpl_fail=1; }
done
[ "$tmpl_fail" -eq 0 ] && echo "templates OK" || exit 1
echo "ALL PASS"
