# S40 Mind Map — Distributed Rate Limiter (hand-write practice)

```
                                    ┌─ local counter → 100×50 = 5000/min (BROKEN)
                                    │
                    ┌─ COUNT ───────┼─ shared Redis = one source of truth
                    │               │     cost: network hop + critical dep
                    │               └─ 500K / 100K = 5 shards, by user_id
                    │
DISTRIBUTED ────────┤
RATE LIMITER        │               ┌─ HARD part = concurrency, NOT counting
                    │               │
                    ├─ ATOMICITY ───┼─ counter 99, 2 reqs read 99 → both pass → oversell
                    │               │
                    │               ├─ simple count → INCR (single cmd, atomic)
                    │               └─ multi-step (sliding window) → Lua (bundle)
                    │
                    ├─ CLARIFY ─────── reject 429 (not queue) / approx OK / fail-OPEN
                    │
                    └─ 3AM PAGE ────── Redis down / reject spike / Redis P99
```

## Review refreshers (one line each)

```
Bloom      ── FP = waste 1 lookup (OK) / FN = lose real data (disaster)
           ── 1 Bloom PER SSTable → skip DISK read (not "DB")

CB states  ── Closed = flow (normal) / Open = tripped (fail fast) / Half-Open = probe few

Cons.Hash  ── %N change → 99% remap → DB avalanche
           ── ring = move 1/N  |  vnode = even load  (TWO axes)

LB         ── sticky (state IN server) vs Redis (state OUT) = opposite
           ── busy/idle uneven → Least Connections (not latency)
```

## The one habit to fix

```
FIRST SENTENCE = naked conclusion  ❌
   "use Redis, cost is low"
→ say WHY (mechanism) + COST (specific thing that bites you), unprompted, first try
```
