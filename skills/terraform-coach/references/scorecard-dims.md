# Scorecard Dimensions

These dimensions stack on the engine's Tiered Scorecard frame (defined in ENGINE.md).
The 60% pass threshold is the engine's and is not redefined here. Each tier adds
dimensions on top of all previous tiers; the primary dimension is present at every tier.

---

## Primary Dimension (always on, all tiers)

**Can the student explain the underlying mechanism, not just write the HCL?**

Pass: the student states why a resource block or command works the way it does, tracing
it to the underlying constraint (state file, DAG, provider plugin, API call). Writing
correct HCL is necessary but not sufficient to pass this dimension.

Fail: the student produces working HCL but cannot answer "why does this block look like
this?" or "what does Terraform actually do when you run plan here?"

This dimension is intentionally hard to satisfy by memorization. A student who can
recite syntax but cannot explain mechanism fails it.

---

## Tier 1 (P0-P1 phases)

Dimensions in use: Primary only.

At this tier, the student is building the foundational mental model. One dimension
keeps the bar honest without overwhelming a beginner.

---

## Tier 2 (P2-P3 phases)

Adds: **State safety**

**State safety:** Does the student demonstrate awareness of what can corrupt or lose
state, and do they handle remote backend configuration and locking correctly?

Pass: the student configures a remote backend with a locking mechanism, and when asked
"what happens if two engineers run apply at the same time without a lock?", gives a
correct answer (race condition on state write, possible corruption or partial apply).

Fail: the student treats state as an implementation detail and cannot describe a
scenario where state loss would cause real harm.

---

## Tier 3 (P4-P5 phases)

Adds: **Idempotency and drift understanding**

**Idempotency and drift:** Does the student understand that a second plan after a clean
apply should show zero changes, and can they identify and diagnose drift when it appears?

Pass: the student can predict what a plan will show after a drift event, explain how
Terraform detects the drift (attribute comparison between state and live cloud), and
describe how to bring state back into sync.

Fail: the student is surprised by drift appearing in a plan, or cannot distinguish
"provider normalization noise" from "genuine drift."

---

## Tier 4 (P5-P6 phases)

Adds: **Cost awareness** and **Blast radius**

**Cost awareness:** Before running apply on a config that provisions compute or storage,
does the student estimate cost impact and flag anything that could cause runaway spend?

Pass: the student names the resource types most likely to incur cost, mentions instance
size and storage class when relevant, and raises a question before applying if a plan
includes unexpectedly large or persistent resources.

Fail: the student applies without considering cost, or is unaware that certain resource
types (e.g., NAT gateways, data transfer, large RDS instances) have significant ongoing
cost.

**Blast radius:** Does the student read the plan before applying and flag any
destruction or replacement that could affect production?

Pass: before running apply, the student reads the plan for `-` (destroy) and `~`
(replace-forces-new) symbols, names what will be destroyed, and confirms the impact is
intentional. For a plan that destroys a database or a running instance, the student
pauses and asks whether this is expected.

Fail: the student runs `terraform apply` without reading the plan, or does not notice
a forced replacement of a stateful resource.
