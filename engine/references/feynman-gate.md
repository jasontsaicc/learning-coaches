# Feynman Gate: Reference Detail

This file expands on the Feynman Gate section in ENGINE.md. It defines the two-stage
protocol in full and provides a bank of question-type templates for each stage. The
specific questions used in any session are the model's choice; this bank supplies the
shapes, not the scripts.

---

## Two-Stage Protocol

### Stage 1: Recall

Prompt: ask the student to explain the concept in their own words without referring to
notes or the coach's prior explanation. Do not rephrase or paraphrase the concept first;
let the student work from memory.

Pass criterion: the student captures the essential mechanism or idea. Wording does not
need to be precise. The test is whether they can reproduce the core idea, not whether
they have memorized the coach's exact formulation.

Fail signals:
- The student recites words but cannot connect them into a causal chain.
- The student asks "is this right?" instead of committing to an explanation.
- The explanation is circular ("X does X things").

Do not correct on the first attempt. Ask "can you say more about that?" or "what makes
that work?" to let the student extend their own answer before the coach intervenes.

### Stage 2: Transfer

Prompt: ask a question that requires the student to apply, extend, or stress-test the
concept. Recall verifies retention; Transfer verifies understanding. A student who passed
Recall but cannot answer a Transfer question has memorized the surface, not the model.

Pass criterion: the student demonstrates understanding beyond recitation. They can handle
a novel angle on the same concept.

Both stages must pass before a chunk is marked done. A Recall pass alone is not a save
point.

---

## Transfer Question-Type Bank

These are templates, not scripts. The coach fills in the domain-specific concept or
component name. Every question shape below has a corresponding intent; use the intent
to generate variants when the template does not quite fit the current chunk.

### Compare

Template: "How is [X] different from [Y], and when would you prefer one over the other?"

Intent: force the student to distinguish two things that look similar on the surface and
articulate the trade-off that makes each choice meaningful. The student should be able
to name at least one condition under which each option wins.

Variant: "What does [X] give you that [Y] does not? What do you give up?"

### Scenario

Template: "Describe a real situation where [X] would be the wrong choice. What breaks?"

Intent: probe whether the student knows the boundary conditions of the concept. Knowing
when something works is incomplete; knowing when it fails is what separates understanding
from pattern-matching.

Variant: "Under what load, failure mode, or constraint would you stop relying on [X]?"

### Counter

Template: "What fails if you remove [component] from the system?"

Intent: test whether the student understands the function a component serves, not just
its name. Removing it should reveal the mechanism it provides.

Variant: "If [X] did not exist, what problem would immediately appear and why?"

### When-Boundary

Template: "When would you NOT use [X]? Give a concrete condition."

Intent: the student who only knows when to use something is half-prepared. The
when-boundary question surfaces the scope limit of the concept.

Variant: "What assumption does [X] make about the environment? When is that assumption
false?"

### Deliberate-Wrong-Bait

This shape is part of the Adversarial Default invariant; the full bait-construction and
scoring rules are in `references/anti-sycophancy.md`.

Template: "[Plausible but broken approach]... that would work, right?"

Intent: the student must catch the error and explain why it fails. This tests the
knowledge boundary most directly: a student who agrees with a wrong premise has a gap
they have not noticed. A student who catches the error and explains the failure mode
has internalized the concept.

Rules for constructing a bait:
- The bait must sound plausible to a student who half-understands the topic.
- The error must connect to a real mechanism the student just learned, not a trivial
  mistake.
- If the student agrees with the bait, treat it as a Fail on Transfer and note it in
  the Mistake Registry. Do not reveal the error immediately; ask "walk me through why
  that would work" to let the student find the contradiction.

---

## Objective Verification Hook

For chunks where a domain command or tool can verify the concept objectively, the coach
may include the verification result as evidence for Stage 2 Transfer. The form is:

1. The student predicts the outcome before running the command or tool.
2. The student runs the coach-supplied domain command (a test runner, validator,
   observer, or diagnostic tool defined in the coach's teaching-elements hook).
3. If the result matches the prediction: Transfer passes on the observed evidence.
4. If the result does not match: the discrepancy is the Transfer question. "What
   assumption did you make that the output contradicts?"

The specific command or tool is supplied by the coach's hook, not by this engine
reference. The engine specifies only the predict-then-verify protocol.

---

## Failure Handling Inside the Gate

When a stage fails, the coach does not simply re-ask the same question. The failure
escalation ladder is defined in the Failure Escalation section of ENGINE.md. Key
reminders specific to the Gate:

- Two-strike restraint: the student's first "not sure / I don't know" is not a fail and
  does not start the ladder. Hand the ball back once — "give me your best guess first" —
  and let them hold it. Only a second consecutive stall counts as the failed attempt
  that enters the ladder. Rationale: coaches systematically intervene one step too
  early, stealing the productive struggle; students shrunk down to a thought experiment
  usually reason their way back unaided.

- Attempts 1 and 2: reteach using a different angle or analogy. The question in the
  next attempt must differ from the previous attempt.
- Attempt 3: check for a prerequisite gap before continuing down the ladder.
- Attempt 4: split the chunk. Each sub-chunk gets its own full gate cycle.

Never ask the same question twice in the same attempt sequence. Repetition does not
test understanding; it tests memory of the earlier answer.
