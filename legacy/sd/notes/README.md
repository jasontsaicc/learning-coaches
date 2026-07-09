# System Design Notes

Structured system design study with hands-on PoC projects — from a DevOps engineer's perspective.

Each topic includes concept notes, trade-off analysis, and working code.

## Roadmap (61 days + 5 prep)

| Phase | Topic | Days | Focus |
|-------|-------|------|-------|
| **-1** | Go Refresher | 5 prep days | Types, concurrency, HTTP server, testing, Docker |
| **0** | Thinking Framework | Day 1-3 | Interview rubric, estimation, 4-step answer framework |
| **1** | Building Blocks | Day 4-16 | LB, caching, DB, message queue, API, consistent hashing |
| **2** | Distributed Systems | Day 17-26 | CAP, consistency, replication, rate limiting, observability |
| **3** | Applied Problems | Day 27-53 | 8 Tier-1 + 4 Tier-2 system design problems |
| **4** | Mock Interviews | Day 54-61 | Trade-off drills, timed mocks, weak spot reinforcement |

## Concept Coverage (Tier 1 Problems)

```
                        URL  ID  Rate Noti Chat Feed Cache Pay
Hashing/Encoding         ●        ●                    ●
Database Sharding        ●   ●                  ●            ●
Caching                  ●                      ●      ●
Message Queue                         ●        ●  ●        ●
WebSocket/Real-time                        ●
Fan-out Strategies                             ●  ●
Consistent Hashing                                    ●
Idempotency                  ●   ●                          ●
Distributed Locking              ●                          ●
Async Processing                      ●        ●           ●
```

8 problems → 90% of core SD concepts. Each concept reinforced by 2-3 problems.

## DevOps Differentiator

Topics where production DevOps experience adds real depth to SD answers:

| Topic | DevOps Angle |
|-------|-------------|
| Load Balancer | ALB/NLB selection, target group health checks |
| Caching | ElastiCache operational concerns, eviction tuning |
| Message Queue | SQS FIFO vs Standard, DLQ monitoring |
| Observability | Prometheus/Grafana/ELK, SLO-based alerting |
| Any system | Multi-AZ, DR, blue-green deployment |

## Structure

```
notes/      # Concept notes with trade-off analysis (English + 繁中)
projects/   # Working PoC code (Go + Docker)
docs/       # Curriculum roadmap and planning review
```

## Tech Stack

Go, Docker, Nginx, Redis

## Detailed Planning

- [Curriculum Roadmap](docs/curriculum-roadmap.md) — full daily tracker and dependency map
- [Planning Review](docs/planning-review.md) — design decisions, tier system rationale, and iteration history
