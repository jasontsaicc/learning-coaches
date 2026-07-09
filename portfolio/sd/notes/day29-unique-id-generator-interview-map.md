# Day 29 Interview Map — Unique ID Generator (Snowflake)

> Walk it TOP → BOTTOM while answering. This is the talking order, not a topic list.

```
                ┌─ 1. CLARIFY ──→ how many IDs/sec? (~100k/s)
                │   (ask FIRST,    unique + sortable? length limit?
                │    don't jump)   scope: internal ID, NOT short code
                │
                ├─ 2. HIGH-LVL ─→ propose Snowflake, 64-bit
                │                 1 sign | 41 time | 5 dc | 5 worker | 12 seq
  "Design a     │                 time=order, machine=no clash, seq=per-ms
   Unique ID  ──┤
   Generator"   ├─ 3. DEEP DIVE → WHY NOT others (say this BEFORE concluding):
   (center)     │                  UUID → unsortable, bad B-tree index
                │                  DB auto-inc → SPOF + bottleneck @ high QPS
                │                 ∴ Snowflake = unique + sortable + local
                │                 RISK clock skew: back → seq resets → DUP
                │                  → on now<lastTs: REFUSE (refuse > duplicate)
                │                 machineID: ZK/etcd, coordinate ONCE @ boot
                │
                └─ 4. SCALE/OPS → capacity: 4M/s/node → 100k = 40x, easy
                                  multi-node = HA + geo, NOT for QPS
                                  MONITOR: clock-skew alert + QPS + seq saturation
                                  security: leaks time → encrypt if client-facing
```

Opening line: "Globally unique IDs without coordinating on every ID — I'd use Snowflake: a 64-bit timestamp + machineID + sequence. Time in the high bits makes it roughly sortable; machineID + sequence kill collisions."
