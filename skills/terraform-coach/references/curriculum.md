# Curriculum

Each phase has a one-line focus, prerequisites, and the reference filename that holds
its detailed teaching material (to be filled in future tasks). Phases are sequential;
the engine enforces prerequisite checks via Routing branch 5.

---

## Senior Fast Path(2026-08-11 規劃,Jason 專用入口;取代 P0-P6 全程)

背景:學員日常管 1,500+ AWS resources(Terraform + Terragrunt、multi-account、GitLab CI
plan/apply + approval、PR review)。P0-P4 的內容是他的日常,warm-up 必為 strong。本 fast path
只教工作逼不出來的部分,6 場,每場含 lab(用 `lab-iac`,不碰公司帳號)。

**排程與預算:** 插在 k8s-coach 的 P3 之後、P5 之前(見 workspaces/k8s/curriculum-plan §10.1),
借 k8s 檔期,不新增每週配額。預估起跑 ~2026-10,6 場約 3 週。workspace 於 s1 由 coach 建立
(engine schema)。

**Session 計畫:**

| 場 | 主題 | 核心內容 | Lab / 驗收 |
|---|------|---------|-----------|
| s1 | Module 作者視角 | 消費 module 和設計 module 是兩件事:interface 合約(variables/outputs/validation)、semver 與 breaking change 發佈策略、對 70% 消費者 roll out 的節奏 | 把一個自家常用 pattern 抽成 module,發 v1 → 設計一次 v2 breaking change 的遷移路徑 |
| s2 | 測試 | native `terraform test`(1.6+)、plan assertion、terratest 概念對照、CI 裡的 test 層級(validate → plan assert → apply test)| 給 s1 的 module 寫測試,CI 綠燈 |
| s3 | State surgery I | `moved`/`removed` blocks、`state mv`、import blocks(1.5+)、brownfield import | 把一組手建資源 import 進 module 管理,全程零 destroy |
| s4 | State surgery II | 拆 monolithic state(搬 resource 不炸環境)、lock 丟失 / state 損毀的 incident 處置(面試高頻)| 把一個 state 拆成兩個,plan 前後皆零 diff |
| s5 | Policy & drift | OPA/tfsec/checkov 進 CI gate、drift 偵測策略、fleet 規模的 reconcile 決策(自動修 vs 告警 vs 忽略)| 給 lab repo 上一道會擋錯誤的 policy gate |
| s6 | Interview sprint + gate | 限時 mock:secrets in state、locking 機制與丟失、workspace vs dir-per-env 取捨、「怎麼把 breaking change 推給全公司」(直接用他 GitLab template 的真實故事練)| Examiner gate:一題 state surgery 實作 + 一題設計口試 |

**明確不教(工作已覆蓋或 ROI 不足):** HCL 基礎、backend 設定、Terragrunt 操作、
provider plugin 內部、state schema versioning。

**與 k8s P5 的接口:** s1-s6 的 module + 測試 + policy gate 直接沿用到 k8s P5 的
EKS prod terraform capstone,不重做。

---

## Warm-Up Diagnostic (new students only)

Open with: "You need to create an EC2 instance in a new AWS account using Terraform.
Walk me through what you would write and what commands you would run."

Listen for: whether the student knows what a provider block is, what `init` does,
and what the state file is for. Classify: strong (can sketch the flow) / mid (knows
init/apply but not state) / new (no Terraform experience). Record in progress file.

---

## P0 - IaC Mental Model

**Focus:** Understand what problem IaC solves, the declarative model vs. imperative
scripts, and what the state file is and why it exists.

**Prerequisites:** Familiarity with AWS (can log in, knows what EC2 and S3 are).
No Terraform experience required.

**Reference file:** `references/p0-iac-mental-model.md` (to be created in a future task)

---

## P1 - HCL and Provider/Resource Basics

**Focus:** Write valid HCL; understand provider configuration, resource blocks,
variables, outputs, and data sources. Run init/plan/apply on a simple config.

**Prerequisites:** P0 gate passed — student can explain the declarative model and
the purpose of state.

**Reference file:** `references/p1-hcl-provider-resource.md` (to be created in a future task)

---

## P2 - Modularization and DRY

**Focus:** Extract repeated config into modules; understand module inputs, outputs,
and the difference between a root module and a child module. Use the public registry.

**Prerequisites:** P1 gate passed — student can write a working HCL config for a
VPC + EC2 instance from scratch.

**Reference file:** `references/p2-modularization.md` (to be created in a future task)

---

## P3 - State Management

**Focus:** Move state to a remote backend (S3 + DynamoDB for AWS); understand state
locking, state drift, and the consequences of concurrent `apply` without a lock.

**Prerequisites:** P2 gate passed — student can author and call a reusable module.

**Reference file:** `references/p3-state-management.md` (to be created in a future task)

---

## P4 - Multi-Environment and CI/CD Integration

**Focus:** Manage dev/staging/prod with workspaces or directory-per-env layouts;
wire `terraform plan` and `apply` into a CI/CD pipeline with approvals.

**Prerequisites:** P3 gate passed — student can configure a remote backend with
locking and explain what happens when a lock is lost mid-apply.

**Reference file:** `references/p4-multi-env-cicd.md` (to be created in a future task)

---

## P5 - Policy, Security, and Drift

**Focus:** Run tfsec/OPA to catch security misconfigurations before apply; detect
and respond to drift (out-of-band changes to managed resources).

**Prerequisites:** P4 gate passed — student can manage multiple environments and
integrate Terraform into a CI pipeline.

**Reference file:** `references/p5-policy-security-drift.md` (to be created in a future task)

---

## P6 - Interview and Hands-On Sprint

**Focus:** Timed mock design and live coding sessions; answer common Terraform
interview questions without reference material; complete the portfolio sprint.

**Prerequisites:** P5 gate passed — student can identify a security misconfiguration
with tfsec and explain the remediation.

**Reference file:** `references/p6-interview-sprint.md` (to be created in a future task)
