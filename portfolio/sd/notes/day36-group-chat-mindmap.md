# Day 36 Group Chat — mind map

```
                 ┌─ COUNT ──→ per-user 500 / per-server 50 / per-group 1
                 │
                 ├─ TABLES ─→ group_members (DB) + connection map (Redis)
  GROUP FAN-OUT ─┤
  (center)       ├─ 100K ───→ 100k × 5/s = 500k lookups/s → boom
                 │
                 ├─ FLIP ───→ server SUBSCRIBE group:<id> → PUBLISH × 1
                 │
                 └─ COST ───→ member lookup moves to connect time (cache)
```

One line: store once per group, servers subscribe to groups, sender publishes once.
