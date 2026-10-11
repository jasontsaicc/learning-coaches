# Day 35 Chat System — mind map

```
1v1 bank chat
├─ connect: WebSocket (Upgrade → 101), client dials out
│   └─ drain → thundering herd → jitter + backoff, dereg delay
├─ storage axis: DB = source of truth (commit before ack)
│   ├─ order: per-conversation seq, atomic increment, row lock
│   └─ catch-up: last_msg_id + conversation scope + participant check
├─ delivery axis: Redis pub/sub (fire-and-forget)
│   ├─ PUBLISH returns 1 → push over WS
│   └─ PUBLISH returns 0 → content-free push (SNS → APNs/FCM)
│       └─ why: carrier NAT, OS owns the only connection
└─ observe: page on delivery latency (commit → client ACK)
    ├─ online recipients only
    └─ CPU / DB latency → dashboard, not pager
```
