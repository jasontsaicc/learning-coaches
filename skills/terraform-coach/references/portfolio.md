# Portfolio

## Workspace Directory

Progress files, registries, and in-progress work live in:

```
~/terraform-coach-workspace/
```

This directory is not a public repo. It holds:
- `progress.md`: the engine's progress file (phase status, scorecard history, Mistake
  Registry, spaced repetition queue, breakpoints).
- `term-registry.md`: the student's personal term registry, built incrementally from
  the term cards in `teaching-elements.md`.
- Phase working directories (`p0/`, `p1/`, etc.): scratch space for lab exercises
  that have not yet been promoted to the portfolio.

The student owns and manages this directory. The engine reads and writes `progress.md`
each session.

---

## Portfolio Directory

Artifacts that clear the quality bar ship to:

```
~/tf-portfolio/
```

This is a public (or shareable) repo. Only promote an artifact when it would impress
a senior reviewer who has not seen the backstory.

### Quality Bar

Before promoting any artifact: ask "Would a senior Terraform practitioner reviewing
this for the first time be impressed by the structure, the naming, the state
configuration, and the lack of hardcoded secrets?"

If the answer is no or uncertain, the artifact stays in the workspace until it is
ready.

---

## Per-Phase Artifacts

### P0 - No artifact

P0 builds mental model only. The warm-up diagnostic result is noted in `progress.md`
but produces no public artifact.

### P1 - VPC + EC2 Module (baseline)

**Artifact:** A working Terraform config for a VPC with public and private subnets,
an EC2 instance in the public subnet, and a security group allowing SSH.

**Ships with:**
- `main.tf`, `variables.tf`, `outputs.tf` in a `p1-vpc-ec2/` directory under
  `tf-portfolio/`.
- A `destroy.log` file: the output of `terraform destroy -auto-approve`, confirming
  the resources were cleaned up after the lab (no orphaned resources, no runaway cost).
- A short `README.md` (3-5 sentences) explaining what the config does and what the
  state file tracks.

### P2 - Reusable VPC Module

**Artifact:** A reusable VPC module called from a root config for two environments
(dev and prod) with different CIDR inputs.

**Ships with:**
- `modules/vpc/` directory with `main.tf`, `variables.tf`, `outputs.tf`.
- `envs/dev/main.tf` and `envs/prod/main.tf` calling the module.
- A `destroy.log` for each environment.
- The module is documented: each variable has a `description` attribute.

### P3 - Remote State Configuration

**Artifact:** The P2 config extended with a remote S3 + DynamoDB backend for the dev
environment.

**Ships with:**
- Backend block in `envs/dev/main.tf` pointing to an S3 bucket and DynamoDB table.
- A `backend-setup/` directory with the Terraform config used to create the S3 bucket
  and DynamoDB table themselves (bootstrapping the backend).
- A `destroy.log` for the backend setup as well as the dev environment.

### P4 - Multi-Environment Layout with CI Pipeline

**Artifact:** A complete directory-per-environment layout (dev, staging, prod) wired
into a GitHub Actions (or equivalent) pipeline.

**Ships with:**
- `.github/workflows/terraform.yml` (or equivalent) with: a plan step on PR open and
  push, a manual approval step before apply, apply running only on merge to main.
- State is separate per environment (separate S3 prefixes or separate backend configs).
- A `destroy.log` for each environment used during development.
- Pipeline run screenshot or log showing a plan output and a manual approval event.

### P5 - Policy-Checked Config with Drift Remediation

**Artifact:** Any of the above configs with tfsec integrated into the CI pipeline and
at least one OPA policy enforcing a team naming convention or tag requirement.

**Ships with:**
- `tfsec` findings and remediation: a before-and-after diff showing the original
  misconfiguration and the HCL fix.
- An OPA policy file (`.rego`) and a description of what it enforces.
- A documented drift scenario: description of the out-of-band change, the plan output
  showing it, and the remediation taken.

### P6 - Complete Portfolio + Mock Result

**Artifact:** A clean `tf-portfolio/` with all phase artifacts present, plus:
- A written mock result: the design produced during the P6 gate (three-tier web app
  layout), with module structure, state config, and CI/CD approach documented.
- The P6 gate scorecard printed from the session.
