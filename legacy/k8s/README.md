**[English](README.md)** | **[繁體中文](README.zh-TW.md)**

# k8s-coach: Kubernetes / SRE Coaching Skill

> Not YAML memorization. Not CKA cram sheets.
> Your AI becomes a Socratic mentor who traces every k8s mechanism to the OS, network, and distributed-systems primitive underneath, then makes you debug it in a real cluster.

An AI coaching skill for Claude Code that turns your AI into a structured Kubernetes / SRE interview coach. Feynman method, first-principles derivation, and hands-on chaos drills. Part of the same family as `sd-coach` and `leetcode-coach`.

---

## North Star

**Pass big-tech senior DevOps / SRE interviews and land a strong offer.**

Drilling to first principles (OS, networking, distributed systems, control theory) is the means, not the end. Every trade-off in the curriculum comes back to one question: does this help the interview and the package?

---

## 8-Phase Curriculum Map

| Phase | One-line Focus |
|-------|----------------|
| **P0 Mental Model** | Declarative API, reconcile loop, control plane anatomy, apply to Running full flow |
| **P1 Core Objects + Container Internals** | Pod/probe, Deployment/rollout, StatefulSet/Job, resource/QoS, namespace/cgroup/OOM |
| **P2a Networking Deep Dive** | Service/kube-proxy/CoreDNS, Ingress, NetworkPolicy, CNI, full packet path |
| **P2b Storage + RBAC** | PV/PVC/CSI, StorageClass, RBAC/ServiceAccount, IRSA |
| **P3 Scheduling + High Concurrency + Troubleshooting** | scheduler, affinity/taints, HPA/VPA/Karpenter, PDB, capacity planning |
| **P4 Observability Engineering** | Three pillars, Prometheus/PromQL, SLI/SLO/Error Budget, OTel/Jaeger |
| **P5 Platform Engineering / GitOps** | Helm, ArgoCD/GitOps, EKS prod Terraform, progressive delivery |
| **P6 Interview Sprint** | SRE scenario mocks, k8s x system design crossover, CKA/CKAD speed drills (side track) |

**MVP status:** P0 ships now (reference material complete). P1 through P6 are planned and will be added incrementally.

---

## Install

Prerequisites: `kind`, `kubectl`, and an SSH key registered with your GitHub account.

```bash
git clone git@github.com:jasontsaicc/k8s-mastery-lab-skill.git ~/jason/k8s-coach
mkdir -p ~/.claude/skills && ln -s ~/jason/k8s-coach ~/.claude/skills/k8s-coach
```

The symlink puts the repo on Claude Code's skill path so the skill can read `k8s-coach-workspace/progress.md`.

### Sync across machines

Session state (`progress.md`, mistake/term registries, cluster configs) is tracked in git. To continue on another VM: `git pull` before each session, then `git commit` + `git push` after. Always pull before starting so the two machines never diverge.

---

## How to Start

1. Open Claude Code in this directory (or anywhere `k8s-coach` is on the skill path).
2. Say: **"let's learn Kubernetes"** or **"start k8s-coach"**.
3. The skill reads `k8s-coach-workspace/progress.md` and routes you: new student warm-up, resume from breakpoint, or weekly review.

---

## Lab Environment

Local clusters run on `kind` via a single script:

```bash
scripts/lab-cluster.sh up p0      # spin up a P0 lab cluster
scripts/lab-cluster.sh reset p0   # wipe and recreate (use after chaos drills)
scripts/lab-cluster.sh down p0    # tear down
scripts/lab-cluster.sh status     # list all k8s-coach-* clusters
```

EKS enters the picture at P2a (cloud integration topics). Terraform commands are generated as code blocks for you to run; the skill never touches cloud resources directly.

---

## Workspace and Portfolio

| Path | Purpose |
|------|---------|
| `k8s-coach-workspace/` | Local session state: progress, breakpoints, mistake registry, term registry, cluster configs |
| `k8s-portfolio/` (separate repo) | Public artifact repo: manifests, runbooks, SLO dashboards, GitOps config (what recruiters see) |

Portfolio is initialized on your first P0 session. Every session ends with a `git commit` to `k8s-portfolio` so there is always a tangible output per lesson.

---

## What Makes This Different

**Hands-on + chaos drills, not YAML memorization.**

Each topic follows this cycle:

1. **Derive** the mechanism from the underlying OS / network / distributed-systems principle.
2. **Lab** it in a real `kind` cluster (you type the commands, you observe).
3. **Break it** intentionally (chaos drill) and debug back to root cause within a time-boxed round.
4. **Teach it back** in your own words (Feynman gate) before moving on.
5. **Interview drill** (5 min, every session, non-skippable) to anchor the north star.

Every session ends with a portfolio commit so understanding converts into visible proof of work.

---

## Project Structure

```
k8s-coach/
├── SKILL.md                          # Teaching engine: routing, flow, gates, protocols
├── scripts/
│   └── lab-cluster.sh                # Lab cluster lifecycle manager (kind)
├── references/
│   └── phase-0-mental-model.md       # P0 teaching material (MVP)
├── k8s-coach-workspace/              # Local session state (gitignored from portfolio)
└── evals/                            # Skill validation test cases
```

---

## License

MIT
