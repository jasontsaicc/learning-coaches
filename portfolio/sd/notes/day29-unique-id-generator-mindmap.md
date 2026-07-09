# Day 29 Mind Map — Unique ID Generator (Snowflake)

> Hand-copy onto paper in 2-3 min. Cover a branch → recall it → check.

```
                ┌─ LAYOUT ───→ 64-bit: 1 sign | 41 time | 5 dc | 5 worker | 12 seq
                │              time=order, machine=no clash, seq=same-ms counter
                │
                ├─ WHY ──────→ machineID → cross-node unique
                │              + seq → same node, same ms unique
                │              + timestamp → reboot resets seq, time always fwd
                │              + time in HIGH bits → sort by number = sort by time
  UNIQUE ID  ───┤
  (Snowflake)   ├─ CLOCK SKEW → NTP / leap sec / VM pause pulls clock BACK
  (center)      │  (#1 trap)    → re-enter old ms → seq resets → DUPLICATE ID
                │              fix: store lastTs; if now < last → REFUSE or wait
                │              rule: refuse > risk a duplicate
                │
                ├─ MACHINE ID → who assigns it? coordinate ONCE at boot
                │              ZK / etcd / K8s StatefulSet / config
                │              run-time = zero coordination
                │
                ├─ ROUTES ───→ UUID: random, no sort, bad DB index
                │              DB auto-inc: perfect sort BUT SPOF + bottleneck
                │              KGS: central, can be SHORT, no time info
                │              Snowflake: local calc, sortable, ~4M/s
                │
                └─ CAPACITY ─→ 12 bits = 4096/ms → ~4M/sec/node
                               need 100k/s = 40x. multi-node = HA, not QPS
```

One line: Pack time + machine + seq into 64 bits → globally unique, roughly time-sortable, no per-ID coordination.
