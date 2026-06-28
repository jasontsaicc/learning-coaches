# Phase Gates

One pass condition per phase. Pass conditions are scope-based, not time-based.
The engine enforces the 3-attempt cap and the failure protocol; this file defines
what "pass" means for each phase. See ENGINE.md for the gate mechanics.

---

## P0 Gate - IaC Mental Model

**Pass condition:** The student explains declarative vs. imperative infrastructure
management without prompting, and correctly states what the state file is for.

Specifically, the student must be able to:
1. Distinguish declarative ("describe what you want") from imperative ("describe what to
   do") without looking at notes.
2. Explain why Terraform needs a state file even though it already queries the cloud on
   every plan run. (Expected: the state file tracks resource identities, metadata,
   cross-resource reference values, and destroy ordering -- information that a blind
   cloud enumeration cannot reconstruct.)
3. Name one real consequence of losing the state file.

**Suggested gate question:** "Explain to me what the state file is for. Terraform
already queries the cloud on every plan run -- so why is the state file still
necessary?"

---

## P1 Gate - HCL and Provider/Resource

**Pass condition:** The student writes a working Terraform configuration for a VPC +
EC2 instance from scratch, plans it, and explains what the state file contains after
apply — without referring to notes.

Specifically, the student must:
1. Write the provider block, VPC resource, subnet resource, and EC2 instance resource
   with correct references between them (e.g., `vpc_id = aws_vpc.this.id`).
2. Run `terraform plan` and read the plan output, identifying what will be created and
   in what order.
3. After apply, run `terraform state show aws_instance.<name>` and explain why the
   state contains fields that were not in the HCL (e.g., private IP, ARN, security
   group defaults assigned by AWS).

Scoring against Tier 1 scorecard; must meet the engine's scorecard pass threshold on the Tier 1 scorecard.

---

## P2 Gate - Modularization

**Pass condition:** The student extracts a reusable VPC module, calls it twice with
different input variables (e.g., dev and prod CIDRs), and explains the difference
between a root module and a child module.

Specifically:
1. Module has declared `variable` inputs and at least one `output` that the root module
   uses.
2. Student can answer: "Why would you use a module here instead of copying the resource
   blocks?" (Reuse, single point of change, testability — must give a concrete reason,
   not just "DRY".)
3. Student knows what `terraform init` does when a new local module path is added.

---

## P3 Gate - State Management

**Pass condition:** The student designs a remote backend configuration using S3 + DynamoDB
for an AWS project, explains what the DynamoDB table is for, and explains what happens
if the lock is lost mid-apply.

Specifically:
1. Writes a valid `backend "s3"` block with `dynamodb_table` set.
2. Explains the DynamoDB lock entry: what key it uses, what happens if it is not
   released (apply crashes), and how to manually remove a stuck lock (`terraform force-unlock`).
3. Answers: "Two engineers run `terraform apply` at the same second. What happens with
   the lock? What happens without it?" (With lock: one waits or errors out. Without:
   both read state, compute plans, both write state — last write wins and the loser's
   changes are silently lost from state.)

---

## P4 Gate - Multi-Environment and CI/CD

**Pass condition:** The student describes and implements a working layout for managing
dev and prod environments with separate state, and explains how `terraform plan` fits
into a CI/CD pipeline with a manual approval gate before apply.

Specifically:
1. Chooses between workspaces and directory-per-env and justifies the choice for a
   given scenario (key trade-off: workspaces share backend config; directory-per-env
   allows different provider configs and backend paths per env).
2. Draws or describes a CI pipeline where plan output is posted for review and apply
   only runs after explicit approval — names which CI event triggers which step.
3. Answers: "What should the pipeline do if `terraform plan` exits non-zero?" (Block
   the pipeline; do not apply a broken plan.)

---

## P5 Gate - Policy, Security, and Drift

**Pass condition:** The student runs tfsec against a config with at least one known
misconfiguration, identifies the finding, explains the underlying security risk, and
writes the remediation in HCL.

Additionally:
1. Explains what drift is and gives a concrete example of how it could appear in a
   production environment (e.g., a team member adjusts a security group in the console
   to unblock a debug session and forgets to revert it).
2. Describes how to detect drift (`terraform plan` compares state to live cloud) and
   the two remediation paths: update HCL to match the drift (if intentional) or
   `terraform apply` to revert it (if unintentional).
3. Explains one OPA use case: what kind of policy would you enforce with OPA that
   tfsec cannot check? (Example: organizational tag requirements, naming conventions,
   resource count limits.)

---

## P6 Gate - Interview and Hands-On Sprint

**Pass condition:** The student completes a timed mock session (scope: design a
production Terraform layout for a standard three-tier web app on AWS) and meets the
engine's scorecard pass threshold on the Tier 4 scorecard without reference material.

The mock covers:
- Module structure for the layout.
- Remote state configuration with locking.
- How CI/CD would handle plan approval.
- One security consideration caught by tfsec.
- Blast radius analysis of a hypothetical "terraform apply" that replaces the RDS
  instance.

Portfolio must be complete (see `portfolio.md`) before the gate is attempted.
