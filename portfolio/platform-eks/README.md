# platform-eks

唯一 active flagship：把既有 shop platform 沿同一條演進路徑做成可驗證的
production-shaped EKS platform，而不是另開一個示範專案。

## Problem statement

為 `shop-api` / `shop-web` 提供安全、可觀測、可回滾且成本可解釋的部署平台。
kind 是日常低成本驗證環境；EKS 只用於 IRSA、AWS controller、managed control plane
或雲端拓撲等 kind 無法證明的能力。

## Definition of done

- Terraform module 與 environment layout，plan/test 可在 CI 重現。
- Workload 有 probes、resources、PDB、NetworkPolicy 與最小權限 identity。
- GitOps 或等價的 declarative delivery，包含 staged rollout 與 rollback drill。
- 至少一個 SLI/SLO、dashboard、actionable alert 與對應 runbook。
- 至少一次限時 failure injection，保留 evidence 並產出 postmortem。
- 成本估算列出主要 driver，能說明可靠性與成本的取捨。
- README、runbook、ADR 與 postmortem 的最終版本使用英文。
- 一場隔離 Examiner/design review 通過後才標記完成。

## Milestones

| Milestone | Reuse from current project | Required new evidence | Status |
|---|---|---|---|
| M0 Baseline | `portfolio/k8s/manifests/` 的 shop/ingress/probe 素材 | inventory、可重現部署與 smoke test | planned |
| M1 Security | NetworkPolicy lab、後續 P2b RBAC/IRSA | negative test、identity boundary、threat model | planned |
| M2 IaC | Terraform senior fast path | module tests、zero-diff plan、state safety | planned |
| M3 Reliability | K8s P3/P4 | load test、SLO、alert、runbook | planned |
| M4 Delivery | K8s P5 | GitOps、staged rollout、rollback evidence | planned |
| M5 Incident | troubleshooting 主線 | timeline、evidence、root cause、prevention | planned |
| M6 Review | SD/CA/English mock | architecture critique + Examiner verdict | planned |

## This-week boundary

本週只建立治理與驗收契約，不搬移現有 manifests、不建立雲端資源、不產生成本。
下一個 build session 從 M0 inventory 開始，先證明既有素材能被重現，再新增能力。
