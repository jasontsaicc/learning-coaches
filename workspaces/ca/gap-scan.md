# P1 Networking Gap-Scan Record

Protocol: 16 questions, oral, no notes. pass = mechanism level; shaky/hole = mini-lesson
on the spot + retest in a later session. P1 does not close until all retests pass.

## Round 1 (2026-07-19, session 2)

| # | Question | Result | Gap noted |
|---|----------|--------|-----------|
| 1 | S3 from private subnet, 3 options | shaky | named gateway endpoint + NAT; said "peering" instead of interface endpoint; no cost/policy tradeoffs. Mini-lesson given (gateway = route entry, interface = ENI, hybrid reach, NAT cost). RETEST |
| 2 | SG vs NACL, stateful/stateless | shaky | placement + behavior correct; missing conntrack mechanism ("how does SG recognize return traffic"). Mini-lesson given (connection table / 5-tuple; NACL ephemeral-port classic miss). RETEST |
| 3 | refused vs timeout | hole | direction inverted: thought refused = blocked. Corrected: refused = RST from live host w/o listener (fast, app layer); timeout = silent drop by SG/NACL or no route (slow, network layer). Links Linux bank #14. RETEST |
| 4 | TGW vs peering scale | pass | nailed non-transitivity with example; complements given: n(n-1)/2 mesh count, route-table limits, TGW attachment+GB cost |
| 5 | DX vs VPN | shaky | named both + cost; missed "consistent latency is the product" and entirely missed why-both (VPN as DX failover). Mini-lesson given. RETEST |
| 6 | BGP on DX/VPN | hole | honest "not familiar". Mini-lesson: prefix advertisement, DX-preferred path, session drop → route withdrawal → auto failover to VPN; static routes fail on topology change. RETEST |
| 7 | hybrid DNS resolver endpoints | hole | knew "configure DNS" direction only. Mini-lesson: inbound endpoint (on-prem→VPC private zone) + outbound endpoint + forwarding rules (VPC→on-prem); "inbound = others ask us". RETEST |
| 8 | who answers resolv.conf in EC2 | shaky | said "AWS" — vendor not mechanism. Mini-lesson: VPC+2 (.2 resolver), Route 53 Resolver, private zone + public recursion, only reachable in-VPC. RETEST |
| 9 | ALB vs NLB | shaky | L7/L4 correct; confused NLB static IP (LB's own addr) with source-IP preservation; didn't know XFF / NLB default preserve / proxy protocol v2. Mini-lesson given. RETEST |
| 10 | TLS handshake + cert chain | hole | asked to be walked through. Mini-lesson: ClientHello/SNI → cert chain → validation to local root trust store (+SAN/expiry/revocation, missing-intermediate & clock-drift traps) → ECDHE; terminate at ALB w/ ACM, re-encrypt for FSI. RETEST |
| 11 | route table selection | shaky | guessed "smallest range wins" (right instinct) but couldn't name longest-prefix match; got association backwards (said subnet can bind multiple tables — it's exactly one). Mini-lesson given incl. local route. RETEST |
| 12 | overlapping CIDR | shaky | identified ambiguity + peering rejection; no solutions. Mini-lesson: re-IP / private NAT gateway / PrivateLink, IPAM as day-one landing-zone task. RETEST |
| 13 | MTU / PMTUD blackhole | hole | knew MTU=packet size, 1500 only. Mini-lesson: 9001 vs 1500, DF bit + ICMP frag-needed dropped → blackhole; signature "small packets fine, big packets hang"; fix ICMP 3/4 or MSS clamp. Links CASE-6 + linux bank #20. RETEST |
| 14 | NAT gateway does/doesn't | shaky | behavior right (out yes, in no, 0.0.0.0/0 route); placement wrong (said private subnet — it lives in public); missing stateful-translation why, per-GB cost trap, per-AZ design. Mini-lesson given. RETEST |
| 15 | share network across accounts | shaky | peering + TGW named; missed RAM shared VPC (the literal "same network" option) + tradeoffs. Mini-lesson given. RETEST |
| 16 | FSI inspected egress design | shaky | core instinct right (0.0.0.0/0 → firewall) but no assembled design. Mini-lesson: no-IGW structural guarantee, TGW → inspection VPC → NFW, DX egress + VPC endpoints (no public net), logs to log-archive, prove-by-absence for auditor. RETEST |

## Round 1 summary
- 1 pass (Q4), 10 shaky, 5 hole (Q3, 6, 7, 10, 13). All 15 retest before P1 closes.
- Pattern: service-name layer present, mechanism layer systematically missing.
- Inversions to kill first: Q3 refused=blocked (backwards), Q11 subnet binds many tables (backwards), Q14 NAT in private subnet (wrong placement).
- Hybrid cluster (Q6 BGP, Q7 resolver endpoints, Q13 MTU) all down — P2 second pass hits these; also the Outposts resume line depends on them.
