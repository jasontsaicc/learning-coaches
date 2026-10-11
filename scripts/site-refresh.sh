#!/usr/bin/env bash
# Rebuild the learning map (site/dist) and restart its tailnet server, then check it answers.
# Restart is not strictly needed after a rebuild (http.server reads files per request);
# it's here so one command also recovers a dead server.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 site/build.py | tail -1
systemctl --user restart learning-map.service
sleep 1
systemctl --user is-active learning-map.service
curl -sf -o /dev/null -w 'data.json %{http_code} %{size_download}B\n' "http://100.86.161.122:8123/data.json?v=$(date +%s)"
echo "open http://100.86.161.122:8123/?v=$(date +%s)"
