#!/usr/bin/env bash
set -uo pipefail
SCRIPT="$(dirname "$0")/lab-cluster.sh"
fail=0
assert_eq() { [ "$1" = "$2" ] || { echo "FAIL: expected '$2' got '$1'"; fail=1; }; }

# 載入函式但不執行 main
LAB_CLUSTER_NO_MAIN=1 source "$SCRIPT"

assert_eq "$(cluster_name p0)" "k8s-coach-p0"
assert_eq "$(cluster_name)" "k8s-coach-default"
# 未知子指令 → 退出碼 2
( LAB_CLUSTER_NO_MAIN= ; bash "$SCRIPT" bogus >/dev/null 2>&1 ); assert_eq "$?" "2"

[ "$fail" = 0 ] && echo "ALL PASS" || exit 1
