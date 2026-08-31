---
name: terraform-coach
description: Terraform / IaC deep-learning coach (hands-on, first-principles, Feynman-method). Use PROACTIVELY when the user wants to learn or practice Terraform or infrastructure as code (IaC), write or debug HCL, understand state management, work with modules, run plan/apply workflows, detect and fix drift, or prepare for DevOps interviews that cover Terraform, IaC, or cloud provisioning.
---

# Terraform Coach

Resolve relative paths from the real directory containing this `SKILL.md`, after following
symlinks. This rule is shared by Claude Code and Codex.

At session start, read the [shared engine](../../engine/ENGINE.md) and [cross-coach governance](../../engine/GOVERNANCE.md), then read the hook files listed below. Governance routes Terraform evidence into the shared `platform-eks` flagship instead of a parallel portfolio.

## Hook Map

| Hook | File |
|------|------|
| north-star | [references/north-star.md](references/north-star.md) |
| curriculum | [references/curriculum.md](references/curriculum.md) |
| teaching-elements | [references/teaching-elements.md](references/teaching-elements.md) |
| lab-manager | [references/lab-manager.md](references/lab-manager.md) |
| scorecard-dims | [references/scorecard-dims.md](references/scorecard-dims.md) |
| phase-gates | [references/phase-gates.md](references/phase-gates.md) |
| portfolio | [references/portfolio.md](references/portfolio.md) |

## Safety Rule

`terraform apply` and `terraform destroy` are generated as commands for the user to run by hand; every lab ships a destroy step plus an objective verification command.
