# P1 chunk 5 — Resource / QoS / OOM (mind map, hand-copy)

```
                          ┌── requests ──→ SCHEDULER (sum <= node allocatable, no oversell)
              resources ──┤
              │           └── limits ────→ CGROUP / kernel (hard cap, CAN oversell)
              │
              │           ┌── CPU  compressible ───→ THROTTLE (slow, stays alive)
              hit limit ──┤
  RESOURCE /  │           └── MEM  incompressible ─→ OOMKilled (exit 137 = SIGKILL)
  QoS / OOM ──┤
  (center)    │           ┌── container-level → own cgroup; node free = IRRELEVANT
              two OOMs ───┤
              │           └── node-level ────→ kubelet EVICTS, picks by QoS
              │
              │           ┌── Guaranteed  (req == lim)  → evict LAST
              QoS ────────┼── Burstable   (set, not eq) → evict MID
              │           └── BestEffort  (none)        → evict FIRST
              │
              triage ─────→ describe pod → Last State Reason:
              (CrashLoop        OOMKilled / 137  → memory (req/lim, trend)
               = SYMPTOM)       Error / 1        → app crash → logs --previous
                                probe failed     → probe config
                                ImagePullBackOff → image name
```
