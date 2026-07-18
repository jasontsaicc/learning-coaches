# cloud-architect-coach Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `cloud-architect-coach`, a 4-week sprint coach on the shared engine targeting the AWS ProServe Delivery Consultant - Cloud Architect (Taiwan) interview loop.

**Architecture:** A standard engine coach (thin SKILL.md + hook files under `references/`), scaffolded by `scripts/new-coach.sh`, no lab-manager hook (whiteboard/packet-path teaching, per spec decision 6), with three subject-material files beyond the engine hooks: a networking gap-scan, a customer case bank, and a Linux interview bank. LP behavioral is out of scope (delegated to `fsi-devops-english`).

**Tech Stack:** Markdown hook files; `scripts/lint-coach.sh` as the test harness; behavioral evals in `evals/evals.json` following the sd-coach format.

**Spec:** `docs/superpowers/specs/2026-07-18-cloud-architect-coach-design.md`. Read it before starting.

## Global Constraints

- Writing style (from user CLAUDE.md, applies to all authored prose): no em dashes (—); no inflated AI vocabulary (delve, leverage, comprehensive, robust, seamless, pivotal); no reflex tricolons; no bold-spam.
- Teaching prose in Traditional Chinese, structural headings in English. `lint-coach.sh` greps English marker words (`win condition`, `tie-break`, `warm-up`, `step b/c/e`, `gate`, `workspace`, `artifact`, `primary`, `tier 1`), so those must appear literally in headings or labels. This matches sd-coach and k8s-coach house style.
- Git commits: one-line subject only, no body, no attribution. Format: `cloud-architect-coach: <what>`.
- Coach must not re-implement engine mechanics (Feynman Gate, escalation, 60% threshold, spaced repetition). Hooks supply domain content only; `lint-coach.sh` rejects engine leaks.
- Do not duplicate k8s-coach material. Topics already covered in `skills/k8s-coach/references/foundations-linux-network.md` (TCP state machine §3, DNS resolution §4, OOM/cgroup §2.4, conntrack §3.5, perf triage §5) are cross-referenced by path and section, never rewritten.
- Timeline framing inside content: 4-week sprint, application submitted ~2026-07-20. If a phone screen lands early, mocks move forward (curriculum must say this).

---

### Task 1: Scaffold the coach and fill the thin SKILL.md

**Files:**
- Create (via script): `skills/cloud-architect-coach/SKILL.md` and `references/{north-star,curriculum,teaching-elements,scorecard-dims,phase-gates,portfolio,language}.md`

**Interfaces:**
- Produces: the directory layout and Hook Map every later task fills. Subject files added in Tasks 4, 6, 7 are `references/gap-scan-aws-networking.md`, `references/case-bank.md`, `references/linux-interview-bank.md`.

- [ ] **Step 1: Run the scaffold**

Run: `./scripts/new-coach.sh cloud-architect-coach --no-lab --with-language`
Expected: `Scaffolded skills/cloud-architect-coach`. Verify `references/lab-manager.md` does NOT exist and the `| lab-manager |` row is absent from SKILL.md (`grep -c 'lab-manager' skills/cloud-architect-coach/SKILL.md` → `0`).

- [ ] **Step 2: Fill SKILL.md**

Replace the frontmatter description TODO with:

```
AWS ProServe Cloud Architect interview sprint coach (Feynman-based, 4-week plan, Traditional Chinese teaching with English mocks). Use PROACTIVELY when the user mentions the AWS Delivery Consultant / Cloud Architect / Professional Services interview, cloud migration methodology (7R, MAP, landing zone), AWS hybrid networking for interview prep (TGW, Direct Connect, hybrid DNS), Well-Architected case practice, consultant case mocks, or EC2/Linux interview question drills (linux-interview-bank). Also trigger on 上雲, 遷移案例, ProServe 面試, 雲端架構師面試.
```

Append three rows to the Hook Map table (these are subject-material files the curriculum references, same convention as k8s-coach's foundations file):

```
| gap-scan (P1 subject) | `${CLAUDE_SKILL_DIR}/references/gap-scan-aws-networking.md` |
| case-bank (P2/P3 subject) | `${CLAUDE_SKILL_DIR}/references/case-bank.md` |
| linux-interview-bank (sidecar) | `${CLAUDE_SKILL_DIR}/references/linux-interview-bank.md` |
```

- [ ] **Step 3: Verify**

Run: `grep -q 'engine/ENGINE.md' skills/cloud-architect-coach/SKILL.md && grep -q 'linux-interview-bank' skills/cloud-architect-coach/SKILL.md && echo OK`
Expected: `OK`. (Full lint still fails on unfilled reference TODOs; that is expected until Task 12.)

- [ ] **Step 4: Commit**

```bash
git add skills/cloud-architect-coach/
git commit -m "cloud-architect-coach: scaffold + thin SKILL.md"
```

---

### Task 2: north-star.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/north-star.md`

- [ ] **Step 1: Write the hook**

Replace all TODOs. Required headings: `## Win Condition`, `## Tie-Break`. Content from spec "Context and Goal":

- Win condition: given an unseen migration or hybrid-architecture case, the student delivers a structured answer (Assess/Mobilize/Migrate&Modernize plan, per-workload 7R judgment with stated reasons, hybrid networking design, Well-Architected trade-offs) at hire bar in English, and survives resume thread-pulls into EC2/Linux depth via the linux-interview-bank material.
- Tie-break: delivery over coverage. When case/mock practice competes with learning one more AWS service for session time, the mock wins; this loop scores judgment and communication, not encyclopedic service knowledge. Second tie-break from spec decision 5: if a phone screen or loop date lands, reshuffle the week plan around it (mocks move forward).

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'win condition' skills/cloud-architect-coach/references/north-star.md && grep -iq 'tie-break' skills/cloud-architect-coach/references/north-star.md && ! grep -q 'TODO:' skills/cloud-architect-coach/references/north-star.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/north-star.md
git commit -m "cloud-architect-coach: fill north-star hook"
```

---

### Task 3: curriculum.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/curriculum.md`

**Interfaces:**
- Produces: phase names `P0 意識定向`, `P1 Networking Gap-Scan`, `P2 Migration`, `P3 Case Drills`, `Sidecar: Linux Bank` used verbatim by phase-gates (Task 9) and scorecard-dims (Task 8).

- [ ] **Step 1: Write the hook**

Replace all TODOs. Needs a `warm-up` marker and >= 3 `## ` subsections. Structure:

- `## Warm-Up Diagnostic (new students / week 1 intake)`: confirm application status and any recruiter/interview dates first (dates reorder everything); then run the resume thread-pull exercise: student reads their own resume line by line and predicts "這行會被追問什麼", coach records the list into the progress file. This list feeds P0's output and the linux-interview-bank priority order.
- `## P0 意識定向 (0.5 week)`: what a ProServe Delivery Consultant does day-to-day (customer workshops, migration delivery, architecture docs); loop anatomy: phone screen (LP + light technical) arrives 1-2 weeks before the full loop, full loop is ~50% LP-weighted with every interviewer scoring LPs; deliverable: personalized thread-pull list. Prereq: none.
- `## P1 Networking Gap-Scan (0.5 week)`: run `references/gap-scan-aws-networking.md`. Rule from spec decision 3: "familiar" is tested, not trusted; mechanism-level answer → skip, stuck → the hole becomes a mini-lesson. No labs. Prereq: P0 done.
- `## P2 Migration (1 week)`: three phases (Assess / Mobilize / Migrate & Modernize), 7R decision logic, tool chain (MGN, DMS/SCT, DataSync/Snowball, Migration Hub), landing zone (Control Tower, multi-account), hybrid connectivity and hybrid DNS (second pass over P1 topics: first pass was "what is it", this pass is "when do you choose it"). Case-driven via `references/case-bank.md`. Ends with first mini-mock. Prereq: P1 gate.
- `## P3 Case Drills + Mocks (2 weeks)`: whiteboard cases from case-bank (migration assessment, hybrid architecture, cost optimization, consultant pushback), Well-Architected pillars as scoring frame only; W4 full English mocks + weak-point retest. Prereq: P2 gate.
- `## Sidecar: Linux Interview Bank`: 2 sessions, interleaved during P2/P3 weeks, from `references/linux-interview-bank.md`; priority order: the two real prior misses (IRQ/softirq, static vs shared library) first.
- A one-line note: LP behavioral runs in parallel in `fsi-devops-english` starting week 1; it is not this coach's scope.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'warm-up' skills/cloud-architect-coach/references/curriculum.md && [ "$(grep -cE '^## ' skills/cloud-architect-coach/references/curriculum.md)" -ge 3 ] && ! grep -q 'TODO:' skills/cloud-architect-coach/references/curriculum.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/curriculum.md
git commit -m "cloud-architect-coach: fill curriculum hook (4-week sprint)"
```

---

### Task 4: gap-scan-aws-networking.md

**Files:**
- Create: `skills/cloud-architect-coach/references/gap-scan-aws-networking.md`

**Interfaces:**
- Consumes: phase name `P1 Networking Gap-Scan` from Task 3.
- Produces: the 16-question scan that phase-gates (Task 9) makes P1's gate.

- [ ] **Step 1: Write the file**

Header explains protocol: coach asks each question verbally; student answers without notes; scoring per question is `pass` (mechanism-level: explains why, not just names the service), `shaky` (names the right thing, cannot explain the mechanism), `hole` (stuck). `shaky` and `hole` become mini-lessons; every one is retested in a later session before P1 closes. Results recorded in the progress file per `engine/PROGRESS-SCHEMA.md`.

The 16 questions (write each with a one-line "listen for" note stating the mechanism a pass must contain):

1. Private-subnet EC2 needs to reach S3. Three ways, and when do you pick each? (listen for: NAT+IGW vs gateway endpoint vs interface endpoint; cost and policy trade-offs)
2. SG vs NACL: what does stateful/stateless mean at the packet level? (listen for: connection tracking; return traffic; cross-ref k8s foundations conntrack §3.5)
3. Connecting to a port gives Connection Refused vs Timeout: what does each imply in a VPC? (listen for: refused = RST from a live host with no listener; timeout = SG/NACL silently dropping)
4. TGW vs VPC peering: when does peering stop scaling? (listen for: no transitive routing, n-squared mesh, route-table limits)
5. Direct Connect vs site-to-site VPN: how do you choose, and why do real designs run both? (listen for: latency consistency, bandwidth, cost, VPN as DX failover)
6. What does BGP do on a DX or VPN connection? (listen for: route advertisement/propagation, path selection, why static routes stop scaling)
7. On-prem hosts need to resolve records in a Route 53 private hosted zone, and VPC workloads need to resolve on-prem names. How? (listen for: Resolver inbound + outbound endpoints, forwarding rules)
8. Inside an EC2 instance, who answers the address in /etc/resolv.conf? (listen for: VPC+2 / 169.254.169.253, Route 53 Resolver)
9. ALB vs NLB: layer, TLS termination options, source-IP preservation. (listen for: L7 vs L4, X-Forwarded-For vs proxy protocol)
10. Walk through a TLS handshake and how the certificate chain is validated. Where do you terminate TLS and why? (listen for: chain of trust to a root CA, ALB termination + ACM, re-encrypt to backend)
11. How does a VPC route table pick a route? (listen for: longest-prefix match, the local route, one table per subnet)
12. Customer's on-prem CIDR overlaps the VPC CIDR. What breaks and what are the options? (listen for: routing ambiguity, private NAT gateway, re-IP)
13. MTU: in-VPC vs over VPN/DX, and what does a blackhole look like? (listen for: 9001 vs 1500, PMTUD blocked by ICMP filtering, small packets pass while large hang)
14. What does a NAT gateway do and not do, and what are its cost/design traps? (listen for: no inbound, per-AZ placement, data-processing charges)
15. Two accounts need to share a network. Options and trade-offs? (listen for: RAM shared VPC vs TGW vs peering)
16. FSI customer requires all egress inspected and no public internet. Sketch the egress design. (listen for: no IGW, centralized egress via TGW, Network Firewall or proxy, SG egress rules)

- [ ] **Step 2: Verify**

Run: `[ "$(grep -cE '^[0-9]+\.' skills/cloud-architect-coach/references/gap-scan-aws-networking.md)" -ge 16 ] && grep -q 'listen for' skills/cloud-architect-coach/references/gap-scan-aws-networking.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/gap-scan-aws-networking.md
git commit -m "cloud-architect-coach: P1 networking gap-scan (16 questions)"
```

---

### Task 5: teaching-elements.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/teaching-elements.md`

**Interfaces:**
- Consumes: phase names from Task 3; case IDs `CASE-1`..`CASE-6` from Task 6 (referenced by name only; Task 6 defines them).

- [ ] **Step 1: Write the hook**

Replace all TODOs. Lint needs literal `step b`, `step c`, `step e` (case-insensitive). No step D (no lab-manager). Per-topic entries, each with `Scenario (Step B)`, `First-principles chain (Step C)`, `Chunks`, `Drill (Step E)`:

1. **Migration 三階段 (Assess/Mobilize/Migrate&Modernize)**. Step B scenario: CASE-1 opening (200-VM DC exit). Step C chain: migrations fail on unknowns, not on technology; the three phases exist to spend money on discovery before commitment (assess buys information, mobilize buys capability, migrate spends at scale). Chunks: discovery/TCO, business case, landing zone as mobilize artifact, wave planning. Step E drill: given a jumbled 10-item activity list, sort into the three phases and defend two placements.
2. **7R 決策邏輯**. Step B: CASE-1 workload list. Step C: each R trades migration cost against future agility; the R is chosen by workload constraints (license, coupling, roadmap, compliance), not preference. Chunks: the seven Rs with one canonical example each; decision tree (retire first, then retain, then the cost/agility ladder). Step E: 6 one-line workloads, assign an R + one-sentence reason each, in interview time.
3. **工具鏈 (MGN, DMS/SCT, DataSync/Snowball, Migration Hub)**. Step B: CASE-4 (Oracle). Step C: every tool is a data-movement problem with a consistency window; pick by data type (block/db/file) and tolerable lag. Chunks: MGN replication model, DMS CDC + SCT conversion, offline vs online transfer sizing (when Snowball beats the wire: bandwidth math). Step E: given data size + link bandwidth + downtime window, pick the transfer path and show the arithmetic.
4. **Landing zone / multi-account**. Step B: CASE-2 (FSI). Step C: account is the strongest isolation boundary AWS offers, so org design is security design; Control Tower is the paved road. Chunks: OU structure, SCP vs IAM, centralized logging/egress, IaC baseline. Step E: whiteboard an OU tree for a bank with prod/nonprod/sandbox and justify two SCPs.
5. **Hybrid connectivity + DNS(P1 內容第二輪)**. Step B: CASE-6 (latency-sensitive hybrid app). Step C: second pass rule; first pass asked what TGW/DX/Resolver are, this pass asks when: every hybrid design is bandwidth × latency-consistency × failover × cost. Chunks: DX+VPN failover design, hybrid DNS end-to-end resolution path, MTU pitfall. Step E: draw the packet path on-prem app → VPC DB including DNS resolution, then break it at one point of the student's choosing and troubleshoot.
6. **Well-Architected as scoring frame**. Step B: any completed case answer. Step C: WA is a review checklist, not an architecture; used to find what the answer forgot (usually cost or ops). Chunks: five pillars one line each; how to run a self-review pass. Step E: apply the five pillars to one's own CASE answer and find two gaps.
7. **顧問溝通(pushback)**. Step B: CASE-5 (multi-region insistence). Step C: consultants are paid to disagree with data; structure = acknowledge goal, quantify cost of the ask, offer the cheaper path to the same goal, land on customer choice (maps to LP: Have Backbone; Earn Trust). Chunks: the 4-move structure; delivering it in English. Step E: 2-minute English pushback delivery for CASE-5, scored on structure not accent.

Cross-reference block at the end: topics NOT taught here because k8s-coach foundations owns them (TCP §3, DNS internals §4, conntrack §3.5, OOM §2.4, perf triage §5), with the file path.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'step b' skills/cloud-architect-coach/references/teaching-elements.md && grep -iq 'step c' skills/cloud-architect-coach/references/teaching-elements.md && grep -iq 'step e' skills/cloud-architect-coach/references/teaching-elements.md && ! grep -q 'TODO:' skills/cloud-architect-coach/references/teaching-elements.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/teaching-elements.md
git commit -m "cloud-architect-coach: fill teaching-elements hook (7 topics)"
```

---

### Task 6: case-bank.md

**Files:**
- Create: `skills/cloud-architect-coach/references/case-bank.md`

**Interfaces:**
- Produces: case IDs `CASE-1`..`CASE-6` consumed by teaching-elements (Task 5) and phase-gates (Task 9).

- [ ] **Step 1: Write the file**

Six cases. Each entry: ID, one-paragraph customer brief (the exact text the coach reads aloud), what a hire-bar answer must contain (bullet rubric), and the standard follow-up the interviewer would push.

- `CASE-1 製造業 DC exit`: 200 VMs on VMware, data-center lease ends in 12 months, small ops team, wants "everything moved". Hire bar: 3-phase plan with discovery first, wave planning, 7R mix (mostly rehost/replatform, names retire candidates), names MGN, calls out the VMware licensing angle. Follow-up: "customer wants zero downtime for the ERP wave".
- `CASE-2 金融業 compliance`: bank moving a customer-facing app; regulator requires no public internet egress, all traffic inspected, data in-country. Hire bar: multi-account landing zone, centralized egress + inspection, DX private connectivity, hybrid DNS, audit logging. Follow-up: "auditor asks how you prove no packet left uninspected".
- `CASE-3 帳單爆炸`: lift-and-shift finished 6 months ago, bill is 3x the business case. Hire bar: structured cost review: right-sizing evidence, RI/Savings Plans, storage class audit, NAT/data-transfer traps, tagging for allocation; frames it as an ops-process fix, not one-off cuts. Follow-up: "CFO wants 40% off next quarter, what do you cut first".
- `CASE-4 Oracle 遷移`: on-prem Oracle behind a licensed appliance, team of 2 DBAs. Hire bar: SCT assessment first, replatform-to-RDS vs repurchase debate with license cost as the driver, DMS CDC cutover with rollback, downtime window negotiation. Follow-up: "CDC lag never reaches zero, cutover window is 2 hours, go or no-go?".
- `CASE-5 多region 執念`: low-traffic internal app, customer insists on multi-region active-active from day one. Hire bar: the 4-move pushback (acknowledge RTO/RPO goal, quantify active-active cost and complexity, offer backup-restore or pilot-light matched to actual RTO/RPO numbers, leave the decision with the customer). Follow-up: "customer says money is not a concern".
- `CASE-6 Hybrid 延遲敏感`: factory-floor app on-prem must call a VPC API under 20ms p99. Hire bar: DX with VPN failover, latency budget arithmetic, hybrid DNS resolution path, MTU mismatch called out proactively. Follow-up: "p99 fine for weeks, then multi-second spikes: where do you look?" (expected: failover to VPN path, or PMTUD blackhole).

- [ ] **Step 2: Verify**

Run: `[ "$(grep -c 'CASE-' skills/cloud-architect-coach/references/case-bank.md)" -ge 6 ] && grep -qi 'follow-up' skills/cloud-architect-coach/references/case-bank.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/case-bank.md
git commit -m "cloud-architect-coach: case bank (6 customer scenarios)"
```

---

### Task 7: linux-interview-bank.md

**Files:**
- Create: `skills/cloud-architect-coach/references/linux-interview-bank.md`

- [ ] **Step 1: Write the file**

Header states purpose (insurance against resume thread-pulls; 2 sessions, interleaved in P2/P3) and the answer format: every question is answered in three layers: (1) command-level answer, (2) mechanism one layer down, (3) a hands-on verify command. Questions whose mechanism layer is already written in k8s-coach foundations link there instead of restating.

`## Priority 0: 上次真實失分題` (retested twice, spaced, per spec):
- IRQ / hardirq / softirq: what they are; softirq as the network-packet processing context; bridge to conntrack material the student already knows (k8s foundations §3.5). Verify: `cat /proc/softirqs`, `cat /proc/interrupts | head`.
- Static vs shared library: link-time copy vs load-time resolution; `ldd`, `LD_LIBRARY_PATH`, glibc-vs-musl as the practical DevOps encounter (alpine images). Verify: `ldd /bin/ls`.

`## Core 20 (CA framing)` — the twenty questions, grouped:

A. EC2 系統管理: 1. EC2 won't boot: console output/screenshot, rescue instance; underlying chain firmware → bootloader → kernel → init/systemd. 2. cloud-init and user-data timing. 3. EBS grown but df unchanged: growpart then resize2fs/xfs_growfs. 4. df vs du mismatch: deleted-but-open files (`lsof +L1`), inode exhaustion variant. 5. Service autostart + restart-on-crash: systemd unit, `Restart=`, journalctl. 6. SIGTERM vs SIGKILL and graceful shutdown (ASG lifecycle hooks, ALB deregistration delay). 7. High-concurrency tuning: nofile/ulimit, somaxconn, sysctl read/write. 8. EC2 time sync: chrony, 169.254.169.123, clock-drift consequences. 9. IMDS and why IMDSv2 (SSRF).

B. 效能與排查: 10. High load average with low CPU: iowait; t-series CPU credits. 11. free -h buff/cache is not a leak (page cache). 12. OOM killer, leak detection, mitigation (link k8s foundations §2.4 for cgroup OOM; add single-host view: free, smaps, oom_score). 13. strace vs lsof vs tcpdump: which layer each observes.

C. 網路(單機接雲層): 14. Connection Refused vs Timeout, mapped to OS (RST, no listener) and cloud (SG silent drop). 15. SG vs NACL statefulness = conntrack (link k8s foundations §3.5). 16. TCP 3-way handshake + TCP vs UDP with when-to-choose (link k8s foundations §3). 17. Routing: `ip route` on the host, then the VPC route table layer above it. 18. DNS resolution path + who answers in a VPC (link k8s foundations §4 for the general path). 19. TLS handshake and cert-chain validation. 20. MTU 9001 vs 1500, PMTUD blackhole symptoms.

`## Appendix: Support-loop 逐字稿原題(降權)` — questions from the author's real AWS Support interview kept for coverage, listed as prompts only (answered via the Core 20 or k8s foundations where they overlap): kernel/shell version check; chmod and 755 meaning; why `-R` on directories; /etc/hosts; fstab automount fields; LVM concept, benefits, extend flow; reading df -h; resize without deletion; sysctl view/modify (TCP memory, open-file limits); full boot sequence to login; why BIOS hands to GRUB and GRUB's job; TCP vs UDP; 3-way handshake and timeout behavior; route/netstat for routing table; ping-triggered DNS path, resolv.conf, how 8.8.8.8 works; OOM killer causes and mitigations; which logs after a crash (/var/log/messages, syslog) and journalctl usage; Connection Refused mechanism on a down service.

- [ ] **Step 2: Verify**

Run: `grep -q 'Priority 0' skills/cloud-architect-coach/references/linux-interview-bank.md && [ "$(grep -cE '^[0-9]+\.| [0-9]+\.' skills/cloud-architect-coach/references/linux-interview-bank.md)" -ge 20 ] && grep -q 'foundations-linux-network' skills/cloud-architect-coach/references/linux-interview-bank.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/linux-interview-bank.md
git commit -m "cloud-architect-coach: linux interview bank (P0 misses + core 20 + appendix)"
```

---

### Task 8: scorecard-dims.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/scorecard-dims.md`

- [ ] **Step 1: Write the hook**

Replace all TODOs. Needs literal `primary` and `tier 1`. Engine owns the 60% threshold; do not restate it as a rule, only reference it.

- `## Primary (always-on)`: does the student justify a recommendation with a trade-off tied to the customer's stated constraint, instead of naming a service? ("用 TGW" fails; "peering 到第三個 VPC 就失去 transitive routing,所以用 TGW" passes.)
- `## Tier 1 (P0-P1)`: mechanism accuracy: networking answers explain behavior at packet/DNS/TLS level, matching the gap-scan "listen for" lines.
- `## Tier 2 (P2)`: migration judgment: right R with a workload-specific reason; risk (downtime, data consistency, rollback) named without prompting.
- `## Tier 3 (P3)`: consultant delivery: answer has a stated structure, English is clear enough for a customer call, pushback uses the 4-move shape, and a WA self-review pass finds its own gaps.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'primary' skills/cloud-architect-coach/references/scorecard-dims.md && grep -iq 'tier 1' skills/cloud-architect-coach/references/scorecard-dims.md && ! grep -q 'TODO:' skills/cloud-architect-coach/references/scorecard-dims.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/scorecard-dims.md
git commit -m "cloud-architect-coach: fill scorecard-dims hook"
```

---

### Task 9: phase-gates.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/phase-gates.md`

**Interfaces:**
- Consumes: phase names (Task 3), gap-scan protocol (Task 4), CASE IDs (Task 6).

- [ ] **Step 1: Write the hook**

Replace all TODOs. Needs literal `gate` and >= 1 `## ` subsection. One `## <phase> Gate` per phase:

- P0 gate: thread-pull list exists in the progress file and the student can state the loop shape (phone screen vs full loop, LP weight) unprompted.
- P1 gate (spec success criterion, verbatim): gap-scan completed; every `shaky`/`hole` either closed and retested in a later session, or explicitly parked with a written reason.
- P2 gate: an unseen mini-case (coach varies; not CASE-1..6) answered with a 3-phase plan and per-workload 7R with reasons, at tier-2 scorecard pass.
- P3 gate (spec success criterion): two full English mocks at hire bar on the coach's scorecard, one migration case and one hybrid-networking case, drawn from or modeled on CASE-1..6 with numbers changed.
- Sidecar gate: all Priority-0 and Core-20 questions answerable at the mechanism layer; the two Priority-0 questions retested twice, spaced.

- [ ] **Step 2: Verify markers**

Run: `grep -iq 'gate' skills/cloud-architect-coach/references/phase-gates.md && [ "$(grep -cE '^## ' skills/cloud-architect-coach/references/phase-gates.md)" -ge 1 ] && ! grep -q 'TODO:' skills/cloud-architect-coach/references/phase-gates.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/phase-gates.md
git commit -m "cloud-architect-coach: fill phase-gates hook"
```

---

### Task 10: portfolio.md + workspace directory

**Files:**
- Modify: `skills/cloud-architect-coach/references/portfolio.md`
- Create: `workspaces/ca/.gitkeep`

- [ ] **Step 1: Write the hook**

Replace all TODOs. Needs literal `workspace` and `artifact`. Follow the sd-coach convention (repo-internal workspace, not `~/`):

- Workspace directory: `${CLAUDE_SKILL_DIR}/../../workspaces/ca/`. Holds `progress.md` (engine-owned schema per `engine/PROGRESS-SCHEMA.md`; do not redefine), the gap-scan record, the thread-pull list, and mock scorecards.
- Artifact section: what clears the bar and is kept: written case answers after mock review, the final pre-interview one-page crib (thread-pull list + parked holes + weak-point retest log).

- [ ] **Step 2: Create the workspace dir**

```bash
touch workspaces/ca/.gitkeep 2>/dev/null || { mkdir workspaces/ca && touch workspaces/ca/.gitkeep; }
```

- [ ] **Step 3: Verify markers**

Run: `grep -iq 'workspace' skills/cloud-architect-coach/references/portfolio.md && grep -iq 'artifact' skills/cloud-architect-coach/references/portfolio.md && [ -f workspaces/ca/.gitkeep ] && ! grep -q 'TODO:' skills/cloud-architect-coach/references/portfolio.md && echo OK`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add skills/cloud-architect-coach/references/portfolio.md workspaces/ca/.gitkeep
git commit -m "cloud-architect-coach: fill portfolio hook + workspaces/ca"
```

---

### Task 11: language.md

**Files:**
- Modify: `skills/cloud-architect-coach/references/language.md`

- [ ] **Step 1: Write the hook**

Replace all TODOs. Content:

- Default: teaching discussion in Traditional Chinese; AWS/domain terms stay in English inline (TGW, landing zone, 7R).
- Ramp (tied to the 4 weeks): W1-W2 zh discussion; W3 case answers attempted in English with zh follow-up allowed; W4 mocks entirely in English, including clarifying questions.
- English Polish rule (same as sd-coach): when the student attempts English, correct by restating the natural interview-ready version in one line; never stop for a grammar lesson.

- [ ] **Step 2: Verify**

Run: `! grep -q 'TODO:' skills/cloud-architect-coach/references/language.md && grep -qi 'ramp' skills/cloud-architect-coach/references/language.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add skills/cloud-architect-coach/references/language.md
git commit -m "cloud-architect-coach: fill language hook (zh teaching, W4 English mocks)"
```

---

### Task 12: Evals, full lint, plugin wiring

**Files:**
- Create: `skills/cloud-architect-coach/evals/evals.json`
- Create: `skills/cloud-architect-coach/evals/description-triggering.md`
- Create: `skills/cloud-architect-coach/evals/files/progress-p1-entry.md`
- Modify: `.claude-plugin/plugin.json` (description), `README.md` (live-coach list and tree)

- [ ] **Step 1: Write description-triggering.md**

Follow `skills/sd-coach/evals/description-triggering.md` format: quote the SKILL.md description, then lists. Should trigger: "幫我準備 AWS ProServe Cloud Architect 的面試"; "練一個 migration case:客戶要把 200 台 VM 搬上 AWS"; "考我 linux interview bank"; "7R 是什麼?幫我複習遷移策略"; "mock 一場 hybrid networking 的架構面試". Should NOT trigger: "幫我修這個 k8s Pod CrashLoopBackOff" (k8s-coach); "教我 consistent hashing" (sd-coach); "幫公司規劃真實的上雲專案" (real engineering task, not練習); "想練 DevOps 英文口說" (fsi-devops-english); "寫一個 Terraform module 建 VPC" (execution task).

- [ ] **Step 2: Write evals.json**

sd-coach format (`skill_name`, `_note`, `evals` array). Two behavioral evals:

```json
{
  "skill_name": "cloud-architect-coach",
  "_note": "Behavioral evals. Each tests the FIRST coaching turn given a learner's opening message. Coach runs on the shared engine; progress in workspaces/ca/.",
  "evals": [
    {
      "id": 1,
      "name": "gap-scan-tests-not-trusts",
      "prompt": "AWS networking 我很熟,VPC TGW DX 都用過,P1 可以直接跳過吧,我們直接開始 migration。",
      "expected_output": "不直接放行。依 P1 規則「熟要用測的」:開始 gap-scan 快問快答(從 references/gap-scan-aws-networking.md 抽題),說明 mechanism-level 答對就快速通過、卡住的點才補課。不因學生自評就跳過 gate,也不倒出完整教材。",
      "files": ["evals/files/progress-p1-entry.md"],
      "expectations": []
    },
    {
      "id": 2,
      "name": "case-first-not-lecture",
      "prompt": "今天想練 migration,教我 7R。",
      "expected_output": "不從名詞定義開講。依 teaching-elements 的 case-driven 原則:先丟 CASE-1(200 VM DC exit)場景讓學生試答 workload 分類,再從學生的答案帶出 7R 決策邏輯。Step B 場景先於 Step C 原理。",
      "files": ["evals/files/progress-p1-entry.md"],
      "expectations": []
    }
  ]
}
```

- [ ] **Step 3: Write the eval fixture**

`evals/files/progress-p1-entry.md`: a minimal progress file per `engine/PROGRESS-SCHEMA.md` showing P0 complete (thread-pull list recorded) and P1 not started. Copy the field structure from `skills/sd-coach/evals/files/progress-p1.md`, replace domain content with: student = DevOps engineer, target = ProServe CA loop ~4 weeks out, P0 done 2026-07-21.

- [ ] **Step 4: Update plugin.json and README**

`.claude-plugin/plugin.json` description: replace the domains sentence with "Domains: Terraform/IaC, Kubernetes/SRE, system design interviews, LeetCode coding interviews, and AWS ProServe Cloud Architect interview prep." `README.md`: add cloud-architect-coach to the live-coaches sentence and a tree entry mirroring the other coaches (SKILL.md, references incl. gap-scan/case-bank/linux-interview-bank, evals, no scripts).

- [ ] **Step 5: Full lint**

Run: `./scripts/lint-coach.sh cloud-architect-coach && ./scripts/lint-all.sh && echo ALL-GREEN`
Expected: `ALL-GREEN`. If lint fails, fix the named file; do not weaken the linter.

- [ ] **Step 6: Commit**

```bash
git add skills/cloud-architect-coach/evals/ .claude-plugin/plugin.json README.md
git commit -m "cloud-architect-coach: evals + plugin wiring, full lint green"
```

---

## Execution Notes

- Tasks 2-11 are independent of each other except where Interfaces say otherwise (3 → 4/5/9 phase names; 6 → 5/9 CASE IDs). Safe order: 1, 2, 3, 4, 6, 5, 7, 8, 9, 10, 11, 12.
- The spec's "Success Criteria" section is a study outcome, not a build outcome; the build is done at Task 12. First session afterward starts at Warm-Up Diagnostic.
