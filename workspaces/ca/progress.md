# progress

## Meta
- session_count: 2
- last_weekly_review: 0
- last_session_date: 2026-07-19
- warm_up_classification: mid (strong hands-on resume material; can name tools and outcomes but mechanism-level articulation gaps — see Terragrunt registry item; English output not yet exercised this session)

## Application status (warm-up intake, 2026-07-19)
- resume: not submitted; referral ask planned 2026-07-20 (former colleague)
- recruiter reply: none
- phone screen / loop dates: none — default 4-week schedule stands
- resume file: /home/ubuntu/go_senior_devops/job-applications/aws-proserve-tw/resume.md
- language preference (asked once): simple English as main language; short Traditional Chinese assists for hard concepts. Ramp to full-English mocks in W4 per language hook.

## Current Session breakpoint
- P1, gap-scan round 1 complete, next-action: next session opens with step A spaced-rep (4 mistake items due 2026-07-22) then P1 retests (15 items in gap-scan.md); Linux bank P0-1/P0-2 still queued (not yet started).
- Student's plan: resume self-prep with model-answers.md in parallel; BQ/LP via fsi-devops-english.

## Session 2 notes (2026-07-19)
- Ran full P1 gap-scan (16Q): 1 pass / 10 shaky / 5 hole. Detail + mini-lesson content in gap-scan.md.
- Pattern: names present, mechanisms missing; 3 dangerous inversions logged to Mistake Registry; hybrid cluster (BGP/resolver endpoints/MTU) is the deepest hole and overlaps the Outposts resume line.
- Format that worked: grade → mini-lesson in EN (L6 voice) + zh version on request. Student engaged consistently across all 16 — much better throughput than session 1's deflection pattern. English output still all-receptive; retests on 07-22 must be produced by the student, in English, out loud.

## Session 1 notes (2026-07-19)
- Warm-up intake done: no dates yet, referral ask 2026-07-20; language = simple English + short zh-TW assists.
- Student requested interviewer mode (routing branch 4), then full survey mode: coach swept entire resume, produced thread-pull-list.md (P0 artifact done).
- Student's own line-1 predictions: EKS depth, EKS-vs-ECS why, CI/CD permissions + audit — good instincts, missed Terragrunt and "audit-ready" concreteness.
- Coaching observation (honest, for next session): student deflected English output 4× (hint → model answer → zh version → skip). Output debt is real; the Terragrunt retest on 2026-07-22 is the collection point. Do not let survey/input mode become the default; W3-W4 English mocks depend on output reps starting now.
- Taught inline (mini-lesson): why Terragrunt exists — backend block can't interpolate vars → forced copy-paste → blast-radius risk → remote_state/generate/path_relative_to_include; 4-beat answer skeleton (constraint → risk → mechanism → judgment) established as the standard answer format for all thread-pull questions.

## Phase status
- P0: complete (artifact: thread-pull-list.md; no formal gate defined for P0)
- P1: in-progress (round 1 scan complete 2026-07-19: 1 pass / 10 shaky / 5 hole; closes only when all 15 retests pass — see gap-scan.md)
- P2: not-started
- P3: not-started
- Sidecar linux-interview-bank: not-started

## Mastery
- aws-networking (P1 scope): low (s2 — 1/16 pass at mechanism level; retests pending)
- tgw-vs-peering: high (s2 — only clean pass, transitivity mechanism articulated)

## Scorecard history
(none yet)

## Mistake Registry
- 2026-07-19 | Terragrunt rationale | could only say "reduces duplicated code, clearer structure"; couldn't name WHICH files are duplicated or the mechanism (backend block can't use variables → remote_state + generate + path_relative_to_include) | tool-used-but-mechanism-unnamed | unresolved | 3 | 2026-07-22 | 1
- 2026-07-19 | refused vs timeout | inverted: thought refused = blocked; actually refused = live host RST no listener (app layer), timeout = silent drop SG/NACL/route (network layer) | inverted-diagnostic-fork | unresolved | 3 | 2026-07-22 | 1
- 2026-07-19 | subnet↔route-table binding | said subnet can bind multiple route tables; it's exactly one (one table serves many subnets) | inverted-cardinality | unresolved | 3 | 2026-07-22 | 1
- 2026-07-19 | NAT gateway placement | placed NAT GW in private subnet; it lives in public subnet (needs IGW route + EIP), private RT points to it | wrong-placement-mental-model | unresolved | 3 | 2026-07-22 | 1

## Spaced-repetition queue
- mistake:Terragrunt-rationale | mistake | 3 | 2026-07-22 | active
- mistake:refused-vs-timeout | mistake | 3 | 2026-07-22 | active
- mistake:subnet-route-table-binding | mistake | 3 | 2026-07-22 | active
- mistake:NAT-gateway-placement | mistake | 3 | 2026-07-22 | active
- gap-scan retest block (15 items, see gap-scan.md) | chunk | 3 | 2026-07-22 | active

## Curiosity branch
(none yet)

## Domain registries

### Thread-pull list (P0 artifact, feeds linux-interview-bank priority)
Delivered: see `thread-pull-list.md` in this directory (priorities A/B/C + linux-bank order + resume edit suggestions).

## Examiner ledger
(none yet)
