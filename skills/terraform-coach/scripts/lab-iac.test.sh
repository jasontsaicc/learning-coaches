#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
SH=./lab-iac.sh
pass=0; fail=0
check() { if eval "$1"; then pass=$((pass+1)); else echo "FAIL: $2"; fail=$((fail+1)); fi; }

# apply must NOT execute terraform; it only prints a command containing 'terraform apply'
out="$($SH apply ./nonexistent-dir 2>&1 || true)"
check '[[ "$out" == *"terraform apply"* ]]' "apply prints the command"
check '[[ "$out" == *"run this yourself"* ]]' "apply tells user to run it"
check '[[ "$out" != *"Error acquiring the state lock"* ]]' "apply did not actually execute"

# destroy must print a command and a verification reminder
out="$($SH destroy ./nonexistent-dir 2>&1 || true)"
check '[[ "$out" == *"terraform destroy"* ]]' "destroy prints the command"
check '[[ "$out" == *"verify"* ]]' "destroy reminds to verify teardown"

# unknown subcommand exits non-zero
if $SH bogus 2>/dev/null; then echo "FAIL: bogus accepted"; fail=$((fail+1)); else pass=$((pass+1)); fi

echo "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
