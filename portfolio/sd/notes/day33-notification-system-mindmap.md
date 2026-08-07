# Day 33 Notification System (mind map)

```
                    ┌─ CLARIFY ──→ ask only what CHANGES the design
                    │              └─ latency per type: 60s / minutes / none
                    │              └─ volume + peak, delivery guarantee, TTL
                    │
                    ├─ DRAW ─────→ L0 sync direct → provider owns your latency
                    │              L1 add queue  → API returns 202, decouple
                    │              L2 one → three → each type its own pool
                    │
  NOTIFICATION   ───┤
  SYSTEM            ├─ WHY 3 ────→ 2M mktg / 1000 per s = 33 min vs fraud 60s SLO
  (center)          │              priority = ORDER only, not CAPACITY
                    │              bulkhead = who dies / breaker = how long
                    │
                    ├─ NUMBERS ──→ N = lambda x W  (300/s x 0.2s = 60 workers)
                    │              timeout 10s x 3 retry = worker pinned 36s
                    │              130 / 36 = 3.6 free per s  vs  300/s needed
                    │
                    ├─ FAIL ─────→ provider degrades → BOTH designs die
                    │              bottleneck is downstream → circuit breaker to B
                    │              at-least-once → dedupe BEFORE the send
                    │
                    └─ 3AM ──────→ page: fraud queue age > 30s
                                   page: dead man's switch (throughput = 0)
                                   ticket: mktg backlog, template error rate
```

**One line:** Priority solves ordering, not isolation, and the provider is the real bottleneck.
