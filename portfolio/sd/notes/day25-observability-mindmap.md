# Day 25 — Observability (Mind Map)

> Hand-copy in 2-3 min. Drill the 3 pillars by the QUESTION each answers, not the definition.

```
              ┌─ METRICS ─→ "how much? which service is sick?"
              │             numbers, RADAR → fires the alert
              │
              ├─ TRACES ──→ "where? which hop is slow?"
              │             follow ONE request across services
  OBSERV.  ───┤
  (center)    ├─ LOGS ────→ "what happened? WHY?"
              │             hunt the error line = ROOT CAUSE
              │             (e.g. "gateway timeout 7000ms")
              │
              ├─ FLOW ────→ Metrics(alarm) → Traces(locate hop) → Logs(why)
              │
              └─ GLUE ────→ trace-id ties all 3 into ONE timeline
                            (30 services' logs = haystack → filter by id)
```

One line: **Metrics = WHERE · Traces = WHICH HOP · Logs = WHY**, stitched by trace-id.

KEY trap: **CPU normal + still slow = WAITING, not computing.**
Per-machine view lies (same shape as rate-limiter N×limit blind spot).
