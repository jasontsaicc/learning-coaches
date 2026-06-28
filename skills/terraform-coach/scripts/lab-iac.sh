#!/usr/bin/env bash
set -euo pipefail
cmd="${1:?usage: lab-iac.sh <validate|plan|apply|destroy> [dir]}"
dir="${2:-.}"
case "$cmd" in
  validate) terraform -chdir="$dir" validate ;;
  plan)     terraform -chdir="$dir" plan ;;
  apply)
    echo "SAFETY: apply is not run for you. run this yourself after reading the plan:"
    echo "  cd \"$dir\" && terraform apply"
    ;;
  destroy)
    echo "SAFETY: destroy is not run for you. run this yourself, then verify nothing is left:"
    echo "  cd \"$dir\" && terraform destroy"
    echo "  then verify: cd \"$dir\" && terraform state list   (expect empty)"
    ;;
  *) echo "unknown subcommand: $cmd" >&2; exit 2 ;;
esac
