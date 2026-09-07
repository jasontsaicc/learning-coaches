---
name: terraform-coach
description: Use when learning Terraform/IaC, practicing HCL, state safety, modules, plan/apply, or IaC interview drills. Hands-on first-principles coach; ordinary infrastructure implementation does not itself request a course.
---

# Terraform Coach

Resolve relative paths from the real directory containing this `SKILL.md`, after following
symlinks. This rule is shared by Claude Code and Codex.

For planning or skill maintenance, read [governance](../../engine/GOVERNANCE.md)
and the relevant evidence without starting a lesson or writing learning state.
For a learning session, read the [shared engine](../../engine/ENGINE.md) and governance
once per available context, then load hooks using governance's **Context loading contract**.
The Hook Map is an on-demand index. Preserve domain safety and teaching rules before
acting; the progress schema remains engine-owned (`engine/PROGRESS-SCHEMA.md`).

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
