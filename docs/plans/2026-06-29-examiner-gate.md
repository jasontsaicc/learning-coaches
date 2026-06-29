# Examiner Gate (Phase 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an independent Examiner that certifies Phase Gates via a subagent which sees only the gate task, the student's verbatim answer/artifact, and the objective pass criteria — never the teaching transcript — so "did learning actually happen" becomes measurable by a judge that is not the teacher.

**Architecture:** The engine gains one new locked mechanic (`Examiner Gate`). At a Phase Gate, the coach stops self-scoring and instead dispatches an Examiner subagent (the Agent/Task tool) with a fixed payload contract. The examiner returns a structured verdict; the coach records it and runs the existing 3-attempt failure ladder on a fail, and cannot override a fail to a pass. A new append-only `Examiner ledger` in the shared progress schema turns successive verdicts into an outcome curve.

**Tech Stack:** Markdown prose contracts (engine + references), a bash structural linter (`scripts/lint-engine.sh`), Claude Code subagent dispatch (Agent/Task tool) as the runtime that gives the examiner its blind context.

## Global Constraints

- Engine files are domain-neutral. No coach/domain name (`terraform`, `k8s`, `kubernetes`, `system design interview`) may appear in `engine/ENGINE.md`, `engine/PROGRESS-SCHEMA.md`, or any `engine/references/*.md`. `lint-engine.sh` greps for these and fails on a leak.
- `PROGRESS-SCHEMA.md` is a prose contract, not a parsed format. New fields are described in prose; do not invent a YAML/JSON parser.
- The engine specifies WHAT must happen and WHERE the gate is; HOW it sounds stays free. Every new rule must be classifiable as Locked or Free and the Locked ones go in the `## What Is Locked, What Is Free` table.
- Git commits: one-line subject only. No body, no `Co-Authored-By`, no AI attribution. (User hard rule.)
- The examiner is the same model family as the coach; independence is structural (context isolation via subagent), not a claim that a different model judges. The plan's value rests on the coach passing ONLY the contracted payload into the subagent prompt. State this honestly; do not over-claim.

---

## File Structure

| File | Responsibility | Action |
|------|----------------|--------|
| `engine/references/examiner-gate.md` | Full Examiner contract: payload, independence rules, verdict format, LLM-judge failure modes | Create |
| `engine/ENGINE.md` | New `## Examiner Gate` section; one Locked/Free row; pointer from `## Phase Gates` | Modify |
| `engine/PROGRESS-SCHEMA.md` | `certifier` field on scorecard history (§6); new `## 11. Examiner ledger` section; update skeleton | Modify |
| `scripts/lint-engine.sh` | Guards: require Examiner Gate heading, independence keyword, ledger section, examiner-gate.md ref | Modify |
| `skills/terraform-coach/references/phase-gates.md` | Per-gate "Examiner inputs" line naming the objective artifact to pass | Modify |

Order rationale: the linter guards are written first (they are the failing test), each content task makes its guard pass, terraform wiring last, behavioral dry-run as the final acceptance gate.

---

## Task 1: Lint guards for the Examiner Gate (the failing test)

**Files:**
- Modify: `scripts/lint-engine.sh`

**Interfaces:**
- Produces: lint expectations that Tasks 2-3 must satisfy — the literal strings `## Examiner Gate`, `never the teaching transcript`, `## 11. Examiner ledger`, and a non-empty `engine/references/examiner-gate.md`.

- [ ] **Step 1: Add the failing guards to the linter**

In `scripts/lint-engine.sh`, add `"## Examiner Gate"` to the `required` array of ENGINE.md headings (after `"## Phase Gates"`):

```bash
  "## Phase Gates"
  "## Examiner Gate"
  "## Tiered Scorecard"
```

After the existing `burden of proof` guard (line ~34), add the independence lock guard:

```bash
# guard the Examiner independence lock against being gutted
grep -qiF "never the teaching transcript" "$ENGINE" || { echo "MISSING: Examiner independence lock"; fail=1; }
```

In the SCHEMA section, add `"Examiner ledger"` to the required-substring loop:

```bash
for s in "Mistake Registry" "Spaced-repetition" "breakpoint" "Curiosity branch" "Scorecard history" "Examiner ledger"; do
```

Add `engine/references/examiner-gate.md` to the `refs` array:

```bash
  engine/references/anti-sycophancy.md
  engine/references/examiner-gate.md
```

- [ ] **Step 2: Run the linter to verify it fails**

Run: `cd /home/ubuntu/go_senior_devops/learning-coaches && bash scripts/lint-engine.sh; echo "exit=$?"`
Expected: FAIL — prints `MISSING: ## Examiner Gate`, `MISSING: Examiner independence lock`, `MISSING in engine/PROGRESS-SCHEMA.md: Examiner ledger`, `MISSING or EMPTY: engine/references/examiner-gate.md`, and `exit=1`.

- [ ] **Step 3: Commit**

```bash
git add scripts/lint-engine.sh
git commit -m "lint: require Examiner Gate, independence lock, and Examiner ledger"
```

---

## Task 2: Examiner contract reference

**Files:**
- Create: `engine/references/examiner-gate.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the canonical payload contract and verdict format that `ENGINE.md` (Task 3) points to. Must contain the literal phrase `never the teaching transcript` so Task 1's guard passes here OR in ENGINE.md (the lock lives in ENGINE.md; the detail lives here — both reference the same phrase).

- [ ] **Step 1: Write the reference file**

Create `engine/references/examiner-gate.md` with this content:

```markdown
# Examiner Gate: Reference Detail

This file expands the Examiner Gate invariant in ENGINE.md. The teaching coach and the
student spend a whole session building shared context; by gate time the coach has a stake
in the student passing, and an LLM coach drifts toward grade inflation (see
`anti-sycophancy.md`). The Examiner removes that stake by judging from outside the session.

The Examiner is a subagent. Its independence is structural: it receives a fresh context
containing only the contracted payload below. It does not see the conversation, the coach's
opinion, the analogies used, or prior gate attempts. It is the same model family as the
coach, so this is context isolation, not a second opinion from a different model. The
guarantee is only as strong as the coach's discipline in passing nothing beyond the payload.

---

## 1. Payload Contract (what the coach passes in)

The Examiner dispatch prompt contains EXACTLY these four parts and nothing else:

1. **The gate task** — the pass condition and suggested question(s) copied verbatim from the
   coach's `phase-gates.md` hook for the phase under test.
2. **The objective pass criteria** — the numbered "Specifically, the student must..." list
   from that same hook, and the tier scorecard dimensions from `scorecard-dims.md`.
3. **The student's answer, verbatim** — the student's words, and any artifact they produced,
   fenced and unedited: file contents, command output (e.g. a plan or a status), a written
   explanation. The coach does not summarize or improve it.
4. **The attempt number** — which of the 3 attempts this is (the Examiner scores the answer
   in front of it; the coach owns the failure ladder).

Forbidden in the payload: the teaching transcript, the coach's assessment, what analogy was
used, hints the student received, and prior attempts' answers. Leaking any of these voids
the Examiner's independence and is a lint-checked invariant violation.

## 2. Adversarial Default Applies to the Examiner

The Examiner inherits the burden-of-proof stance: the student must earn the pass. The
Examiner leads with the weakest point in the answer, tests it once, and concedes a pass only
if it survives. An answer that recites the right words but cannot survive one probe on the
objective criteria is a Fail. The empty-finding rule applies: an Examiner that finds nothing
to challenge in a weak answer is miscalibrated.

## 3. Verdict Format (what the Examiner returns)

The Examiner returns a structured verdict the coach records without alteration:

- **Per-criterion result** — for each numbered objective criterion: pass / fail + one-line
  reason citing what in the answer satisfied or missed it.
- **Score** — `n/total` against the tier scorecard; the engine's 60% threshold decides
  pass/fail. The coach cannot round up.
- **Footer** — top-improvement (specific, actionable) and best-moment (real, grounded only
  in the answer the Examiner saw; never invented to soften a fail), per `anti-sycophancy.md`.

## 4. LLM-Judge Failure Modes (and the bound on each)

- **Hallucinated pass** — the Examiner certifies an answer that does not meet a criterion.
  Bound: every pass must cite which criterion the answer satisfied and how; a verdict with no
  citation is not a valid pass.
- **Arbitrary harshness** — the Examiner fails an answer for missing something not in the
  criteria. Bound: the Examiner scores only against the supplied objective criteria and
  scorecard dimensions; it may not invent new bars.
- **Criteria starvation** — a coach passes vague criteria, so the Examiner cannot judge
  objectively. Bound: this is a coach hook defect; the gate cannot be administered until the
  hook names objective, checkable criteria. (See `PLUGIN-INTERFACE.md` hook 6.)

## What Stays Free

The Examiner's question phrasing, which probe it leads with, and the wording of its reasons
are free. What is locked: the payload contract (it never sees the transcript), the
burden-of-proof stance, and that the coach cannot override a Fail into a Pass.
```

- [ ] **Step 2: Verify it is non-empty and leak-free**

Run: `cd /home/ubuntu/go_senior_devops/learning-coaches && test -s engine/references/examiner-gate.md && ! grep -qiE 'kubernetes|k8s|kube-proxy|system design interview|terraform' engine/references/examiner-gate.md && echo OK`
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add engine/references/examiner-gate.md
git commit -m "add examiner-gate reference: payload contract and verdict format"
```

---

## Task 3: Examiner Gate engine mechanic

**Files:**
- Modify: `engine/ENGINE.md`

**Interfaces:**
- Consumes: `engine/references/examiner-gate.md` (Task 2) — the new section points to it.
- Produces: the `## Examiner Gate` section, the Locked/Free row, and the `## Phase Gates` pointer that Task 1's guards check for.

- [ ] **Step 1: Add the Locked/Free table row**

In `engine/ENGINE.md`, in the `## What Is Locked, What Is Free` table, add this row after the Phase Gate cap row:

```markdown
| Examiner independence: Phase Gate verdicts are issued by a subagent that receives only the gate task, the objective pass criteria, and the student's verbatim answer/artifact — never the teaching transcript or the coach's opinion — and the coach cannot override an Examiner Fail into a Pass | Examiner question phrasing and which weak point it probes first |
```

- [ ] **Step 2: Add the `## Examiner Gate` section**

Insert a new section in `engine/ENGINE.md` immediately after the `## Phase Gates` section and before `## Tiered Scorecard`:

```markdown
## Examiner Gate

Phase Gates are administered by an Examiner, not by the teaching coach. The coach taught the
material and has a stake in the student passing; an LLM coach drifts toward grade inflation.
The Examiner judges from outside the session so the certification is independent of the
teaching.

**Mechanism.** When a Phase Gate is attempted, the coach dispatches an Examiner subagent in a
fresh context and passes EXACTLY four things: the gate task and objective pass criteria from
the coach's `phase-gates.md` hook, the tier scorecard dimensions, the student's verbatim
answer and any artifact (file contents, command output), and the attempt number. The coach
passes nothing else — never the teaching transcript, never the coach's own assessment, never
the analogies used or hints given. That isolation is what makes the verdict independent.

**Verdict.** The Examiner returns a per-criterion pass/fail with cited reasons, a score
against the tier scorecard (the 60% threshold decides pass/fail), and the honest footer. The
coach records the verdict verbatim. The coach cannot round a score up or convert a Fail into a
Pass. On a Fail the coach runs the existing Phase Gate 3-attempt failure protocol; the
Examiner scores each attempt's answer, the coach owns the ladder between attempts.

**Stance.** The Adversarial Default applies to the Examiner: the student earns the pass, the
Examiner probes the weakest point once and concedes only if it survives.

The full payload contract, verdict format, and the LLM-judge failure modes (hallucinated
pass, arbitrary harshness, criteria starvation) are in `references/examiner-gate.md`.
```

- [ ] **Step 3: Add the pointer in `## Phase Gates`**

In the `## Phase Gates` section of `engine/ENGINE.md`, after the "Scope-based, not timed." paragraph, add:

```markdown
Phase Gate scoring is administered by the Examiner Gate (see `## Examiner Gate`), not by the
teaching coach. The coach still runs the 3-attempt failure protocol below; the Examiner issues
the pass/fail on each attempt.
```

- [ ] **Step 4: Run the linter to verify Task 1's ENGINE.md guards pass**

Run: `cd /home/ubuntu/go_senior_devops/learning-coaches && bash scripts/lint-engine.sh; echo "exit=$?"`
Expected: the `## Examiner Gate` and `Examiner independence lock` MISSING lines are gone. Only `MISSING in engine/PROGRESS-SCHEMA.md: Examiner ledger` may remain (fixed in Task 4). If that is the only remaining failure, this task is correct.

- [ ] **Step 5: Commit**

```bash
git add engine/ENGINE.md
git commit -m "engine: add Examiner Gate mechanic and independence lock"
```

---

## Task 4: Outcome schema (certifier field + Examiner ledger)

**Files:**
- Modify: `engine/PROGRESS-SCHEMA.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the `## 11. Examiner ledger` section (satisfies Task 1's schema guard) and the `certifier` field on scorecard history.

- [ ] **Step 1: Add the `certifier` field to scorecard history (§6)**

In `engine/PROGRESS-SCHEMA.md` section `## 6. Scorecard history`, add a bullet after `best-moment`:

```markdown
- `certifier` — `examiner | coach`. Phase Gate entries are `examiner` (issued by the Examiner
  Gate); formative step-G scores are `coach`. Lets trend tracking separate certified outcomes
  from in-session formative scores.
```

- [ ] **Step 2: Add the `## 11. Examiner ledger` section**

Insert after `## 10. Domain registries` and before `## Example skeleton`:

```markdown
## 11. Examiner ledger

An append-only outcome record, one entry per Examiner Gate verdict. This is the longitudinal
signal that answers "is the student actually getting stronger" independent of the teaching
session. Never overwrite; append.

Each entry:

- `date`
- `phase` — the phase the gate certified.
- `verdict` — `pass | fail`.
- `score` — `n/total` against the tier scorecard at the time.
- `attempt` — which attempt (1-3) produced this verdict.

The ledger is read by the Phase Gate third-attempt diagnosis and by Weekly Review trend
tracking. Unlike per-topic mastery (self-reported, §5), the ledger records only
Examiner-issued outcomes, so a rising mastery level that is not backed by ledger passes is a
calibration flag.
```

- [ ] **Step 3: Update the example skeleton**

In `## Example skeleton`, add an `## Examiner ledger` block after the `## Scorecard history` line and add `certifier` to the scorecard example:

```markdown
## Scorecard history
- 2026-06-27 | step G | 4/6 | name the trade-off before proposing | clear failure-mode walkthrough | coach

## Examiner ledger
- 2026-06-28 | Phase 1 | pass | 5/6 | 2
```

- [ ] **Step 4: Run the full engine linter to verify it now passes**

Run: `cd /home/ubuntu/go_senior_devops/learning-coaches && bash scripts/lint-engine.sh; echo "exit=$?"`
Expected: no MISSING/LEAK lines, `exit=0`.

- [ ] **Step 5: Commit**

```bash
git add engine/PROGRESS-SCHEMA.md
git commit -m "schema: add Examiner ledger and scorecard certifier field"
```

---

## Task 5: Wire terraform-coach Phase Gates to the Examiner

**Files:**
- Modify: `skills/terraform-coach/references/phase-gates.md`

**Interfaces:**
- Consumes: the payload contract from `examiner-gate.md` (Task 2) — names the artifact the coach must pass for each gate.
- Produces: per-gate "Examiner inputs" lines so the coach knows the objective artifact to feed the Examiner.

- [ ] **Step 1: Add an "Examiner inputs" line to each gate**

In `skills/terraform-coach/references/phase-gates.md`, add one line under each gate's pass condition naming the objective artifact the coach passes to the Examiner. Examples for P0 and P1 (add the analogous line to P2-P6 naming each gate's concrete artifact):

P0:
```markdown
**Examiner inputs:** the student's verbatim spoken/written answer to the gate question (no lab artifact for P0).
```

P1:
```markdown
**Examiner inputs:** the student's `.tf` files (fenced), the `terraform plan` output, the `terraform state show aws_instance.<name>` output, and the student's verbatim explanation.
```

P3:
```markdown
**Examiner inputs:** the student's `backend "s3"` block (fenced), and the verbatim answer to the two-engineers-same-second lock question.
```

P5:
```markdown
**Examiner inputs:** the tfsec finding output (fenced), the remediated HCL, and the verbatim drift explanation.
```

(Add P2, P4, P6 lines in the same shape, each naming that gate's concrete checkable artifact.)

- [ ] **Step 2: Verify coach lint still passes**

Run: `cd /home/ubuntu/go_senior_devops/learning-coaches && bash scripts/lint-coach.sh terraform-coach; echo "exit=$?"`
Expected: `exit=0` (no TODO markers reintroduced, structure intact).

- [ ] **Step 3: Commit**

```bash
git add skills/terraform-coach/references/phase-gates.md
git commit -m "terraform-coach: name Examiner inputs per phase gate"
```

---

## Task 6: Behavioral acceptance — dry-run the Examiner independence

This is the real acceptance test: the lint only proves structure exists; this proves the
mechanic behaves. Run it as a one-off, no commit.

**Files:** none (manual/agent-driven verification).

- [ ] **Step 1: Strong-answer case (should PASS)**

Dispatch an Examiner subagent with the P0 gate payload (gate task + criteria from
`terraform-coach/references/phase-gates.md` P0) and a strong student answer that correctly
explains declarative vs imperative and what the state file tracks (identities, metadata,
cross-resource refs, destroy ordering).
Expected: verdict `pass`, each criterion cited, footer present. Confirm the dispatch prompt
contained none of: this conversation, the coach's opinion, any analogy.

- [ ] **Step 2: Weak-answer case (should FAIL)**

Dispatch a second Examiner subagent with the same P0 gate task but a weak answer that says
"the state file is just a cache of the cloud" (the exact misconception P0 criterion 2 targets).
Expected: verdict `fail` on criterion 2 with a cited reason; the Examiner does not wave it
through. This confirms the Adversarial Default reached the subagent.

- [ ] **Step 3: Leak check**

Re-read the two dispatch prompts. Confirm neither contained the teaching transcript, prior
attempts, or the coach's assessment — only the four contracted payload parts.
Expected: both prompts are payload-only. If either leaked, the independence is not real and
Task 3's lock wording needs strengthening before this plan is considered done.

- [ ] **Step 4: Schema round-trip**

Confirm a sample `progress.md` can hold the new fields: a `## Examiner ledger` entry and a
scorecard line ending in `| examiner`, matching the skeleton in `PROGRESS-SCHEMA.md`.
Expected: the example skeleton parses by eye against §6 and §11.

---

## Self-Review

- **Spec coverage:** Examiner-as-independent-subagent → Tasks 2,3,6. Outcome measurability → Task 4 (ledger) + Task 6 step 4. Lint lock so it can't be gutted → Task 1. terraform wiring → Task 5. Honest acknowledgement that independence is structural not cross-model → Global Constraints + examiner-gate.md §1. All covered.
- **Deferred (NOT in this plan):** step-G-every-session Examiner (cost: a subagent every session — revisit after Phase Gate proves out); Weekly Review blind-recall Examiner (Phase 2); a script that mechanically builds the Examiner prompt to remove the coach-leak risk (Phase 2 hardening — noted as the residual fragility); onboarding k8s/sd/leetcode coaches (Phases 3-4).
- **Residual risk:** the coach constructs the Examiner prompt, so leak-prevention is prose-enforced (Task 3 lock + Task 6 step 3 check), not mechanically guaranteed. This is the same prose-constraint fragility flagged in the CEO review; the mechanical prompt-builder is the Phase 2 fix.
