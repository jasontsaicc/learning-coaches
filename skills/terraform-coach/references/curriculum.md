# Curriculum

Each phase has a one-line focus, prerequisites, and the reference filename that holds
its detailed teaching material (to be filled in future tasks). Phases are sequential;
the engine enforces prerequisite checks via Routing branch 5.

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
