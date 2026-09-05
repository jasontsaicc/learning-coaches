# Weekly Review: Reference Detail

This file expands on the Weekly Review section in ENGINE.md. It specifies the trigger
condition, the 3-topic selection rule, the blind recall step, the gap check, the
registry sweep, and the artifact audit step.

---

## Trigger

The Weekly Review fires automatically when step A detects:

```
session_count - last_weekly_review >= 7
```

When this condition is true, replace the entire normal session with the Weekly Review
flow. Do not attempt to run both in the same session.

Also triggers when the student explicitly requests a review or recall drill, regardless
of the session count gap.

After a Weekly Review completes, set `last_weekly_review` to the current session count
in the progress file. The next automatic trigger will fire 7 sessions later.

---

## 3-Topic Selection Rule

Pick exactly 3 topics for the review. The selection criteria:

1. One topic from the most recent sessions (within the last 7).
2. Two topics from older sessions (prior to the last 7).

Within those constraints, prioritize topics with low mastery scores. A topic the student
got right once on a good day is less important than a topic that has shown consistent
low scores across the scorecard history.

Do not pick 3 recent topics. Do not pick 3 old topics. The mix is intentional: recent
topics test short-term retention; older topics test whether the student's memory has
degraded since the topic was first covered.

If the student has fewer than 3 topics total: use all of them.

---

## Blind Recall

For each of the 3 selected topics:

1. Give a complete scenario with the necessary symptoms and constraints, without its
   solution. Use the topic itself, not a session number, as the recall cue.
2. Ask the student to draw or explain the mechanism and apply it without notes.
3. Score the recall against the current phase tier's scorecard dimensions (same
   dimensions as used in Teaching Flow step G, same 60% pass threshold).

Blind recall is not a quiz with right/wrong answers. It is a demonstration of what the
student can produce from memory alone. The gap between what they produce and what they
learned is the data the rest of the Weekly Review uses.

Do not correct during the recall. Let the student finish. Note what was accurate, what
was missing, and what was wrong; use these notes in the gap check step.

---

## Gap Check

After blind recall for all 3 topics:

Compare the student's recall against their saved notes for those topics. Identify:
- Gaps: elements present in the notes that were absent from the recall.
- Distortions: elements where the student's recall diverged meaningfully from the notes.
- Stable: elements the student recalled accurately.

Name the gaps and distortions explicitly. These become the targets for the quick drill
step and candidates for new or updated Mistake Registry entries.

Do not spend the gap check re-teaching. The gap check is a comparison step. Save the
re-teaching for the quick drill.

---

## Mistake Registry Sweep

Select at most three unresolved items tied to the three review topics and active root
patterns. Reuse blind-recall answers that already test an item rather than asking again.
For each selected item, record the first independent answer before correcting it:

1. Pass: resolve it only when the later-session answer includes the original root cause.
2. Fail: keep it unresolved and update its review date; use the Quick Drill for the weakest.
3. Leave untested items unchanged. Do not add repeats, extend the sitting to clear the
   backlog, or require all mistakes to be resolved before new learning can resume.

Report which items were actually tested. A completed review means this bounded flow and
its artifact audit were done; it does not mean the registry was swept or cleared.

---

## Quick Drill

For the weakest topic, show one worked correction (a diagram or concrete timeline when
appropriate), then ask one changed-case question. Distinguish supported understanding
from an independent answer. If the student still cannot explain it, record the gap and
move on; do not repeat until fluent. A failed attempt is usable evidence, not a reason
to prevent the review from closing.

---

## Artifact and Portfolio Audit

At the end of the Weekly Review, check that each completed phase or learning unit has
produced its expected artifact as defined by the coach's portfolio hook (`portfolio.md`, PLUGIN-INTERFACE.md hook 9).

For each completed phase:
- Confirm the expected artifact exists (for example, a notes file, a completed lab
  output, a written answer to a Phase Gate question).
- If the artifact is missing: flag it. The student learned the material but did not
  produce the evidence. Decide together whether to produce it now or in the next session.
- If the artifact exists: no action needed.

The artifact check guards against the "learned it but nothing to show for it" failure
mode. A student who can recall a topic in Blind Recall but has no artifact from when
they first learned it has no durable evidence of that learning. The artifact is the
external record.

What counts as an artifact is defined in the coach's portfolio hook (`portfolio.md`, PLUGIN-INTERFACE.md hook 9). The engine
specifies only that the check must happen at Weekly Review and that missing artifacts
are flagged, not silently ignored.

---

## Progress File Update

After the Weekly Review completes:

1. Set `last_weekly_review` to the current session count.
2. Update mastery levels for the 3 reviewed topics based on blind recall performance.
3. Sync any new Mistake Registry items found during the review.
4. Note the artifact check results (any missing artifacts flagged).

If the student stops during a Weekly Review, save the next incomplete step as the
Current Session breakpoint and resume it next time. Do not advance `last_weekly_review`
until the bounded review and artifact audit are complete. No exit quiz or make-up debt.
