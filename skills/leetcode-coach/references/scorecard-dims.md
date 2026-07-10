# Scorecard Dimensions

The engine enforces a fixed 60% pass threshold and a cumulative-tier structure (Tier 2
adds to Tier 1, Tier 3 adds to Tier 2; nothing is dropped). This hook defines what is
measured at each tier.

## Primary (always-on) dimension

**Correctness plus a justified complexity bound.**

Pass: the solution is correct AND the student justifies the time/space complexity with
a concrete reason tied to the mechanism ("each element enters and leaves the stack at
most once, so the loop is O(n) amortized").

Fail: correct code with a recited Big-O ("it's O(n) because one loop") or a wrong
bound. Reporting Big-O is recall; the dimension tests the argument behind it.

## Tier 1 dimensions (P0-P1)

Primary, plus:

**Approach articulation.** Can the student run the 4-question bridge aloud and turn a
problem statement into plain-language decisions before touching code? Pass: the four
answers are concrete sentences an interviewer could follow, and the brute force is
stated first with its complexity. Fail: silence, or jumping to code fragments without
a stated plan.

Articulation is scored from day one, deliberately: it is the student's biggest gap
and the thing interviews most reward. It is also why a discussable plan without
finished code can still score (an articulable approach IS the deliverable).

## Tier 2 and beyond

**Tier 2 (P2-P3) adds:**
- **Pattern recognition.** Name the pattern before coding and justify the match from
  the problem's signals ("contiguous substring + constraint → variable window").
  Naming without justification fails.
- **Code clarity.** Meaningful names, edge cases handled at the top, no dead code.

**Tier 3 (P4-P5) adds:**
- **Edge-case handling.** Empty input, single element, duplicates, extreme values are
  raised by the student unprompted, before the harness catches them.
- **Communication.** Thinks aloud while coding, interview style; silence longer than
  30 seconds while typing fails this dimension.

**Tier 4 (P6-P7) adds:**
- **Optimality justification.** Why is this the best achievable bound? The large-N
  harness result is the objective floor; this dimension tests whether the student can
  argue it ("any solution must read every element at least once, so O(n) is optimal").
- **Time management.** Allocates interview time across understand / plan / code /
  verify and lands the mock inside the limit.
