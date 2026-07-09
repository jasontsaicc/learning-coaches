#!/usr/bin/env bash
# k8s-coach lab 叢集管理:統一管 kind 叢集生命週期,降低學員操作摩擦。
# Only apply strict mode when run directly, not when sourced by tests.
[[ "${BASH_SOURCE[0]}" == "$0" ]] && set -euo pipefail

PREFIX="k8s-coach"
CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../k8s-coach-workspace/clusters" && pwd)"

cluster_name() { echo "${PREFIX}-${1:-default}"; }

usage() {
  cat <<'EOF'
Usage: lab-cluster.sh <up|down|status|reset> [phase]
  up [phase]     依 clusters/kind-<phase>.yaml 開叢集(預設 default)
  down [phase]   刪除該叢集
  status         列出所有 k8s-coach 叢集
  reset [phase]  down 後再 up(乾淨重來,給故障注入 drill 用)
EOF
}

cmd_up() {
  local name cfg; name="$(cluster_name "${1:-default}")"
  cfg="${CONFIG_DIR}/kind-${1:-default}.yaml"
  if [ -f "$cfg" ]; then kind create cluster --name "$name" --config "$cfg";
  else kind create cluster --name "$name"; fi
  kubectl --context "kind-${name}" get nodes
}
cmd_down()   { kind delete cluster --name "$(cluster_name "${1:-default}")"; }
cmd_status() { kind get clusters | grep "^${PREFIX}-" || echo "(無 k8s-coach 叢集)"; }
cmd_reset()  { cmd_down "${1:-default}" || true; cmd_up "${1:-default}"; }

main() {
  case "${1:-}" in
    up) shift; cmd_up "$@";;
    down) shift; cmd_down "$@";;
    status) cmd_status;;
    reset) shift; cmd_reset "$@";;
    *) usage; exit 2;;
  esac
}

# 允許測試 source 而不執行 main
[ -n "${LAB_CLUSTER_NO_MAIN:-}" ] || main "$@"
