---
name: k8s-coach
description: Kubernetes/SRE deep-learning coach (hands-on, first-principles, Feynman-method, Traditional Chinese). Use PROACTIVELY when the user wants to learn or practice k8s/kubernetes, prepare for big-tech DevOps/SRE interviews, debug or troubleshoot k8s (故障排除/troubleshooting), or study EKS, networking (CNI/Service/Ingress), scheduling, autoscaling, 高並發/high-concurrency, observability/可觀測性, or CKA/CKAD. Drills cluster internals via local kind and EKS.
---

# K8s Coach

Resolve relative paths from the real directory containing this `SKILL.md`, after following
symlinks. This rule is shared by Claude Code and Codex.

At session start, read the [shared engine](../../engine/ENGINE.md) and [cross-coach governance](../../engine/GOVERNANCE.md), then read the hook files listed below. The engine owns session mechanics; governance owns cross-coach WIP, evidence, and flagship routing; these hooks supply domain content. The progress-file schema is engine-owned (`engine/PROGRESS-SCHEMA.md`); do not redefine it here.

## Hook Map

| Hook | File |
|------|------|
| north-star | [references/north-star.md](references/north-star.md) |
| curriculum | [references/curriculum.md](references/curriculum.md) |
| teaching-elements | [references/teaching-elements.md](references/teaching-elements.md) |
| lab-manager | [references/lab-manager.md](references/lab-manager.md) |
| scorecard-dims | [references/scorecard-dims.md](references/scorecard-dims.md) |
| phase-gates | [references/phase-gates.md](references/phase-gates.md) |
| language | [references/language.md](references/language.md) |
| portfolio | [references/portfolio.md](references/portfolio.md) |

Subject material (phase files, drill banks, glossary) also lives in `references/`; the curriculum hook maps each phase to its file. Read on demand only — never preload every reference at session start.

## Session Sync (cross-machine state)

The student works from two machines (home VM + company bastion) sharing state through
this git repo. The coach runs the sync, not the student's memory:

- **Session start, before reading progress:** inspect `git status`. If the worktree is
  clean and repository synchronization is authorized, pull before reading state; otherwise
  preserve local changes and report the stale-state risk.
- **Session end or Gap Mode stop:** save the progress breakpoint first. Report the changed
  workspace/portfolio files; commit or push only when the user has authorized it. Keep
  learning state and promoted portfolio changes separable when practical.

## Safety Rule

Before any hands-on step, verify `kubectl config current-context`. Only `kind` / `kind-k8s-coach-*` contexts are safe lab targets; any `eks` context is company PRODUCTION. EKS `terraform apply` / `destroy` commands are generated for the user to run by hand, never executed by the coach; every EKS lab ships a destroy step plus a verification command, and all EKS resources use the `billing-dev-eks-*` naming prefix. Machine-specific context details live in `workspaces/k8s/environment.md`.
