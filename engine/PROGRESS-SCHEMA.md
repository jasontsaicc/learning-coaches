# Progress File Schema

The progress file is the single source of truth for a student's state across sessions.
Every engine mechanic (Routing, Gap Mode breakpoints, Spaced Repetition, Weekly Review,
Phase Gates, scorecard history) reads or writes it. This schema is engine-owned and
shared by every coach. A coach must not redefine these fields; it supplies only the
workspace path (via its portfolio hook) and any optional domain registries, which reuse
the registry format defined here.

This is a prose contract, not a parsed format. The model maintains the file as markdown.
The schema fixes the field set and the entry formats so that every coach serializes the
same way and the engine can resume any student from any coach.

---

## 1. Location

The file is named `progress.md` and lives in the workspace directory named by the coach's
portfolio hook (`portfolio.md`, PLUGIN-INTERFACE.md hook 9). The engine does not hardcode
the path; the path is the coach's only progress-file responsibility.

---

## 2. Meta

A short header block:

- `session_count` — integer; incremented once per completed session (Teaching Flow step H).
- `last_weekly_review` — the `session_count` value at which the last Weekly Review ran.
  Drives the automatic trigger `session_count - last_weekly_review >= 7`.
- `last_session_date` — ISO date (YYYY-MM-DD) of the last session. Drives the Comeback
  Protocol gap check (>= 7 days).
- `warm_up_classification` — the new-student level recorded by Routing branch 1
  (the coach's curriculum hook defines the levels, e.g. new / mid / strong).

---

## 3. Current Session breakpoint

Exactly one line, written immediately after each chunk or lab step passes, and cleared on
normal session completion (step H). Format:

```
phase, step, chunk-index (or lab-step index), next-action
```

This matches the breakpoint format in `references/gap-mode.md`. If absent, the student is
either new or finished the last session cleanly (see Routing branches).

---

## 4. Phase status

Per phase in the coach's curriculum:

- `status` — one of `not-started | in-progress | gate-passed | gate-flagged`.
- `weak-topic flags` — topics flagged for revisit when the student chose to advance after
  a third failed Phase Gate attempt (ENGINE.md Phase Gates, failure protocol).

---

## 5. Per-topic mastery

Per topic covered:

- `level` — one of `low | med | high`.
- `last-updated` — the `session_count` or date the level last changed.

Updated in step H and during Weekly Review blind recall.

---

## 6. Scorecard history

An append-only list. One entry per Interview Q&A (step G) and per Phase Gate attempt:

- `date`
- `context` — `step G` or `phase gate (phase N, attempt K)`.
- `score` — `n/total` (the 60% threshold applies to the current tier's total).
- `top-improvement` — the footer's actionable suggestion.
- `best-moment` — the footer's real positive moment.
- `certifier` — `examiner | coach`. Phase Gate entries are `examiner` (issued by the Examiner
  Gate); formative step-G scores are `coach`. Lets trend tracking separate certified outcomes
  from in-session formative scores.

The history is the longitudinal signal used by the Phase Gate third-attempt diagnosis and
by trend tracking. Never overwrite past entries; append.

---

## 7. Mistake Registry (canonical entry)

This is the canonical entry format. ENGINE.md and `references/spaced-repetition.md` point
here rather than restating it. Each entry:

- `date` — when the item was created.
- `topic`
- `what-was-wrong` — the specific error or misconception.
- `root-cause-tag` — short tag naming the underlying gap; this is the target the student
  must reach to resolve the item.
- `status` — `unresolved | resolved`.
- `interval` — current spaced-repetition interval in days: `3 | 7 | 14`.
- `next-review-date` — ISO date the item is next due in step A.
- `unresolved-session-count` — how many sessions the item has been unresolved; at `>= 5`
  the item jumps to the top of the review queue regardless of `next-review-date`
  (Priority Override).

Resolution requires a correct explanation including the root cause; a partial answer does
not resolve the item.

---

## 8. Spaced-repetition queue

The queue is the ordered review view, not separate storage. Each queued item:

- `item-ref` — reference to the source entry (a Mistake Registry item or a domain
  registry item).
- `type` — `mistake | term | chunk`.
- `interval` — `3 | 7 | 14`.
- `next-review-date`
- `status` — `active | retired`.

A Mistake Registry item carries its own interval and next-review-date in section 7, so it
is not duplicated here; the queue references it. The interval rhythm (`3 -> 7 -> 14`) is
fixed by the engine and is identical for every queued type.

---

## 9. Curiosity branch

Threads parked by the Depth Ceiling's Three Questions, kept so they can be pulled back
later without costing current session time. Each parked thread:

- `topic`
- `date-parked`
- `Three-Questions-result` — which question(s) triggered the park.
- `one-line-note` — what the student wanted to chase, in one line.

---

## 10. Domain registries (coach extension point)

A coach may declare additional registries in its portfolio hook (for example, a term
registry or a command registry). They live in their own sections of the progress file (or
sibling files named by the coach) and reuse the section-7 fields: `interval`,
`next-review-date`, `status`, plus whatever domain payload the item needs (e.g. a term and
its definition). The engine treats them with the same A-step queue and `3 -> 7 -> 14`
rhythm as the Mistake Registry. The schema reserves the extension point; the coach names
the registry and its payload.

---

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

---

## Example skeleton

Every coach serializes to the same shape. A minimal `progress.md`:

```markdown
# progress

## Meta
- session_count: 4
- last_weekly_review: 0
- last_session_date: 2026-06-29
- warm_up_classification: mid

## Current Session breakpoint
(none -- last session completed)

## Phase status
- Phase 0: gate-passed
- Phase 1: in-progress

## Mastery
- topic-a: high (s4)
- topic-b: low (s3)

## Scorecard history
- 2026-06-27 | step G | 4/6 | name the trade-off before proposing | clear failure-mode walkthrough | coach

## Examiner ledger
- 2026-06-28 | Phase 1 | pass | 5/6 | 2

## Mistake Registry
- 2026-06-27 | topic-b | conflated X with Y | missing-boundary-condition | unresolved | 3 | 2026-06-30 | 1

## Spaced-repetition queue
- mistake:topic-b | mistake | 3 | 2026-06-30 | active

## Curiosity branch
- topic-c internals | 2026-06-27 | Q1 no (won't appear in target) | wanted the proof, parked

## Domain registries
(coach-defined; e.g. term registry)
```
