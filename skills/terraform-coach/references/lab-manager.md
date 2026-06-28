# Lab Manager: lab-iac.sh

`lab-iac.sh` is the cost-safety shell script for terraform labs. It wraps four terraform subcommands with a strict guardrail: `validate` and `plan` execute directly; `apply` and `destroy` are command generators only.

## Subcommands

```
lab-iac.sh <validate|plan|apply|destroy> [dir]
```

| Subcommand | Behavior |
|------------|----------|
| `validate` | Runs `terraform -chdir="$dir" validate` directly. Safe: reads config, no cloud calls. |
| `plan`     | Runs `terraform -chdir="$dir" plan` directly. Reads state and provider APIs, but makes no changes. |
| `apply`    | Prints the apply command for the learner to run by hand. Does NOT execute terraform. |
| `destroy`  | Prints the destroy command and a `state list` verification step. Does NOT execute terraform. |

Unknown subcommands exit non-zero (exit 2).

## The cost-safety guardrail

`apply` and `destroy` are command generators, not executors. The learner reads the printed command, decides it is correct, and runs it manually in their own shell. This prevents the coach from ever creating or destroying real cloud resources on the learner's behalf.

Example output for `apply`:

```
SAFETY: apply is not run for you. run this yourself after reading the plan:
  cd "./my-lab" && terraform apply
```

## Lab teardown protocol

Every lab session must end with a destroy step. The sequence:

1. Generate the destroy command with `lab-iac.sh destroy <dir>`.
2. The learner runs the printed `terraform destroy` command manually.
3. The learner runs `terraform state list` in that directory and confirms the output is empty.

This two-step sequence (destroy + state list verification) is the teardown contract. Skipping the verification step leaves the learner with no confirmation that cloud resources are gone.

## Feynman Gate hook

`validate` and `plan` are the objective verification hook for phase gates:

- `validate` confirms the config is syntactically correct and internally consistent.
- `plan` confirms the config produces a plausible execution plan against the target provider state.

Both must pass before a learner advances to the next phase. They serve as the machine-checkable half of the Feynman Gate; the oral explanation check is the other half.
