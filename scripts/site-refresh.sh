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

# Cloudflare Pages (learn.jasondevops.space, behind Access). No token file = tailnet only.
[[ -r ~/.cloudflare-token ]] || exit 0
CLOUDFLARE_API_TOKEN=$(<~/.cloudflare-token) CLOUDFLARE_ACCOUNT_ID=d8d2fcf49422f37de7b5f82a1436ee47 WRANGLER_SEND_METRICS=false npx -y wrangler@4.40.0 pages deploy site/dist --project-name learning-map --branch master --commit-dirty=true 2>&1 | tail -1
# 302 = Access login in front; 200 would mean the gate is gone
curl -s -o /dev/null -w 'learn.jasondevops.space %{http_code}\n' https://learn.jasondevops.space/data.json
