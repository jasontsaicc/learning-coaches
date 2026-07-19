# Thread-Pull List (P0 artifact)

Built 2026-07-19, session 1. Source: resume.md at job-applications/aws-proserve-tw (pre-submission version).
Each line of the resume is a promise; these are the questions that test the promise.
Priority = how likely × how deep the probe goes for a ProServe Delivery Consultant loop.

## Priority A — will be probed, must hold (prep before phone screen)

### Migration bullet (eCloudValley #1) — THE bullet for this role
- Walk me through the migration. Cutover plan? Rollback plan? Downtime?
  - Answer shape: assess deps → build new env in parallel → data sync → cutover (DNS/traffic) → rollback criteria. Map to Assess/Mobilize/Migrate language (P2).
- SQS in-flight messages and ElastiCache data — how do you move stateful pieces?
  - SQS: stop producers, drain consumers. ElastiCache: cold start vs warm-up; know what can be dropped vs must move.
- Why ArgoCD instead of Terraform for apps? What breaks if ArgoCD is down?
  - 4-beat: app change frequency >> infra / ArgoCD down = deploys freeze, runtime unaffected / git desired state + reconcile loop / infra=TF, app=ArgoCD boundary.
- Four EKS environments — differences, and how does a change promote?

### Outposts bullet (TPIsoftware #1) — hybrid goldmine
- Why Outposts instead of region? What customer constraint forced it? (data residency / regulator / latency — name the real one)
- How does Outposts connect to the region; what still works when the service link drops? (service link, local gateway, local data plane survives, control plane degraded)
- What did data/network isolation concretely mean for the regulator?

### VMware line (TPIsoftware #2) — expect the migration pivot
- "If that VMware customer moved to AWS today, walk me through your approach." (relocate vs rehost, MGN; P2 trains this)

### Terragrunt (Summary + eCloudValley #3) — RETEST DUE 2026-07-22 (Mistake Registry)
- What forces duplication in plain Terraform; what mechanism does Terragrunt use?
  - backend block can't take variables → copy-paste per env → wrong key = shared state = corrupt prod → remote_state + generate + path_relative_to_include → judgment: this scale yes, small project no.

## Priority B — likely, medium depth

### CI/CD 6h→1h, ~70% (eCloudValley #2)
- Where did the 5 hours go? How measured?
- Why both GitLab CI and Jenkins? (honest answer: history + migration in progress, know why not to force-kill)
- What is a "guardrail" concretely?

### 1,500 resources import (eCloudValley #3)
- How did you import existing resources without breaking anything? (import → plan to no-diff, batch scripting)
- What does "audit-ready" mean — who audits, what do they ask? (change record: who/when/diff/approver; retained plans = pre-change evidence)
- Drift detection after import?

### RBAC / prod gate (eCloudValley #6)
- Technically, what stops a dev deploying to prod? (protected environments/branches + approval rules — name the exact control)
- "Eliminating" — zero since? How do you know? (have the number or soften the word)

### RHEL hardening (TPIsoftware #5) → feeds linux-interview-bank
- Which benchmark (CIS)? What categories of change?
- One vulnerability remediated without breaking prod?

### Discovery / presales (TPIsoftware #3) — day-job simulation
- How do you run technical discovery with a new customer? (current state → pain → constraints → success definition; have a real structure)
- Neo4j PoC: why graph shape? PoC success criteria?

## Priority C — possible, shallower

- Cross-account dashboard auth: hub role assumes read-only spoke roles, trust policy direction.
- LLM code-review bot: secrets scrubbing, false positives, human final reviewer.
- Observability hours→min: release monitoring vs steady state; deployment markers + error/latency delta.
- 40% Terraform efficiency: one-line measurement definition.
- Certs: SA Pro → landing zone design; Security Specialty → KMS / account isolation.
- Australia years: career-change story → LP track (fsi-devops-english), not this coach.

## Linux-interview-bank priority order (derived)

1. IRQ/softirq (known hole, memory) — reachable via RHEL hardening/perf probes
2. static vs shared library (known hole, memory) — reachable via RHEL/build probes
3. CIS hardening mechanics (services, accounts, kernel params)
4. patching/vuln remediation without breaking prod (kernel live patching, staged rollout)

## Resume edit suggestions (pre-submission)

| Line | Suggestion | Why |
|------|-----------|-----|
| eCV #1 migration | Add cutover result: "with a controlled cutover and zero production downtime" (if true) | Migration role; line has process but no outcome |
| eCV #2 "~70%" | Prepare one-line definition (70% of what, counted how) | Every number is a promise |
| eCV #6 "eliminating" | Keep only if you can say "zero accidental prod deploys in N months, vs M/quarter before"; else soften to "preventing" | Absolute words get pressed |
| TPI #4 "~40%" | Same: one-line measurement baseline | Same |
