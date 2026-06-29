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
