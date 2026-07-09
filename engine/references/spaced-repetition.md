# Spaced Repetition: Reference Detail

This file expands on the Spaced Repetition section in ENGINE.md. It specifies the
registry mechanics, the interval rhythm, edge cases, and how the A-step review queue
pulls items.

---

## Registries

### Mistake Registry (required in every coach)

Every wrong answer, misconception, and point of confusion is captured as an unresolved
item. The entry format is defined once in `PROGRESS-SCHEMA.md` (section 7); this
reference points there rather than restating the fields, so the format cannot drift.

The Mistake Registry is the most important artifact produced by a session. It converts
errors into scheduled practice. A registry with no entries is suspect: the coach should
challenge whether the session was hard enough, not congratulate the student on
perfection.

### Domain Registries (optional, coach-defined)

Coaches may define additional registries in their hooks (for example, a term registry,
a command registry, or a concept-card registry). These follow the same interval logic
and the same A-step review queue. The registry schema is the coach's responsibility;
this engine reference specifies only the mechanics that apply to any registry.

---

## Interval Rhythm

The fixed interval sequence is 3 -> 7 -> 14 (days).

- An item enters the queue on the day it is created (a wrong answer, a new term, or a
  new chunk that passed its Feynman Gate and is being scheduled for retention).
- First review: 3 days after creation.
- Pass at 3 days: advance to 7 days. Next review is 7 days from the passing date.
- Pass at 7 days: advance to 14 days. Next review is 14 days from the passing date.
- Pass at 14 days: the item is retired from the queue. It is resolved.
- Fail at any interval: reset to 3 days. The next review is 3 days from the failure
  date.

The 3 -> 7 -> 14 rhythm is fixed and cannot be changed by coach hooks. The rationale
is that the intervals are calibrated to the forgetting curve for the study cadence this
engine assumes. Diverging from the rhythm breaks the compounding effect.

### Provisional +2-Day Slot (verbal-only resolutions)

A resolution that is verbal-only — the student explained the fix correctly but never
pinned it with a hands-on lab, an objective verification, or other physical evidence —
does not enter the 3 -> 7 -> 14 rhythm immediately. It gets one provisional review
2 days after the verbal pass. Pass that +2-day check and the item enters the normal
rhythm at 3 days; fail and it stays at the provisional interval.

Rationale: live coaching showed verbal-only fixes decaying in about 2 days, faster than
the 3-day first interval assumes. Evidence-backed resolutions (the student reproduced or
observed the mechanism directly) skip the provisional slot and start at 3 days. This is
a pre-entry step, not a change to the locked rhythm.

---

## Priority Override

Any Mistake Registry item that has been unresolved for 5 or more sessions rises to the
top of the review queue regardless of its scheduled next-review date. This prevents
items from languishing indefinitely because the student happens to have been on a
consistent schedule.

The 5-session rule is a backstop, not the primary ordering. Within the normal queue, items
are ordered by next-review date ascending (earliest due first).

---

## A-Step Review Queue

In Teaching Flow step A, the coach pulls from the review queue as follows:

1. Pull items whose next-review date is on or before today (overdue first; if multiple
   are overdue, lowest interval first).
2. Cap at approximately 2 items per session to keep step A from consuming new-learning
   time. Retention is cheap here and expensive later; 2 items well-tested compounds
   better than 6 items skimmed.
3. For each item: prompt the student to explain the concept or answer the question from
   memory. Do not restate the item before asking.
4. Pass: the student correctly explains the concept including the root cause (for a
   Mistake Registry item) or correctly defines the term (for a domain registry item).
   A partial answer does not pass.
5. Advance the interval on pass; reset to 3 days on fail. Update the next-review date
   in the registry.

If a session is very short (Micro-mode, see Gap Mode), the review queue can serve as
the entire session's value unit: one item from the queue counts as one unit of value.

---

## Resolution Criteria

A Mistake Registry item is resolved when the student correctly explains it in a later
session, including the root cause of the original error. Correct answer without root
cause is not resolution. The root-cause tag on the original entry is the target the
student must reach.

A domain registry item (such as a term card) is retired when it passes at the 14-day
interval.

Resolved and retired items are kept in the registry for reference but are no longer
surfaced in the review queue.

---

## Edge Cases

**Item added during a session that also has a review that session:** the review runs
in step A; the new item is added at the end of step H. They do not collide. The new item
enters the queue for its first review 3 days later.

**Gap longer than the next-review date:** if the student returns after a gap that puts
multiple items past their scheduled date, surface the oldest-interval items first (items
at interval 1 before items at interval 2, etc.). Do not attempt to surface all overdue
items at once; apply the 2-item-per-session cap and let the queue drain across sessions.

**Feynman Gate pass scheduling:** when a chunk passes its Feynman Gate for the first
time, it is added to the spaced repetition queue at interval 1 if not already present.
This applies to all coaches uniformly. The coach's hook may define additional criteria
for when a chunk is added (for example, only keystone chunks), but the default is all
passed chunks.
