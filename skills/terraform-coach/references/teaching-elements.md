# Teaching Elements

This file fills engine Teaching Flow steps C (first-principles chain), D (hands-on),
and E (drill) with Terraform-specific content. The engine owns the step structure and
the Feynman Gate protocol; this file supplies what is Terraform-specific.

---

## Step B: Scenario Intro

Brief production scenarios (one to two lines each) that make each phase topic feel
concrete before the first-principles explanation. The engine surfaces these at step B;
keep them terse.

| Phase | Scenario hook |
|-------|--------------|
| P0 - IaC Mental Model | A new engineer hand-creates an EC2 instance in the console; six months later no one knows it exists, it can't be updated safely, and deleting it would break prod. |
| P1 - HCL and Providers | You clone a repo and run `terraform apply` but get "provider not found"; `terraform init` was never run after the provider version changed. |
| P2 - Modularization | Three teams copied the same VPC block into their configs; a CIDR typo in one copy caused an outage, and the other two copies still have the bug. |
| P3 - State Management | Your team shares one remote state file with no lock. A teammate's apply and yours ran close together; last write won, and the other apply's tracked changes silently vanished from state. |
| P4 - Multi-Environment and CI/CD | A dev `terraform apply` accidentally ran against the prod backend because the workspace was not switched; the prod database was replaced. |
| P5 - Policy, Security, and Drift | A support engineer opened port 22 to `0.0.0.0/0` in the console to debug a prod issue; the next `terraform apply` would have reverted it, but the team only noticed three weeks later during a security audit. |
| P6 - Interview Sprint | You're asked in an on-site: "walk me through how you'd design Terraform state for a team of 20 engineers across dev, staging, and prod." |

---

## Step C: First-Principles Chain

### Core First-Principles Chain (applies to all phases)

Cloud APIs are stateful: creating a resource returns an ID and initial attributes,
but there is no way to enumerate all cloud resources and reconstruct the full picture
of what Terraform manages. Terraform maintains a state file to track resource
identities (IDs), metadata, cross-resource reference values, and destroy ordering --
information that a blind cloud enumeration cannot reconstruct.

The state file is not there to avoid API calls. `terraform plan` calls the provider's
read APIs on every run by default (implicit refresh) to detect drift. State exists so
Terraform knows *which* resources to call those APIs for, and can reconstruct
references and ordering without scanning every resource in the account.

This single constraint explains why the state file exists, why remote state matters,
why locking matters, and why drift is dangerous.

**Teach this chain before any surface-level HCL mechanics.** The specific derivation:

1. Cloud resources have IDs, ARNs, and attributes that must be tracked to manage them
   later (delete, update, reference from other resources).
2. Without a state record, Terraform could not know which cloud resources it manages
   (the API has no "list everything Terraform created" endpoint), could not resolve
   cross-resource references at plan time, and could not determine destroy order.
3. The state file is that record: it maps each resource block in HCL to a real cloud
   object with its identity and last-known attributes.
4. `terraform plan` performs an implicit refresh by default:
   it reads the state file for resource IDs, calls the provider's read APIs for each
   tracked resource to get live actual state, then diffs that refreshed-actual against
   the desired HCL, then emits the plan. Use `-refresh=false` to skip the live API
   calls. The standalone `terraform refresh` command was deprecated as unsafe
   because it writes refreshed state back without a reviewable plan.
5. A shared team using the same state file without a lock can run two concurrent
   `apply` operations: both read the same state, compute their changes, and both write
   an updated state file back -- last write wins, silently dropping the other apply's
   tracked changes from state. That is why remote state + locking is not optional at
   team scale.

### Dependency Graph and Plan Order (step C deep-dive for P1-P2)

The plan does not apply resources in the order they appear in `.tf` files. Terraform
builds a directed acyclic graph (DAG) of resource dependencies, derived from
references between blocks (e.g., `aws_subnet.this.id` in a route table resource
creates an edge from the subnet to the route table).

**Key points for student understanding:**
- A resource that references another can only be created after the referenced resource
  exists. The DAG captures this constraint and orders the apply accordingly.
- Resources with no dependency relationship can be applied in parallel. Terraform runs
  parallel `apply` operations by default, which makes large applies tractable by
  reducing wall-clock time compared to a strictly sequential apply. Plan itself makes
  read-only API calls and is generally faster than apply, which provisions resources
  and waits on creation (often minutes per resource); parallelism narrows the gap but
  does not reverse it.
- `terraform graph | dot -Tpng > graph.png` produces a visual DAG. Teach this in P1
  so students have a concrete way to reason about apply order.
- If the DAG contains a cycle, Terraform errors before apply. Cycles usually indicate
  a circular resource reference that must be broken with a `depends_on` or refactoring.

**Feynman Gate question (Transfer stage):** "If I have an `aws_security_group` and an
`aws_instance` that references it, which gets created first and why? What does the DAG
look like?" (Expected: security group first, because the instance block references
`aws_security_group.this.id`, creating a directed edge. The DAG orders sg before
instance.)

---

## Step D: Hands-On Lab

The engine calls this step after the first-principles chain is taught. Commands are
generated and run in the student's lab environment (see `lab-manager.md` for setup).

### Standard HCL Write-Plan-Apply Sequence

For each new topic, the hands-on follows this three-step pattern:

**1. Write the HCL.** The student writes the resource block(s) from scratch, not
from a template. The coach provides the resource type and required attributes; the
student figures out the block syntax. Example starting point: "Write an S3 bucket
resource named `my-demo-bucket` with versioning enabled."

**2. Run `terraform plan`.** Student runs:
```
terraform init      # only if this is a new config or providers changed
terraform plan -out=tfplan
```
The coach asks the student to read the plan output aloud and explain: what will be
created/modified/destroyed, what the `+` / `~` / `-` symbols mean, and whether the
plan matches the intent of the HCL.

**3. Apply and inspect state.** Student runs:
```
terraform apply tfplan
terraform state list
terraform state show <resource_address>
```
The coach asks: "What does the state file now contain for this resource? Why did
Terraform store `arn` and `id` but not `tags_all` from the plan output?"

### Drift Injection Lab (step D for P3-P5)

After a resource is applied and state is clean, inject out-of-band drift:
- In the AWS Console (or via AWS CLI), change a resource attribute that is tracked
  in state (e.g., change the S3 bucket's versioning setting, add a tag to an EC2
  instance, modify a security group rule).
- Have the student predict: "What will `terraform plan` show now, and why?"
- Run `terraform plan` and compare the student's prediction to the actual output.
- Discuss: how does Terraform detect the change? (Plan performs an implicit refresh:
  it uses the resource IDs in state to call provider read APIs, gets the current live
  attributes, then diffs those against the desired HCL. Drift appears because the live
  attribute no longer matches what the HCL declares.)

This drill converts the abstract concept of drift into a concrete observable.

---

## Step E: Drill

### Drill 1 - Idempotency Check

After a clean apply (plan shows 0 changes), run plan a second time without touching
any HCL. Expected: 0 changes. If the provider is not idempotent (rare but real),
plan will show unexpected changes every time.

Ask: "Why should a second `terraform plan` after a successful `apply` always show zero
changes? What would it mean if it does not?" (Expected answer: the apply brought
actual state into alignment with desired state; the state file now matches both. If
plan still shows changes, either the provider is normalizing attribute values
differently on read vs. write, or something out of band changed the resource.)

### Drill 2 - Dependency Removal

Add a resource B that depends on resource A. Apply both. Then remove resource B from
the HCL. Run plan. Ask the student to predict the plan before running it.

Expected: plan shows only the destruction of B, not A. Extend: "What if you removed
both A and B but in a dependency order that would require destroying A first?" (This
surfaces the dependency-ordering question for destroys: Terraform reverses the DAG
for destruction.)

### Drill 3 - State Corruption Scenario (verbal, P3+)

Without running any commands, ask the student: "Your team's remote state file in S3
was manually deleted. You still have the local `.terraform` directory. What is the
impact, and what are your recovery options?" Evaluate whether the student understands:
- The state file, not the HCL, is the source of truth for what Terraform manages.
- Without state, `terraform plan` treats all resources as new (it does not know they
  exist) and will try to recreate them, likely failing on duplicate-resource errors.
- Recovery: `terraform import` each resource, or restore from an S3 versioned backup.

---

## Term Registry

Key Terraform vocabulary, with the underlying concept each term points to.

| Term | What it points to (not just a definition) |
|------|------------------------------------------|
| `terraform init` | Downloads provider plugins and sets up the backend; must run before any other command or after provider version changes |
| provider | A plugin that translates HCL resource blocks into API calls for a specific cloud or service |
| resource | A single managed cloud object (an EC2 instance, an S3 bucket); the unit of state tracking |
| data source | A read-only reference to an existing resource not managed by this config; does not appear in state as a managed object |
| state file (`terraform.tfstate`) | The mapping between HCL resource addresses and real cloud resource IDs and attributes |
| plan | A diff between desired HCL and live actual state; by default performs an implicit refresh (calls provider read APIs for each tracked resource) before computing the diff; skip the refresh with `-refresh=false` |
| apply | Execute the plan: call provider APIs to create/modify/destroy resources and update state |
| module | A reusable bundle of resources with declared inputs (variables) and outputs; can be called multiple times with different inputs |
| remote backend | Where the state file is stored (e.g., S3); enables team use by making state shareable |
| state lock | A mechanism (e.g., DynamoDB) that prevents two concurrent `apply` operations from racing on the same state file |
| workspace | A named state file within the same backend config; one way to separate dev/staging/prod state |
| drift | A difference between the live cloud resource and what the state file records, caused by out-of-band changes |
| `terraform import` | Bring an existing cloud resource under Terraform management by writing its attributes into state |
| `terraform taint` (deprecated) | Force a resource to be destroyed and recreated on next apply; replaced by `-replace` flag |
| `-replace` flag | `terraform apply -replace=<address>` forces a specific resource to be recreated even if the plan shows no changes |
| DAG | Directed acyclic graph of resource dependencies; determines apply and destroy order |
| HCL | HashiCorp Configuration Language; the syntax used in `.tf` files; not a general-purpose language, not YAML |
| output | A named value exported from a module or root config; used to pass values between modules or display results |
| variable | A declared input to a config or module; can be set via `.tfvars`, environment variables, or `-var` flags |
| `terraform.tfvars` | A file of variable values loaded automatically; do not commit secrets here |
| `locals` | Named intermediate values computed within a module; not exposed as inputs or outputs |
