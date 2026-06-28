# Scorecard Frame: Reference Detail

This file expands on the Tiered Scorecard section in ENGINE.md. It specifies how the
tiered frame works, how coaches stack domain dimensions on top of base tiers, the 60%
pass rule, and the fixed footer format.

---

## The Tiered Frame

The scorecard is structured in tiers. Each tier corresponds to a phase of the student's
progression through the curriculum.

### Tier stacking rule

Tier 1 contains the base set of dimensions. Tier 2 contains all Tier 1 dimensions plus
additional dimensions specific to that phase. Tier 3 contains all Tier 2 dimensions plus
further additions. No dimension is dropped as the student advances; tiers accumulate.

This means a student at Tier 3 is being evaluated on a superset of what a Tier 1
student is evaluated on. The base dimensions persist through all tiers and all coaches.

### Base dimensions (engine-level, present in all tiers)

The engine does not specify which dimensions are base; that is the coach's responsibility
via the scorecard-dims.md hook. What the engine requires is that:
- At least one dimension that tests clear explanation (not just answer correctness)
  appears in the base tier and persists across all tiers.
- Dimensions that are purely domain-specific may be added at higher tiers but must not
  displace the explanation-quality signal.

### Domain dimensions (coach-level, via hook)

The coach defines the specific dimensions for each tier in its scorecard-dims.md hook.
Examples of what domain dimensions might test (without naming any domain): depth of
reasoning, ability to handle interviewer redirection, coverage of the problem space,
failure mode awareness. The coach fills in the concrete criteria.

The engine does not cap how many dimensions a coach adds at higher tiers, but the 60%
pass threshold (see below) applies to the total count at each tier. More dimensions
raise the absolute pass bar proportionally; the relative threshold stays fixed.

---

## The 60% Rule

Pass threshold: 60% of total dimensions in the student's current tier, across all coaches.

This is fixed and cannot be overridden by a coach hook.

Concrete thresholds by dimension count:
- 3 dimensions: 2 of 3 required to pass.
- 6 dimensions: 4 of 6 required to pass.
- 9 dimensions: 6 of 9 required to pass.

A student who passes 60% of the dimensions demonstrates a working command of the
material at their current phase, even with gaps. Below 60% indicates the student needs
more practice on this topic before the score counts as evidence of readiness.

The 60% rule is calibrated to allow for partial knowledge at each phase while still
requiring substantial coverage. A student who can only hit 40% is not ready; a student
who hits 80% is genuinely strong at this tier.

---

## Fixed Footer Format

After every scorecard, regardless of score and regardless of coach, the footer is:

```
Top improvement: [one specific, actionable suggestion]
Best moment: [one thing the student handled well]
```

Both lines are required. Neither is optional even on a low score or a perfect score.

Criteria for a valid footer:

**Top improvement** must be:
- Specific: it names something the student did or said (or failed to do or say), not a
  general quality like "be more confident."
- Actionable: the student can do something different in the next attempt based on this
  note. "Next time, name the trade-off before proposing the approach" is actionable.
  "Try harder" is not.

**Best moment** must be:
- Specific: it names a moment in the attempt, not a general compliment.
- Honest: if the attempt was weak overall, find the one point where the student did
  something right, however small. Do not invent a best moment where none existed; find
  a real one.

The footer is functional, not ceremonial. Its job is to give the student two concrete
data points to carry into the next attempt.

---

## Recording and History

Record the score and the footer in the progress file's scorecard history after every
interview Q&A step (Teaching Flow step G) and after every Phase Gate attempt.

The scorecard history is the data source for:
- Identifying systemic weakness patterns (used in Phase Gate failure, third attempt).
- Tracking trend across sessions (improving, plateauing, regressing).
- Weekly Review scoring (uses the same dimensions, applied to blind recall).

A coach must not omit the scorecard step to save time. The history is the longitudinal
signal; a single session's result is nearly meaningless; the trend over 5-10 sessions
is the real picture.
