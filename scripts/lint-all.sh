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
echo "== terraform lab =="
./skills/terraform-coach/scripts/lab-iac.test.sh >/dev/null && echo "lab-iac OK"
echo "ALL PASS"
