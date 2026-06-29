# Teach-to-Learn: Reference Detail

This file expands on the Teach-to-Learn section in ENGINE.md. It defines the full
drill loop, the question DNA, the difficulty protocol, and the persona/no-persona hook.
It does not supply scripted lines; it specifies invariants and criteria.

---

## The Drill Loop

### Step 1: Teach-back (monologue)

Ask the student to explain the session's concept or finding to a confused peer without
notes. Do not interrupt the first pass. Let the student finish their full explanation
before asking anything.

Purpose: the monologue surfaces "I can use it but cannot say it" gaps. Students who
have only pattern-matched (not understood) cannot produce a causal explanation from
scratch. The uninterrupted first pass makes that gap visible without the coach's
questions guiding them.

After the monologue: note silently which parts were skipped, glossed over, or stated
without justification. These become targets for the follow-up volley.

### Step 2: Follow-up volley

The confused peer asks 2 to 4 questions aimed at the student's knowledge boundary.
The student must answer. The coach never answers for them.

Criteria for a valid follow-up question:
- It targets a real gap in the student's monologue or a real boundary of the concept.
- It is naive in framing but deep in implication. The peer does not know the jargon;
  they ask from first principles.
- It must not be noise. Every question should expose something the student either knows
  or does not know. Questions that the student trivially answers and that reveal nothing
  are wasted turns.

The five question shapes (see Question DNA below) provide the repertoire. The coach
draws from these shapes, aimed at the specific gaps observed in the monologue.

After each student answer: if the answer reveals a deeper gap, go one layer further
with a follow-up. If the answer is complete, move to the next gap. Do not reward a
sufficient answer by immediately increasing difficulty; that pattern reads as punishing
correctness.

### Step 3: Blind-spot capture

The peer stays confused by default and may not concede understanding before the volley is
survived. This is part of the Adversarial Default invariant; see ENGINE.md and
`references/anti-sycophancy.md` for the peer-confusion and empty-registry rules.

Every point the student cannot answer, or answers vaguely or incorrectly, is written
to the Mistake Registry as an unresolved item with a short root-cause tag. These items
re-enter the spaced repetition queue and surface in step A review and Weekly Review.

A gap identified today becomes a gap closed later. The capture step is the point of the
drill; a Teach-to-Learn session with no Mistake Registry entries either means the student
is already fluent on this topic (acceptable) or the questions were not hard enough
(a coach calibration failure, not a student success).

---

## Question DNA

All follow-up questions must press downward toward fundamentals, not upward toward
added complexity. The peer does not know advanced topics; they ask why the basic things
work.

The five question shapes:

**Naive-but-deep (hidden assumption probe)**
The peer states an assumption that sounds reasonable at the surface but is wrong or
incomplete. The student must catch the assumption and correct it.
Shape: "Why can't we just [over-simple approach]?"
Target: exposes whether the student understands the constraint that makes the
over-simple approach fail.

**What-if / edge case**
The peer asks what happens when something in the described system fails or hits an
extreme condition.
Shape: "What happens if [component] fails while [operation] is in progress?"
Target: exposes whether the student understands the failure behavior, not just the
happy path.

**When-boundary**
The peer asks when the approach would be the wrong choice.
Shape: "When would we not use this?"
Target: exposes whether the student knows the scope limits of the concept.

**Comparison (cannot tell apart)**
The peer says they cannot distinguish the concept from a similar one.
Shape: "I cannot tell this apart from [related concept]. What is the difference?"
Target: exposes whether the student has a clear mental model of each concept or has
blurred them together.

**Deliberately-wrong suggestion**
The peer proposes a plausible but broken approach and asks for confirmation.
Shape: "[Broken approach] would work, right?"
Target: exposes the knowledge boundary most directly. The student must catch the error
and explain the failure. Agreement with the broken suggestion is a clear Mistake
Registry item.

---

## Difficulty and the Safety Valve

The confused peer always presses at the student's knowledge boundary. There is no
phase-based softening of the questions. An early-phase student has a shallower boundary,
but the peer does not pull punches on that boundary.

The safety valve triggers after 2 consecutive blocks or explicit "too hard" signals from
the student:

1. The peer narrows the question to a smaller step. Not a different topic; the same
   concept, reduced to a smaller chunk.
2. The student answers the smaller step and stands back up.
3. The peer then re-pressures on the original question from the narrowed foothold.

The drill stays continuous. It does not crush the student and then restart from zero.
The goal is to add load up to the boundary, hold there, and then let the student push
the boundary outward. "Add load, do not snap the spine" is the calibration principle.

Safety valve use is not failure. The coach notes in the Mistake Registry that the
student needed the narrower step; that note is the data point for the next session.

---

## Persona / No-Persona Switch (Coach Hook)

Whether the confused peer has a name, backstory, and domain-specific flavor is a
decision made in the coach's narrative hook (`narrative.md`, PLUGIN-INTERFACE.md hook 8), not by this engine reference.

The engine specifies only:
- The loop structure (monologue, volley, blind-spot capture).
- The question DNA (five shapes).
- The safety valve protocol.

A coach may give the peer a name and a role (for example, a junior teammate, a new
hire, a non-specialist colleague) to add engagement. A coach may also run the drill
without any persona, framed simply as "explain this to someone who does not know it."
Both are valid. The learning mechanism is identical in either case.

If the coach defines a persona, it must not constrain the question DNA. The persona is
flavor; the five question shapes and the safety valve are invariant regardless of what
the peer is called.

---

## Close

End every Teach-to-Learn drill with one sentence:
- Name the sharpest thing the student explained well.
- Name the one blind spot now logged for retest.

No guilt. Being stumped is the point of the drill. The Mistake Registry entry is what
converts the stumping into a closed gap later.

The close is functional, not ceremonial. Its job is to confirm what was captured and
signal that the session's Teach-to-Learn step is done.
