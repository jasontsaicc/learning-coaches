# Day 31 Mind Map — Distributed Rate Limiter

> Hand-copy onto paper in 2-3 min. Cover a branch → recall it → check.

```
                 ┌─ PROBLEM ──→ 1 limiter copied to 100 nodes = 100 islands
                 │              each counts alone → user gets N x limit (100x100=10k)
                 │
                 ├─ FIX ──────→ don't share NOTHING, share the COUNTER (Redis)
                 │              (share counter, NOT one limiter machine = SPOF)
                 │
  DISTRIBUTED ───┤
  RATE LIMITER   ├─ RACE ─────→ 2 steps "GET then INCR" = gap = oversell
  (center)       │  (the trap)   2 nodes read same stale 99 → both pass → over
                 │              cure: make check+change ATOMIC
                 │
                 ├─ ATOMIC ───→ single op: DECR (Redis single-thread, no gap)
                 │              multi-step: LUA script = run whole script as ONE cmd
                 │
                 ├─ RESET ────→ don't refill by hand → let key EXPIRE (TTL)
                 │              key = "user:minute" + EXPIRE 60s = Fixed Window
                 │              passive expiry > active cleanup job
                 │
                 └─ WINDOW ───→ Fixed: resets on the clock → 2x burst at boundary
                                (12:00:59 x100 + 12:01:00 x100 = 200 in 1 sec)
                                Sliding: look back 60s from NOW → no boundary to game
```

One line: Share the counter in Redis, make check+update atomic (DECR / Lua), and use a sliding window so the boundary can't be gamed.
