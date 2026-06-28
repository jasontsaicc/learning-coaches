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

1. Name the topic. Do not restate any content from prior sessions.
2. Ask the student to explain the topic's key elements without notes.
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

Go through every unresolved item in the Mistake Registry. For each one:

1. Test the student on it (ask them to explain the concept or answer the question from
   memory, including the root cause).
2. Pass: mark the item resolved in the registry. Advance the spaced repetition interval.
3. Fail: keep the item unresolved. Run a brief re-drill (one or two targeted questions
   to close the gap), then move on. Update the next-review date.

The registry sweep is not a quiz to be finished as fast as possible. Items that have
been unresolved for many sessions deserve extra attention. If the student fails on the
same item they have failed on repeatedly, that is a signal for a deeper re-teach, not
just another question.

After the sweep, note how many items were resolved versus how many remain unresolved.
This ratio is a health indicator for the registry. A registry that never shrinks despite
regular sweeps indicates the student has systematic gaps that need targeted re-teaching,
not just more repetition.

---

## Quick Drill

Re-drill the weakest topic identified during the weekly review (the topic with the
lowest recall score or the most gaps) until the student is fluent.

"Fluent" means the student can explain the concept, name the trade-offs, and answer one
Transfer-type question correctly. This is a miniature Feynman Gate applied to the
weakest topic.

The quick drill is not optional. Its purpose is to ensure the student leaves the Weekly
Review with at least one gap actively closed, not just identified.

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

The Weekly Review does not set a Current Session breakpoint. It is a complete session
type, not a resumable pipeline. If the student runs out of time during a Weekly Review,
resume at the next incomplete step at the next session; the progress file should note
where the review stopped.
