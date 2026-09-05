# Cross-Coach Governance

This file governs prioritization across coaches. `ENGINE.md` still owns teaching mechanics,
and each domain `progress.md` remains the runtime source of truth. This overlay decides
which evidence is worth producing next; it does not redefine progress fields or certify
mastery.

## Session-start routing

After reading `ENGINE.md` and before choosing new work:

1. Read the domain `progress.md` and the current decisions in its `curriculum-plan.md`
   when present; resume the active breakpoint within that approved scope.
2. Read `workspaces/shared/root-patterns.md`; use only this track's active patterns.
3. If the session is planning, assessment, or portfolio work, read
   `competency/l6-matrix.md` and `portfolio/platform-eks/README.md`.
4. Prefer work that both tests an active pattern and produces evidence required by the
   matrix or the next `platform-eks` milestone. Domain prerequisites and safety rules
   still apply.

Do not preload the matrix or flagship plan for a simple breakpoint continuation where
neither can affect the next action.

## Current decisions and historical notes

For teaching format, scope, and scheduling, the latest explicit student decision takes
precedence over older briefs, generic hooks, and stale next-action reminders. Dates alone
do not make a coach's suggestion an approved decision. Keep the original records intact;
apply the decision when planning the next session. Safety and honest evidence still apply.

Known retirements to honor:
- SD: the 2026-07-18 plan removed the three-consecutive-pass exit requirement. The
  2026-08-11 plan requires teaching new topics before their drill. Old execution-heavy
  instructions must not freeze new content or presume every gap is only an output issue.
- K8s: the 2026-08-11 plan retired packet-station recitation and repo-scheduled story
  mining. Use incident scenarios for networking; behavioral material is managed outside
  this repo. A stale “sessions without mining” reminder is not debt. Behavioral mocks
  still use real stories when requested or required by an assessment.
- LeetCode: the standalone rebuild owns its state and practice loop. Historical
  answer-debt and engine review schedules do not apply to it.

## Sustainable practice

For a planning session, start with a two-week trial: two platform sittings and one
design sitting per week, plus three short coding practices if the student's time permits.
These are adjustable slots, not deadlines or make-up debt. Resume existing breakpoints;
one sitting need not finish a topic. English practice uses a familiar result and the
student's existing language workflow; increase language load after the mechanism is stable.

Platform work extends the shop baseline; design work supplies its capacity model,
failure modes, SLO and cost decisions. Review the trial using fewer hints, independent
changed-scenario answers, and reproducible artifacts, not pages read or phase count.

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

Readiness reports name the matrix snapshot date and compare it with newer domain evidence.
Report stale or missing evidence explicitly; do not silently promote a score or treat
an old debt count as current. A “L6 answer” is a worked example, not a job-level verdict.
Report hiring readiness by demonstrated skills; long-term senior scope additionally
needs attributable work outcomes, collaboration, rollout decisions and sustained impact.

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
