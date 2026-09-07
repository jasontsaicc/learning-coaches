# Cross-Coach Governance

This file governs prioritization across coaches. `ENGINE.md` still owns teaching mechanics,
and each domain `progress.md` remains the runtime source of truth. This overlay decides
which evidence is worth producing next; it does not redefine progress fields or certify
mastery.

## Session-start routing

First distinguish planning/repository maintenance from an actual learning session.
Planning reads the relevant evidence and plans; it does not run diagnostics, Comeback,
Weekly Review, gates, or learning-state writes. For a learning session, read `ENGINE.md`
once in the current context and then route before choosing new work:

1. Read the domain progress file's Meta and Current Session breakpoint, then its current
   curriculum-plan decisions when present; resume within that scope. Discover headings
   first and read complete relevant sections, rather than truncating an arbitrary prefix.
2. Read the Active WIP and resolution protocol in `workspaces/shared/root-patterns.md`;
   use only this track's active patterns. Read supporting pattern evidence when needed.
3. If the session is planning, assessment, or portfolio work, read
   `competency/l6-matrix.md` and `portfolio/platform-eks/README.md`.
4. Prefer work that both tests an active pattern and produces evidence required by the
   matrix or the next `platform-eks` milestone. Domain prerequisites and safety rules
   still apply.

Do not preload the matrix or flagship plan for a simple breakpoint continuation where
neither can affect the next action.

## Context loading contract

The coach's Hook Map is an index, not a startup checklist. Resolve workspace paths from
its portfolio hook. Load each hook when the next action needs it:

| Action | Required context beyond engine/governance and current state |
|---|---|
| Start/resume teaching | portfolio workspace/write rules; teaching-elements' shared rules and current step; current topic/chunk material |
| Choose a topic / check prerequisites | curriculum phase map and relevant prerequisite/mastery entries; north-star when scope is disputed |
| Run a lab | lab-manager when supplied; current environment/context safety facts and lab instructions |
| Review / Comeback | Meta, applicable engine protocol, relevant queue and unresolved rows; selected item's notes only |
| Score G / mock | scorecard-dims and applicable interview format; first answer before feedback |
| Phase Gate | phase-gates for this phase and Examiner protocol; isolated assessment remains mandatory |
| Use English / narrative | language or narrative hook for the chosen step, when supplied |
| Save / close | progress schema sections and existing entries being changed; portfolio write/quality rules |
| Plan / readiness review | current domain decisions/evidence, matrix snapshot, flagship milestones; [learning project](../docs/devops-learning-project.md) for cross-coach planning |

Before choosing a review item, inspect the relevant queue and unresolved registry rows
so due/aged items are not lost. Weekly Review reads the evidence window required by its
protocol; a wider audit may read more. Unknown headings or ambiguous state justify
expanding the read. A file already fully available and unchanged in the current context
does not need another tool read; after compaction, reload missing rules/current state.

Student-specific teaching constraints are hot context even when stored inside a large
historical file: K8s reads `session-log.md`'s teaching-profile and coach-discipline sections;
SD reads `coaching-brief.md`'s effective/ineffective methods, language and coach self-check
sections, plus the active weakness's subsection. Current decisions below retire stale
instructions within those sections. Session narratives, complete score histories, entire
question banks and model answers are loaded only for an identified question or audit.

An ordinary teaching turn delivers one explanation/diagram or one action/question, then
waits for the student. Give a complete worked example when needed; keep repeated recaps
and alternate model answers out of subsequent turns. Explicit requests for a full plan,
comparison or transcript receive that output. Historical per-question “L6 answer” notes
are satisfied by one concise comparison at the completed teaching question; subsequent
follow-ups address the new gap rather than regenerate the full model answer. Retain required F/G and save points; use
the existing Micro-mode when time is short. Routine teaching and chunk checks stay with
the coach; only formal Phase Gates require an Examiner, and other delegation needs an
explicit task-specific reason and authorization. If the student declines an agent, honor
that choice and offer coach-scored practice without an independent certification claim.
Saving updates changed facts once in
their canonical location, with links from projections instead of copied narratives.

This reduces context retrieval, not an enforceable model-token quota. Measure actual
input/output/cache usage only if the host exposes it; otherwise report UTF-8 bytes and
loaded file/section counts as proxies, never as measured token savings.

## Current decisions and historical notes

Current targets (student confirmed 2026-09-07): active study tracks are K8s and System
Design, building toward Senior DevOps/SRE. AWS Delivery Consultant remains a future
application goal after a first-stage rejection; the rejection reason is unknown and is
not technical assessment evidence. There is no scheduled interview. Terraform is pulled
into platform work when needed; CA/customer cases are optional overlays, not a third
weekly course. Senior/L6 remains an aspiration, not a certified current level.
This replaces the old four-week ProServe urgency without discarding the SRE route,
resetting domain breakpoints or reactivating old debt.
The personalized route and provisional weekly capacity live in
`docs/devops-learning-project.md`; read that document for planning, not every lesson.

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
- K8s: the 2026-08-20 coach-discipline decision puts new content first and brief review
  near the close. The 2026-08-21 curriculum-plan §11 restores production-depth labs,
  command-intent checks and on-premises/traditional EKS/managed EKS comparisons. Preserve
  those decisions when reducing context; do not revive the old coverage-only sprint.
- LeetCode: the standalone rebuild owns its state and practice loop. Historical
  answer-debt and engine review schedules do not apply to it.

## Sustainable practice

For a planning session, start with a two-week trial: two K8s/platform sittings and one
System Design sitting per week, plus short coding practices if time permits. Preserve
existing breakpoints; add a customer-facing lens inside an SD review when useful without
automatically restarting the CA course.
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
