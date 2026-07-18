# cloud-architect-coach Design

- Date: 2026-07-18
- Status: approved in brainstorming, pending spec review
- Author: Jason (with Claude)
- Related: `engine/ENGINE.md`, `engine/PLUGIN-INTERFACE.md`, `scripts/new-coach.sh`, `skills/k8s-coach/references/foundations-linux-network.md` (Linux/network material this coach links to instead of duplicating), `fsi-devops-english` (owns LP behavioral practice)

## Context and Goal

Started as "should I build Linux and network courses?". Brainstorming redirected: the target is the AWS ProServe Delivery Consultant - Cloud Architect (Taiwan) loop, applying within days, interview window ~4 weeks. That loop tests architecture cases, migration methodology, VPC/hybrid networking, and Leadership Principles; it does not test kernel internals. Deep Linux/network material already lives in k8s-coach's foundations file. The gap is the layer between "TCP state machine" and "k8s Service": cloud networking, migration delivery, and consultant-style case communication.

Goal: pass the ProServe CA loop. Win condition: given an unseen migration or hybrid-architecture case, deliver a structured answer (assess/mobilize/migrate, 7R judgment with reasons, hybrid networking design, Well-Architected trade-offs), and survive resume thread-pulls into Linux/EC2 depth.

## Locked Decisions (from brainstorming)

1. **One sprint coach, not standalone linux/network courses.** Standalone courses duplicate k8s-coach foundations and miss this loop's rubric. Deferred, not rejected: if a later target is SRE deep-dive (Google SRE / Meta PE), revisit; the Linux bank below is the seed.
2. **`linux-interview-bank` rides inside this coach.** Insurance against resume thread-pulls (author's prior AWS Support loop went kernel-deep). ~20 questions calibrated to CA framing (EC2 scenarios), plus a de-weighted appendix of the author's real Support-loop transcript questions (LVM detail, GRUB, static vs shared library, IRQ). The two actual miss points from that transcript (IRQ/softirq, library linking) go first. Question format is three layers: command-level answer → mechanism one layer down → hands-on verify. Topics already covered in k8s-coach foundations (TCP, DNS, OOM, conntrack) are linked, not rewritten.
3. **Phase 1 (AWS networking) is a gap-scan, not a course.** Author self-assesses as familiar; the engine rule is "familiar" gets tested, not trusted. One session, 15-20 rapid questions (VPC routing, SG vs NACL statefulness, TGW vs peering, DX vs VPN, hybrid DNS / Route 53 Resolver, TLS/LB layering). Mechanism-level answer → skip; stuck → hole becomes a mini-lesson. No labs.
4. **LP behavioral is delegated to `fsi-devops-english`**, starting week 1: phone screen (LP + light technical) arrives before the full loop, so behavioral cannot wait for the technical phases.
5. **4-week sprint timeline** (application submitted within days; Amazon typical cadence: recruiter contact 1-2 weeks, phone screen, then loop 1-2 weeks later). If the phone screen lands early, mocks move forward.
6. **Lab strategy: minimal.** No new lab scripts. Free-tier VPC/DNS hands-on only if a gap-scan hole needs it; expensive/impossible resources (TGW, DX) are taught via packet-path walkthroughs on the whiteboard.

## Curriculum (4 weeks)

| Week | Content |
|---|---|
| W1 | Phase 0: loop anatomy + resume thread-pull list (1 session). Phase 1 gap-scan (1-2 sessions). LP story bank starts in fsi-devops-english. |
| W2 | Phase 2: migration core: 3 phases (Assess/Mobilize/Migrate&Modernize), 7R with decision logic, tool chain (MGN, DMS/SCT, DataSync/Snowball, Migration Hub), landing zone (Control Tower, multi-account), hybrid connectivity + DNS. Case-driven: every concept hangs on a customer scenario. First mini-mock end of week. |
| W3 | Phase 3: case drills: migration assessment, hybrid architecture, cost optimization, consultant pushback ("customer insists on X, X is wrong"). Well-Architected pillars used as scoring frame, not as material to memorize. Linux bank session 1. |
| W4 | Full mocks in English, weekly review, weak-point retest, Linux bank session 2. |

Deliberate spaced repetition: networking concepts from the W1 gap-scan reappear inside W2-W3 migration cases; first pass is "what is it", second pass is "when do you choose it". Seniority is scored on the second pass.

## Engine Integration

- Scaffold with `scripts/new-coach.sh`; fill hooks per `engine/PLUGIN-INTERFACE.md`; progress file follows `engine/PROGRESS-SCHEMA.md`.
- Reference files: north-star, curriculum (the table above expanded), case-bank (customer scenarios for W2-W3), linux-interview-bank, plus the standard engine hooks.
- Evals: reuse the behavioral eval pattern from k8s/sd coaches; minimum one eval asserting the gap-scan tests instead of trusting "I know this".

## Out of Scope

- Standalone linux-coach / network-coach (deferred; see Locked Decision 1).
- Kernel-internals depth beyond the bank (syscalls, scheduler, page cache).
- New lab automation scripts.
- Resume/application coaching (application ships before the coach does).

## Success Criteria

- Gap-scan completed; every hole either closed and retested, or explicitly parked with a reason.
- Two full English mocks passed at "hire" bar per the coach's own scorecard, including one migration case and one hybrid-networking case.
- Linux bank: all ~20 core questions answerable at mechanism layer; IRQ and library questions (prior real misses) retested twice, spaced.
- LP story bank in fsi-devops-english covers the standard question set with STAR-format English delivery.
