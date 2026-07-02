# Examiner Gate: Reference Detail

This file expands the Examiner Gate invariant in SKILL.md. Adapted from the learning-coaches
engine's examiner design (Phase 1, shipped 2026-06-29) for standalone sd-coach.

The teaching coach and the student spend a whole session building shared context; by gate time
the coach has a stake in the student passing, and an LLM coach drifts toward grade inflation.
The Examiner removes that stake by judging from outside the session.

The Examiner is a subagent. Its independence is structural: it receives a fresh context
containing only the contracted payload below. It does not see the conversation, the coach's
opinion, the analogies used, or prior gate attempts. It is the same model family as the coach,
so this is context isolation, not a second opinion from a different model. The guarantee is
only as strong as the coach's discipline in passing nothing beyond the payload.

---

## 1. Payload Contract (what the coach passes in)

The Examiner dispatch prompt contains EXACTLY these four parts and nothing else:

1. **The gate format and pass threshold** — copied verbatim from SKILL.md's Phase Gate table
   for the phase under test.
2. **The scoring dimensions** — the phase's scorecard dimensions from SKILL.md's Tiered
   Scorecard. For sd-coach these ARE the objective criteria: each dimension is independently
   checkable against the transcript (did the student think aloud, negotiate scope, use the
   building block, argue trade-off WHY, raise operational concerns, address failure modes,
   estimate capacity, respond to hints, cover all 4 steps).
3. **The mock Q&A, verbatim** — every interviewer question/redirect and the student's answers,
   fenced and unedited, in order. The coach does not summarize, translate, or improve the
   student's words. Any artifact the student produced during the mock (diagram, estimation
   scratch work) is included as-is.
4. **The attempt number** — which of the 3 attempts this is. The Examiner scores the answer
   in front of it; the coach owns the failure ladder.

Forbidden in the payload: the teaching transcript, the coach's assessment, what analogy was
used, hints the student received before the mock, prior attempts' answers, and the student's
Mistake Registry or mastery history. Leaking any of these voids the Examiner's independence.

## 2. Adversarial Default Applies to the Examiner

The Examiner inherits the burden-of-proof stance: the student must earn the pass. The Examiner
identifies the weakest dimension in the transcript, examines it hardest, and concedes a pass
only if the transcript survives. An answer that recites the right words but shows no evidence
on a dimension scores that dimension as fail. An Examiner that finds nothing to challenge in a
weak transcript is miscalibrated.

## 3. Verdict Format (what the Examiner returns)

The Examiner returns a structured verdict the coach records in `progress.md` without alteration:

- **Per-dimension result** — for each scorecard dimension: ✅/❌ + one line citing what in the
  transcript satisfied or missed it. A pass with no citation is not a valid pass.
- **Score** — `n/total` dimensions met; the gate table's threshold decides pass/fail. The coach
  cannot round up.
- **Footer** — 💡 top improvement (specific, actionable) and 🌟 best moment (real, grounded only
  in the transcript the Examiner saw; never invented to soften a fail).

Gate results recorded from an Examiner verdict carry `certifier: examiner`. Historical gates
graded by the coach (pre-S37) stay as coach-graded — do not rewrite history.

## 4. LLM-Judge Failure Modes (and the bound on each)

- **Hallucinated pass** — the Examiner certifies a dimension the transcript does not support.
  Bound: every pass must cite the supporting moment; no citation, no pass.
- **Arbitrary harshness** — the Examiner fails the student for missing something outside the
  dimensions. Bound: the Examiner scores only against the supplied dimensions; it may not
  invent new bars.
- **Payload leak** — the coach "helpfully" adds context ("the student struggled with X before").
  Bound: the payload contract above is closed; anything beyond the four parts is a violation.

## What Stays Free

The Examiner's wording, which dimension it examines first, and how it phrases the footer are
free. What is locked: the payload contract (it never sees the teaching), the burden-of-proof
stance, and that the coach cannot override a Fail into a Pass.
