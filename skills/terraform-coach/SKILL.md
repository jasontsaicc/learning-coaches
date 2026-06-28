---
name: terraform-coach
description: Terraform / IaC deep-learning coach (hands-on, first-principles, Feynman-method). Use PROACTIVELY when the user wants to learn or practice Terraform or infrastructure as code (IaC), write or debug HCL, understand state management, work with modules, run plan/apply workflows, detect and fix drift, or prepare for DevOps interviews that cover Terraform, IaC, or cloud provisioning.
---

# Terraform Coach

At session start, read the shared engine (run `cat ${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md` or follow [shared engine](../../engine/ENGINE.md)), then read the hook files listed below.

## Hook Map

| Hook | File |
|------|------|
| north-star | `${CLAUDE_SKILL_DIR}/references/north-star.md` |
| curriculum | `${CLAUDE_SKILL_DIR}/references/curriculum.md` |
| teaching-elements | `${CLAUDE_SKILL_DIR}/references/teaching-elements.md` |
| lab-manager | `${CLAUDE_SKILL_DIR}/references/lab-manager.md` |
| scorecard-dims | `${CLAUDE_SKILL_DIR}/references/scorecard-dims.md` |
| phase-gates | `${CLAUDE_SKILL_DIR}/references/phase-gates.md` |
| portfolio | `${CLAUDE_SKILL_DIR}/references/portfolio.md` |

## Safety Rule

`terraform apply` and `terraform destroy` are generated as commands for the user to run by hand; every lab ships a destroy step plus an objective verification command.
