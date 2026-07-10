# WR5 Mind Map — Multi-Region Session Store (revisit)

```
                    ┌─ GOAL ────→ region dies ≠ 5M re-logins → active-active, both regions
                    │
                    ├─ SYNC? ───→ +150ms EVERY write (sliding TTL = write per request)
                    │             regions' failures infect each other → NO
                    │
                    ├─ ASYNC ───→ ~1s lag window → who falls in? almost nobody → YES
  SESSION STORE ────┤             DAMAGE = window × people in it × symptom
  (multi-region)    │
  (center)          ├─ ZOMBIE ──→ delete = just another write under LWW
                    │             attacker's TTL refresh resurrects session
                    │             → revocation ≠ delete
                    │
                    └─ BLACKLIST → ~hundreds of IDs → plain set, NOT Bloom
                                  in-memory copy per API server (~100ns)
                                  full PULL every N sec → self-healing
                                  worst = 1s + N (missed) + N (failed) ≤ 30s
```

One line: price both sides of every consistency trade (window × people × symptom), and give revocation its own stronger channel because deletes lose races.
