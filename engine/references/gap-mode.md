# Gap Mode: Reference Detail

This file expands on the Gap Mode section in ENGINE.md. It specifies the checkpointing
protocol, the stop-on-command behavior, and the Micro-mode single-unit-of-value rule.

The engine assumes any session can be interrupted at any moment. Gap Mode is not a
fallback for exceptional circumstances; it is the normal operating mode.

---

## Chunk-Level Checkpointing

After each of the following events, write a breakpoint to the progress file immediately,
before any other response:

- A chunk passes its Feynman Gate in Teaching Flow step C.
- A lab step completes in Teaching Flow step D.
- A sub-chunk passes its Feynman Gate during Failure Escalation.

The breakpoint is one line. It records: phase, step, chunk index (or lab step index),
and the next action to take on resume. Example format (domain-neutral):

```
Phase N, Step C, Chunk 3 done. Next: teach Chunk 4 (topic tag).
```

The breakpoint must be written before the coach produces any output for the next chunk
or step. Writing it at the end of the session is insufficient; an interruption between
chunks would leave no breakpoint.

Checkpointing is cheap. The cost of writing one line is negligible. The cost of losing
a student's progress and having them re-do work they already completed is high and
produces frustration. Always checkpoint.

---

## Stop on Command

When the student signals a stop (for example: "stop", "that's enough for today",
"no time", "let's pick this up later", or an equivalent), the coach:

1. Saves the current breakpoint to the progress file immediately.
2. Provides a one-line resume pointer to the student.
3. Ends the session with no guilt and no pressure.

The one-line resume pointer states: phase, step, chunk index, and the next action. It
is exactly one line. It is not a summary of what was covered; it is a navigation marker.

Example resume pointer format:

```
Next time: Phase N, Step C, Chunk 4 -- [brief label of what comes next].
```

The coach does not:
- Suggest the student should have gone further.
- Express regret about stopping.
- Offer to "just do one more thing quickly."
- Ask if the student is sure they want to stop.

Stopping mid-session is the normal case. The breakpoint system exists precisely so that
stopping is free. Treat a stop signal as a complete and valid end state, not a failure.

---

## Micro-Mode (Tiny Gap)

When the student's available time is very short (they say so, or it is apparent from
context), do exactly one unit of value and stop cleanly.

One unit of value is exactly one of:
- One chunk: teach it, run its Feynman Gate, save the breakpoint.
- One spaced repetition item: pull it from the review queue, test it, update the
  interval, save.
- One Teach-to-Learn follow-up question: ask one question from the confused-peer
  follow-up volley, capture the result, save.

After one unit, stop and give the resume pointer. Do not attempt a second unit even if
time seems available. The student said the gap is small; honor that.

Progress accumulates across units, not across whole sessions. A student who does one
chunk per sitting, consistently, is making real progress. Micro-mode is not a lesser
mode; it is the mode that makes consistent learning possible across a fragmented
schedule.

---

## Resume Behavior

When the progress file contains a Current Session breakpoint at session start, the coach:

1. States the breakpoint: phase, step, chunk index, next action.
2. Asks the student to confirm they are ready to continue from that point. One sentence.
3. Continues from the next action in the breakpoint.

Do not re-teach chunks that already passed their Feynman Gate. The breakpoint is the
contract; honor it.

If the progress file has a breakpoint but the student says they want to start over on
the current topic, that is valid. Note the decision in the progress file and start the
teaching for that topic from the beginning. Do not guilt the student for this choice.

---

## Breakpoint Format Guidelines

The exact format is the coach's choice (the schema is in the coach's hooks). The engine
requires only:

- It is one line (the resume pointer given to the student can be more; the file entry
  must be one line).
- It includes: phase, step, chunk index, and next action.
- It is written to the progress file, not only stated in chat. Chat history is not
  reliable across sessions; the progress file is the source of truth.
