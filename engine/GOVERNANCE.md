# Cross-Coach Governance

This file governs prioritization across coaches. `ENGINE.md` still owns teaching mechanics,
and each domain `progress.md` remains the runtime source of truth. This overlay decides
which evidence is worth producing next; it does not redefine progress fields or certify
mastery.

## Session-start routing

After reading `ENGINE.md` and before choosing new work:

1. Read the domain `progress.md`; an active breakpoint wins and must be resumed.
2. Read `workspaces/shared/root-patterns.md`; use only this track's active patterns.
3. If the session is planning, assessment, or portfolio work, read
   `competency/l6-matrix.md` and `portfolio/platform-eks/README.md`.
4. Prefer work that both tests an active pattern and produces evidence required by the
   matrix or the next `platform-eks` milestone. Domain prerequisites and safety rules
   still apply.

Do not preload the matrix or flagship plan for a simple breakpoint continuation where
neither can affect the next action.

## WIP limit

- Each track has at most three active root patterns. New evidence attaches to an existing
  pattern whenever its failure mechanism matches.
- A genuinely new pattern enters backlog when all three active slots are occupied. Moving
  it to active requires moving one current pattern out.
- Review at most three root patterns per week. The original Mistake Registry entries keep
  their own engine-defined review and resolution state.

The overlay groups evidence; it never bulk-resolves the underlying mistakes.

## Evidence lifecycle

Use this sequence for cross-coach evidence:

1. **Acquire:** success with fresh teaching or substantial scaffolding. Record in the
   domain session log; do not raise the L6 matrix from this alone.
2. **Retain:** unprompted cold success after at least seven days.
3. **Transfer:** unprompted success in a changed or cross-domain scenario.
4. **Certify:** isolated mock, Examiner verdict, reproducible artifact, or equivalent
   real-world evidence.

Update `competency/l6-matrix.md` only when a new scorecard, Examiner verdict, cold test,
reproducible artifact, or attributable real-work result changes a row. Cite the source in
the row. When domain mastery and the matrix disagree, retain the lower confidence until
an isolated assessment resolves it.

## Portfolio promotion

`portfolio/platform-eks/` is the only active flagship. Existing domain portfolio folders
remain source-material libraries; do not relocate historical files solely for consistency.

Promote or create flagship material only when it includes:

- reproducible steps or executable configuration;
- objective verification evidence;
- a design decision and its trade-off;
- known limitations or failure modes.

Notes, screenshots, and coach-driven walkthroughs remain learning artifacts until they
meet this gate. Terraform, Kubernetes, observability, security, cost, delivery, and
incident work should extend the same shop platform rather than start parallel showcases.

## Coach evidence ownership

| Coach | Primary evidence responsibility |
|---|---|
| K8s | troubleshooting, technical depth, reliability |
| Terraform | state safety, delivery, policy, blast radius |
| System Design | architecture judgment, capacity, trade-offs |
| Cloud Architect | customer ambiguity, migration, leadership, English delivery |
| LeetCode / Ops coding | correctness, complexity, timed communication, automation |

Ownership prevents duplicated curricula; it does not prevent a cross-domain assessment.

## Session close

At step H:

1. Append concrete failures to the domain Mistake Registry using its existing schema.
2. Map new unresolved evidence to RP1–RP7 in the shared overlay; reuse an existing pattern
   unless the failure mechanism is genuinely new.
3. Update the matrix only when the evidence lifecycle permits it.
4. Record portfolio output as source material or promoted flagship evidence according to
   the promotion gate.

Repository synchronization is a separate operation. Inspect `git status` first, preserve
unrelated user changes, and commit or push only when the user has authorized that action.
