# Day 27 Drill — Mind Map (hand-copy)

## Bloom + Cache

```
                  ┌─ FLOW ────────→ Bloom → Cache → DB
                  │                  guards: missing key / hot key / truth
                  │
                  ├─ cache CAN'T ──→ stores only real keys
  BLOOM +         │   block          missing key → always miss → hits DB
  CACHE  ─────────┤
  (center)        ├─ bloom CAN ────→ says "definitely no" → reject
                  │   block          no false negative → real key never killed
                  │                  bit: insert sets 1, never cleared
                  │
                  └─ 3 cache ──────→ penetration → Bloom
                      fails          stampede   → lock / coalescing
                                     avalanche  → random TTL
```

One line: cache only stores what exists, so only Bloom can block keys that don't.

## URL Shortener

```
                 ┌─ SIZE ──→ 100M/mo → 6B in 5yr
                 │            62 ~ 2^6 → 6 chars = 64B (enough)
                 │
                 ├─ GEN ───→ counter + base62 (not hash)
                 │            no collision, no dedup
                 │
  URL            ├─ STORE ─→ NoSQL KV (no join / txn)
  SHORTENER ─────┤            truth = durable DB, Redis = cache only
  (center)       │
                 ├─ READ ──→ DNS → LB → API → Bloom → Cache → DB
                 │            miss: DB hit → fill cache / none → 404
                 │
                 └─ SCALE ─→ KGS range (allocator: once per block)
                              generator dies → lost block = gaps = OK
                              monitor: hit rate / P99 / Bloom FP
```

One line: read-heavy KV, codes from counter+base62, Bloom guards penetration.

> HTTP: 401 = no login | 403 = no permission | 404 = not found (bad code)
```
