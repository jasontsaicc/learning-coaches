# Model Answers — Senior AWS DevOps voice

Companion to `thread-pull-list.md`. Each answer is a 30-60 second spoken skeleton in the
4-beat shape where it fits: constraint → risk → mechanism → judgment.

Rules for use:
- `[FILL: ...]` = your real fact goes here. Never speak a fact that isn't yours; interviewers press one level deeper and invented details collapse.
- These are skeletons to internalize, not scripts to memorize. Say each one out loud, then rebuild it in your own words.
- Retest debts (e.g. Terragrunt) still get collected verbally.

---

## Priority A

### A1. "Walk me through the migration. Cutover plan? Rollback? Downtime?"

> "The migration was from another team's AWS accounts into a new multi-account setup, so the first phase was assessment: inventory the workloads — EKS services, Lambdas, ECS tasks, SQS queues, ElastiCache — and map their dependencies, because the dependency graph decides cutover order. Second phase, we built the target environments in parallel with Terraform and ArgoCD, so the new platform was fully stood up and tested while production kept running in the old accounts. That's the key risk decision: never migrate in place; build alongside, then move traffic. Cutover itself was [FILL: DNS weight shift / traffic switch method], with rollback being [FILL: e.g. flipping DNS back, old env kept warm for N days]. Downtime was [FILL: number]. The lesson I'd carry to a customer: the assessment phase is where migrations are won — every surprise at cutover is a dependency you missed in week one."

Why senior: maps personal story onto Assess/Mobilize/Migrate without naming AWS methodology in a forced way; ends with a consultant-grade generalization.

### A2. "SQS had in-flight messages, ElastiCache had live data. How did you move stateful pieces?"

> "The rule I use: classify state into 'can be drained', 'can be rebuilt', and 'must be copied'. SQS is drainable — point producers at the new queue, let old consumers empty the old one, decommission when depth hits zero. No message is ever in only one place you can't recover. ElastiCache is rebuildable — it's a cache, the source of truth is the database, so the real question is cold-start impact: can the backend take the hit-rate drop while the new cache warms? [FILL: what you actually did — cold start with off-peak cutover, or pre-warming]. Databases would be the 'must copy' class — DMS with CDC — but in this migration [FILL: your DB situation]. The classification matters more than the tools: it tells you what you're allowed to just throw away, and that's usually the fastest migration path."

### A3. "Why ArgoCD for apps instead of just Terraform? What breaks if ArgoCD is down?"

> "Different change frequencies want different tools. Infra changes a few times a week and wants a plan-review-apply gate; app deploys happen many times a day and want to be self-service for developers. So Terraform owns the platform — clusters, VPCs, IAM — and ArgoCD owns what runs on the clusters, with git as the desired state and a reconcile loop enforcing it. If ArgoCD is down, deploys freeze but nothing running is affected — the apps don't know ArgoCD exists. That failure mode is exactly why I like GitOps: the deploy tool is not in the runtime path. And when ArgoCD comes back, it reconciles to whatever git says, so recovery is 'fix ArgoCD', not 'replay lost deployments'. The boundary I hold: if Terraform and ArgoCD both could manage something, whichever owns its lifecycle wins — split ownership of one resource is how you get drift fights."

### A4. "Four EKS environments — what differs, and how does a change promote?"

> "[FILL: your actual four — e.g. dev / staging / UAT / prod]. They're structurally identical by design — same Terraform modules, same ArgoCD app-of-apps pattern — and differ only in data: instance sizes, replica counts, account IDs. That's deliberate: an environment that's structurally different from prod validates nothing. Promotion is a git operation — [FILL: how — e.g. PR merges bump the image tag / kustomize overlay per env], so the audit trail of who promoted what is the git history itself. The judgment call: fewer environments is better than more. Every extra env costs money and drifts; we kept four because [FILL: real reason — e.g. UAT was a customer-facing requirement]."

### A5. "Why did the customer choose Outposts instead of the region? What forced it?"

> "The forcing constraint was [FILL: the real one — for a Taiwan life insurer, typically the regulator's data-residency and audit posture for core insurance data]. This is the honest framing: nobody chooses Outposts for fun — it's the answer when the workload must stay on premises but the customer wants the AWS control plane, the same APIs, IAM, and tooling as the region. The alternatives we'd weigh: pure on-prem (loses the AWS operating model), region with the regulator's approval path (timeline risk), or Outposts as the middle. The trade-off you accept: capacity is fixed — you order racks, you don't autoscale past them — and a subset of services. So it's the right call only when the constraint is genuinely immovable, which for [FILL: customer context] it was."

### A6. "How does Outposts connect back to the region, and what still works if that link goes down?"

> "The Outpost is anchored to a parent region through the service link — an encrypted VPN-like channel over [FILL: your setup — Direct Connect or internet]. Control plane lives in the region; data plane is local. So when the service link drops: workloads already running keep running, local traffic through the local gateway keeps flowing — the disconnect does not take down the site. What you lose is control-plane operations: no new instance launches, no configuration changes, and monitoring data queues up. That asymmetry is the whole design: AWS put the data plane on-site precisely so a WAN cut degrades management, not service. Operationally that means you size and deploy for 'what if I can't touch it for a day', and you treat service-link health as a first-class alarm."

### A7. "What did 'data and network isolation' concretely mean for the regulator?"

> "Three layers. Network: [FILL: your real design — e.g. dedicated VLANs/subnets separating core insurance data from general workloads, no direct internet path, traffic through inspected egress]. Identity: IAM boundaries so the operations team could touch infrastructure but not data — separation of duties, which is what the auditor actually checks. And evidence: it's not enough to be isolated, you must show it — flow logs, config records, change history. The thing I learned in FSI: the regulator's question is never 'is it secure', it's 'prove who could access what, and show me the record'. Designing for auditability from day one is cheaper than retrofitting evidence."

### A8. "If that VMware customer wanted to move to AWS today, walk me through your approach."

> "Start with discovery, not tooling: inventory the VM estate, dependencies, licensing, and which apps the business actually still needs — some of that estate is always retire or retain. Then per workload it's a 7R decision. The bulk default for a VMware fleet is rehost with MGN — block-level replication, test launches, low-risk cutover waves. Anything with an aggressive timeline and deep vSphere integration might justify relocate to VMware Cloud on AWS, but I'd challenge it: you pay to keep the problem. Databases get their own track — replatform to RDS where the engine allows, DMS for the move. A few high-value apps earn refactor, but not during the migration itself — my rule is 'migrate, then modernize'; doing both at once doubles the failure modes. Wave planning comes from the dependency map: move whole dependency clusters together, quick wins first to build the customer's confidence."

### A9. Terragrunt (retest item — say this one out loud, it's due 2026-07-22)

> "The core constraint: Terraform's backend block can't take variables — it's hard-coded. So multi-account, multi-env setups force a near-identical backend and provider block into every stack folder, differing only in the state key or role ARN. The risk isn't ugliness: one wrong state key and two environments share state — that's how prod gets corrupted. Terragrunt fixes it at the root: one terragrunt.hcl defines remote_state once, generates backend.tf and provider.tf at runtime, computes each stack's key from its folder path — the directory tree is the state layout. Plus dependency blocks and run-all for orchestration. At our scale — 1,500 resources across accounts — yes I'd use it again; for a small single-account project, plain Terraform is simpler."

---

## Priority B

### B1. "6 hours to 1 hour — where did the five hours actually go?"

> "[FILL: your real bottleneck breakdown — the honest pattern is usually: manual steps between stages, sequential jobs that could parallelize, no caching, and waiting for humans]. We measured wall-clock from merge to production-ready, before and after, across [FILL: sample]. The fix was less about faster runners and more about removing human hand-offs: reusable templates so teams stopped hand-writing pipelines, parallelized test stages, [FILL: specifics]. The measurement discipline matters: 'felt faster' isn't a metric — we tracked [FILL: how]."

### B2. "Why are you running both GitLab CI and Jenkins?"

> "History, honestly — Jenkins predates the GitLab adoption, and some teams have deep Jenkins-plugin dependencies. The strategy is convergence, not a forced cutover: new projects start on GitLab CI with the shared templates; Jenkins jobs migrate when a team touches them for other reasons. Killing Jenkins in one quarter would burn goodwill and risk breaking builds nobody fully understands, for zero user-visible benefit. A consultant answer: two CI systems is a cost, but a controlled dual-run is cheaper than a big-bang migration of working pipelines."

### B3. "What does a 'guardrail' concretely mean in your templates?"

> "Things a project gets by default and can't quietly remove: [FILL: your real ones — e.g. mandatory security scanning stage, protected-branch deploy rules, prod deploys only from tagged releases, approval gate on the prod environment]. The template includes them; a team overriding them is visible in the diff. The principle: make the safe path the lazy path — if compliance requires effort, people route around it."

### B4. "1,500 existing resources — how did you import them without breaking anything?"

> "The invariant: import is only done when plan shows no diff. Import puts the resource in state; then you iterate the HCL until Terraform agrees reality already matches — at that point Terraform 'owns' it with zero pending change, and nothing was touched. At 1,500 resources you script it: [FILL: your tooling — import blocks / bulk scripts / import wizard]. Order matters: start with low-blast-radius resources, IAM and stateful things last and most carefully. And you freeze console changes per batch, or you're importing a moving target. It's slow, deliberate work — which is the point; the fast version is the one that breaks prod."

### B5. "'Audit-ready' — who audits, and what do they ask for?"

> "[FILL: who — e.g. financial regulator audits the customer, customer's compliance audits us]. What they ask is always the same shape: for this change, show me who requested it, who approved it, what exactly changed, and that the approver isn't the requester. Our answer is the PR trail plus retained plan outputs — the plan file is evidence of what was about to change, captured before it happened, attached to the approval. That 'before' evidence is the part ad-hoc processes can't reconstruct after the fact."

### B6. "How do you catch drift after import?"

> "[FILL: your real mechanism — e.g. scheduled plan runs surfacing unexpected diffs / pipeline-only applies with locked-down console access]. Two complementary controls: detect drift (scheduled terraform plan, alert on diff) and prevent it (humans lose write access outside the pipeline — SCPs or read-only roles). Prevention beats detection, but you keep both: break-glass changes during incidents are legitimate, and detection is how they get reconciled back into code instead of becoming permanent lies in the state."

### B7. "Technically, what stops a developer deploying to prod?"

> "Named controls, not policy documents: prod is a protected environment in GitLab — only specific groups can trigger deploy jobs to it; branches feeding it are protected — no direct push, merge only via approved PR; and approval rules require [FILL: N] reviewers with the approver/author separation enforced. Dev environments are the opposite — self-service, no gate — which is deliberate: friction belongs at the blast radius, not everywhere. The proof it works: [FILL: your number — accidental prod deploys before vs after]."

### B8. "'Eliminating' accidental deploys — how do you know?"

> "Because the path doesn't exist anymore, and the record backs it: before, an accidental prod deploy was [FILL: how it used to happen]; after, deploying to prod requires being in the deployers group AND an approved MR on a protected branch — there's no sequence of honest mistakes that gets you there. Since rollout: [FILL: N months, zero accidental prod deploys, vs M/quarter before]. If I can't back the absolute claim with that record, I soften the word — but here the control is structural, not behavioral."

### B9. "RHEL hardening — which benchmark, what categories?"

> "[FILL: confirm — typically CIS RHEL benchmark, possibly customer-specific FSI baseline]. The work falls into buckets: services and packages (remove what isn't needed — the cheapest attack-surface win), authentication and accounts (password policy, sudo rules, no shared root), network and kernel parameters (sysctl hardening, firewall defaults), logging and audit (auditd rules so the evidence exists), and file permissions/SELinux. The senior-level caveat: you never apply a full benchmark blindly — every control gets tested against the workload, because some CIS items break real applications, and 'hardened but down' fails the audit too."

### B10. "Tell me about one vulnerability you remediated without breaking production."

> "[FILL: pick ONE real case before the interview — this cannot be improvised. Shape it as: what the finding was → why naive patching was risky (dependency / reboot / legacy app) → how you tested (staging first, snapshot/rollback plan) → staged rollout → verification]. The generalizable part: the vulnerability is rarely the hard part; the hard part is proving the fix is safe on a system someone built years ago. Snapshot first, canary one node, verify the app, then fleet."

### B11. "How do you run technical discovery with a new customer?"

> "Four passes. Current state: what runs where, versions, dependencies — and I want to see it, not hear about it; the diagram is always out of date. Pain: what breaks, what's slow, what does the team fear touching. Constraints: regulatory, licensing, budget, timeline, and org constraints — who can say no. Success definition: what does 'done' look like in the customer's words, with a number on it. The discipline is asking 'what else should I have asked' at the end — the blocker is always the thing nobody thought to mention. From [FILL: a real engagement — e.g. the presales discovery you ran], the artifact that matters is the constraint list, because architecture is mostly eliminating options the constraints already killed."

### B12. "Why was a graph database right for that problem? PoC success criteria?"

> "The shape of the data was relationships, not records: [FILL: the actual TSMC problem shape — entities and connections, multi-hop questions]. In SQL, multi-hop relationship queries become join chains that get worse with depth; a graph DB makes traversal the native operation. PoC criteria were defined before we built: [FILL: real criteria — e.g. representative queries answered within X on realistic data volume, load path proven]. The consultant point: a PoC without pre-agreed success criteria isn't a proof of concept, it's a demo — and demos always succeed."

---

## Priority C

### C1. "Cross-account dashboard — how does it authenticate into each account?"

> "Hub-and-spoke IAM: the tool runs in a hub account and calls sts:AssumeRole into a read-only role deployed in every spoke account. Each spoke role trusts only the hub tool's role, scoped to the ECS describe/list actions it needs. Adding an account is deploying that role — which is itself Terraform, so onboarding is a PR. No long-lived credentials anywhere; every access is a short-lived session that shows up in CloudTrail."

### C2. "An LLM reviews your merge requests — secrets leakage and false positives?"

> "Boundary first: [FILL: your real setup — what the bot can see, whether it's Bedrock/API, what's scrubbed]. Secrets: pre-scrub diffs against secret patterns before anything leaves, plus secret-scanning in CI so secrets shouldn't be in diffs at all — defense in depth. False positives: the bot comments, humans decide; it never blocks a merge on its own judgment. We tuned it by [FILL: how — e.g. limiting to specific rule categories]. The adoption lesson: a noisy reviewer gets ignored, so precision matters more than recall — better to catch fewer things reliably than everything noisily."

### C3. "Release monitoring vs steady-state monitoring?"

> "Steady state asks 'is the system healthy' — SLO-shaped: error rate, latency, saturation, alarms on symptoms users feel. Release monitoring asks a sharper question: 'did this deploy make things worse than five minutes ago' — it's comparative, against the previous version, on a short window. Mechanically: deployment markers in Grafana so any metric shift lines up with the release that caused it, and alarms on error/latency deltas post-deploy [FILL: your specifics]. That comparison is what took detection from hours to minutes: nobody stares at dashboards, the deploy annotates itself and the delta alarm fires."

### C4. "40% efficiency improvement — measured against what?"

> "[FILL: one honest sentence — e.g. 'provisioning a standard FSI environment took ~X days of engineer time manually; the Terraform modules brought it to ~Y' — have the baseline and the counting method ready]. If the honest version is a range, say the range; a defended '30-40%' beats an undefended '40%'."

### C5. "You hold SA Pro — design a multi-account landing zone for a bank."

> "Organizations with an OU structure that mirrors blast radius and policy, not org chart: security OU (log archive, audit accounts), infrastructure OU (shared networking), workloads OU split prod/non-prod, sandbox. Guardrails as SCPs: deny root access keys, deny disabling CloudTrail/Config, region restrictions the regulator requires. Centralized: identity (SSO, no IAM users), logging (CloudTrail org trail to a locked log-archive account), networking (shared VPC or hub via TGW). Control Tower where its defaults fit; custom vending where FSI needs deviate [FILL: connect to your real multi-account build at eCloudValley]. The design driver: an account is the only true isolation boundary in AWS — so account structure is your security architecture."

### C6. "Security Specialty — how do you isolate data between accounts? KMS strategy?"

> "Accounts are the isolation primitive; everything else is policy on top. Cross-account access is explicit: resource policies plus assumed roles, never shared credentials. KMS: keys live in the account that owns the data, key policies grant specific cross-account principals — a KMS key policy is a second, independent gate; even a leaked role can't read what the key policy denies. CMKs per data classification [FILL: your real pattern], automatic rotation on. The principle: encryption doesn't protect data from someone who has the key — key policy design is access design."

### C7. "Why EKS and not ECS?" (your own predicted question — it will come)

> "We run both, so it's a real decision, not a religion. ECS wins on operational simplicity: no control plane to think about, great for a team that just wants containers running — our [FILL: what's on ECS] stays there happily. EKS wins when you need the Kubernetes ecosystem: ArgoCD GitOps, Helm charts, operators, and portability expectations [FILL: your real driver — e.g. customer requirement, multi-env GitOps]. The cost of EKS is real — upgrades, add-on lifecycle, deeper expertise — so my default for a greenfield small team is ECS, and EKS when the ecosystem need justifies the operational overhead. Choosing the heavier tool without that need is resume-driven engineering."

---

## How to practice (order matters)

1. A9 Terragrunt out loud first — it's the registry debt, due 2026-07-22.
2. Fill every `[FILL]` in Priority A with your true facts. A blank you can't fill = a gap to bring to session (that's P1/P2 material, not a failure).
3. One answer per sitting, out loud, in English, 60 seconds. Reading silently does not count as practice for an oral exam.
4. The 4-beat shape (constraint → risk → mechanism → judgment) is the reusable part. If you internalize only that, you can rebuild any of these live.
