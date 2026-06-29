# Plugin Interface

This file defines the contract between the engine and a domain coach. The engine
provides all session mechanics (Feynman Gate, Failure Escalation, Phase Gate protocol,
Tiered Scorecard, Spaced Repetition, Gap Mode, Weekly Review). A coach provides only
the domain-specific content described here.

A coach is a directory under `skills/<coach-name>/` with a thin `SKILL.md` entry
point and a `references/` folder containing hook files. The engine reads the hook
files to fill its steps with domain content. The coach does not re-implement mechanics.

The per-student progress file is engine-owned: its schema is defined once in
`PROGRESS-SCHEMA.md`. A coach must not redefine its fields; it supplies only the
workspace path (via the portfolio hook) and any optional domain registries.

---

## Required vs Optional

| # | File | Required | Engine default if absent |
|---|------|----------|--------------------------|
| 1 | `references/north-star.md` | Yes | n/a |
| 2 | `references/curriculum.md` | Yes | n/a |
| 3 | `references/teaching-elements.md` | Yes | n/a |
| 4 | `references/lab-manager.md` | Yes, only for hands-on domains | skip hands-on step D |
| 5 | `references/scorecard-dims.md` | Yes | n/a |
| 6 | `references/phase-gates.md` | Yes | n/a |
| 7 | `references/language.md` | No | English; no ramp |
| 8 | `references/narrative.md` | No | no named peer persona |
| 9 | `references/portfolio.md` | Yes | n/a |

Hooks 1-6 and 9 are required for every coach. Hooks 7 (language) and 8 (narrative)
are optional; the engine uses its defaults when they are absent. Hook 4 (lab-manager)
is required only for domains with hands-on command execution; a purely conceptual coach
may omit it and the engine skips Teaching Flow step D.

---

## Hook Specifications

### Hook 1 — `references/north-star.md` (required)

**What the engine expects:** a single, unambiguous win condition that defines "done"
for this coach, plus a tie-break rule the engine applies when two valid paths compete
for session time.

The engine reads this at the start of every session to anchor routing decisions. If
the win condition is vague, the engine cannot distinguish a finished student from an
incomplete one.

**Contents:**
- One-sentence win condition (what the student must be able to do or demonstrate).
- Tie-break rule (when in doubt, prioritize X over Y).

**Examples:**

| Coach | Win condition (one line) |
|-------|--------------------------|
| sd-coach | Student can design any classic distributed system from scratch under interview constraints, with justified trade-offs. |
| k8s-coach | Student can operate a production-grade Kubernetes cluster, debug failures end-to-end, and pass CKA-level questions without hints. |
| terraform-coach | Student can write, plan, and apply production Terraform for AWS from scratch and explain every resource and dependency. |

---

### Hook 2 — `references/curriculum.md` (required)

**What the engine expects:** a structured phase list the engine uses to sequence
sessions, gate progression, and resolve prerequisite checks (Routing branch 5).

**Contents:**
- Named phases in order (e.g., Phase 1: Foundations).
- Per-phase focus (topic scope, not time estimate).
- Prerequisites per phase (what must be mastered before entering).
- Per-phase reference pointer (the subset of `teaching-elements.md` that applies).
- Optional warm-up diagnostic for new students (used in Routing branch 1).

**Examples:**

| Coach | Phase 1 focus |
|-------|---------------|
| sd-coach | Core building blocks: load balancers, caches, databases, queues; no full-system design yet. |
| k8s-coach | Cluster anatomy and control plane: nodes, API server, etcd, scheduler, kubelet; no networking yet. |
| terraform-coach | HCL syntax, providers, resources, variables, outputs; no modules or remote state yet. |

---

### Hook 3 — `references/teaching-elements.md` (required)

**What the engine expects:** domain content that fills Teaching Flow steps B, C, D,
and E. The engine calls into this file to get the scenario, the first-principles chain,
the lab script, and the drill format for each topic.

**Contents:**
- Per-topic entry covering:
  - Scenario intro (step B): a real-world situation that makes the topic relevant.
  - First-principles chain (step C): the underlying constraint or property that
    forces this design to exist, before surface-level mechanics are introduced.
  - Chunk list: the ordered sub-units for this topic, each with its own Feynman Gate.
  - Hands-on lab (step D): the specific commands or tasks to run; see also hook 4.
  - Drill format (step E): the failure or recall drill for this topic.
- A term registry if the domain has a dense vocabulary.

**Examples:**

| Coach | First-principles chain for a core topic |
|-------|------------------------------------------|
| sd-coach | Networks have finite bandwidth and latency; a cache exists because re-computing or re-fetching the same value costs more than storing it. |
| k8s-coach | A container is an isolated process; a Pod is the scheduling unit because co-located containers share a network namespace. |
| terraform-coach | Cloud APIs are stateful; Terraform maintains a state file so it can compute a diff between desired and actual, rather than re-creating every resource. |

---

### Hook 4 — `references/lab-manager.md` (required for hands-on domains)

**What the engine expects:** how to set up the lab environment and how to verify that
a lab step completed correctly. The engine calls this during Teaching Flow step D.

Without this hook the engine skips step D entirely. Coaches for domains where
command-line execution is integral to understanding (Kubernetes, Terraform, Linux
systems) must provide it.

**Contents:**
- Lab environment setup: tool versions, cluster or account requirements, how to
  confirm the environment is ready before a session.
- Per-topic lab steps: exact commands or task descriptions.
- Verification criteria for each step: the observable output or state change that
  proves the step succeeded. Verification must be objective (a command output, a
  resource status, a diff), not self-reported.
- Teardown instructions: how to leave the environment clean after a session.

**Examples:**

| Coach | Verification approach |
|-------|-----------------------|
| sd-coach | No hands-on execution; omit this hook. |
| k8s-coach | `kubectl get pod -n <ns> -o jsonpath='{.status.phase}'` returns `Running`; CrashLoopBackOff in events confirms the failure scenario. |
| terraform-coach | `terraform plan` shows zero changes after apply; `terraform state list` confirms the expected resources are tracked. |

---

### Hook 5 — `references/scorecard-dims.md` (required)

**What the engine expects:** the scorecard dimensions the engine uses in Teaching Flow
step G and Weekly Review. The engine enforces a fixed 60% pass threshold and a
cumulative-tier structure; this hook defines what is measured at each tier.

**Contents:**
- Primary (always-on) dimension: the single most important quality signal for this
  domain, present at every tier.
- Per-tier added dimensions: what new criteria are added when the student advances
  from one phase tier to the next.
- Optional rubric notes per dimension (what a pass looks like vs. a fail).

The engine will not modify the 60% threshold. Coaches that want stricter pass
conditions should raise the bar inside individual phase-gate pass conditions
(hook 6), not here.

**Examples:**

| Coach | Primary (always-on) dimension |
|-------|-------------------------------|
| sd-coach | Can the student justify a design trade-off with a concrete reason, not just name the pattern? |
| k8s-coach | Can the student trace a failure from symptom to root cause using only `kubectl` output? |
| terraform-coach | Can the student explain what the state file records and why each resource attribute matters? |

---

### Hook 6 — `references/phase-gates.md` (required)

**What the engine expects:** pass conditions for each phase. The engine enforces the
3-attempt cap and the failure protocol; this hook defines what "pass" means in the
domain.

**Contents:**
- Per-phase gate: a concrete pass condition tied to observable student behavior,
  not a time-on-task target.
- Suggested gate questions or tasks (the engine may vary these across attempts).
- Any domain-specific criteria that raise the bar beyond the scorecard threshold
  (e.g., "must explain three failure modes without prompting").

**Examples:**

| Coach | Phase 1 gate pass condition |
|-------|-----------------------------|
| sd-coach | Student designs a URL shortener end-to-end (data model, API, cache, scale path) with justified trade-offs, scoring 60% on the tier-1 scorecard. |
| k8s-coach | Student explains the path of a Pod creation request (client → API server → etcd → scheduler → kubelet) without reference material, scoring 60% on the tier-1 scorecard. |
| terraform-coach | Student writes a Terraform config for a VPC + EC2 instance from scratch, plans it, applies it, and explains what the state file now contains, scoring 60% on the tier-1 scorecard. |

---

### Hook 7 — `references/language.md` (optional)

**Engine default if absent:** English only; no ramp policy; no code-switching.

**What the engine expects:** the default language for this coach and the ramp policy
for students who want to transition between languages (e.g., start in their native
language and gradually shift to English).

**Contents:**
- Default language for the coach.
- Ramp policy: when and how the coach introduces a second language (e.g., introduce
  English technical terms in parentheses first, then shift terminology, then shift
  full sentences).

**Examples:**

| Coach | Language policy |
|-------|-----------------|
| sd-coach | English default; no ramp. |
| k8s-coach | English default with Traditional Chinese anchors for key concepts; ramp to full English over Phase 2. |
| terraform-coach | English default; no ramp. |

---

### Hook 8 — `references/narrative.md` (optional)

**Engine default if absent:** no named peer persona; the confused peer in
Teach-to-Learn is anonymous.

**What the engine expects:** the persona details for the confused peer used in
Teaching Flow step F (Teach-to-Learn) and any other narrative framing the coach
uses across sessions. The engine owns the Teach-to-Learn loop structure; this hook
adds character details only.

**Contents:**
- Peer persona: name, domain background, personality (optional but makes the drill
  more engaging).
- Any recurring narrative framing (e.g., "you are the on-call engineer and your
  teammate is new").

**Examples:**

| Coach | Peer persona |
|-------|--------------|
| sd-coach | Alex, a backend engineer who understands APIs but has never thought about scale before. |
| k8s-coach | Sam, a developer who only knows Docker and keeps asking why Kubernetes can't just be a big Docker host. |
| terraform-coach | Riley, an ops engineer who manages infrastructure by clicking in the AWS console and is skeptical of "just writing code for it." (example only; terraform-coach runs anonymous) |

---

### Hook 9 — `references/portfolio.md` (required)

**What the engine expects:** the artifacts the student should have produced by the
end of each phase and the workspace directory where they live. The engine checks these
during Weekly Review step 6 (artifact audit).

This hook also names the workspace path for the progress file, but it does NOT define
the progress file's schema. That schema is engine-owned and lives in
`PROGRESS-SCHEMA.md`; the coach points there and only adds optional domain registries
(which reuse the schema's registry format).

**Contents:**
- Per-phase artifact list: what the student should have written, built, or produced.
- Workspace directory name: the path (relative to the student's own workspace root)
  where the coach expects artifacts and the `progress.md` file to live.
- Artifact format notes (file extension, naming convention, etc.) if the engine
  needs to locate them automatically.
- Optional domain registries the coach declares (term, command, etc.), each reusing the
  registry fields from `PROGRESS-SCHEMA.md` section 7.

**Examples:**

| Coach | Workspace dir | Phase 1 artifact |
|-------|---------------|------------------|
| sd-coach | `~/sd-coach/` | One written design doc for URL shortener covering data model, API, cache layer, and scale path. |
| k8s-coach | `~/k8s-coach/` | A running kind cluster with one multi-container Pod deployed and `kubectl describe` output saved. |
| terraform-coach | `~/terraform-coach/` | A working Terraform config for a VPC + EC2 instance, with `terraform.tfstate` committed and a short explanation of each resource. |

---

## SKILL.md Contract

The thin `SKILL.md` entry point must:

1. Read the engine at session start: `${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md`
2. Read each hook in `${CLAUDE_SKILL_DIR}/references/` to load domain content.
3. Not re-implement any engine mechanic. The engine text itself is authoritative for
   mechanics. If a mechanic is duplicated in `SKILL.md`, the lint script will flag it.

The recommended structure for `SKILL.md`:

```
# <Domain> Coach

Read engine: ${CLAUDE_SKILL_DIR}/../../engine/ENGINE.md
Read hooks:
  - ${CLAUDE_SKILL_DIR}/references/north-star.md
  - ${CLAUDE_SKILL_DIR}/references/curriculum.md
  - ${CLAUDE_SKILL_DIR}/references/teaching-elements.md
  - ${CLAUDE_SKILL_DIR}/references/lab-manager.md      # omit if not a hands-on domain
  - ${CLAUDE_SKILL_DIR}/references/scorecard-dims.md
  - ${CLAUDE_SKILL_DIR}/references/phase-gates.md
  - ${CLAUDE_SKILL_DIR}/references/language.md         # optional
  - ${CLAUDE_SKILL_DIR}/references/narrative.md        # optional
  - ${CLAUDE_SKILL_DIR}/references/portfolio.md

[domain-specific routing overrides or context, if any — keep minimal]
```

---

## Adding a New Coach

1. Scaffold the skeleton: `./scripts/new-coach.sh <coach-name>` (add `--no-lab` for a
   conceptual domain, `--with-language` / `--with-narrative` for the optional hooks).
   This stamps `SKILL.md` and the hook files from `templates/coach/`, pre-filled with the
   required structure and `<!-- TODO: -->` markers.
2. Fill every TODO marker with domain content. The engine owns all mechanics and the
   progress-file schema (`PROGRESS-SCHEMA.md`); the hooks supply only domain content.
3. Run `./scripts/lint-coach.sh <coach-name>`. It fails while any TODO remains and checks
   that each hook has its required structure, so a scaffolded-but-unfilled coach cannot
   pass. Fix any reported issues before committing.

Doing it by hand instead of scaffolding is fine; the lint enforces the same contract
either way.
