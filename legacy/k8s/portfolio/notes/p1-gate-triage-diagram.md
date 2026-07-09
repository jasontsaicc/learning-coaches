# P1 gate — how to find why a Pod is broken (mind map, hand-copy)

```
                                ┌─ bad image name  → fix the name
       ┌─ ImagePullBackOff ─────┤
       │    (cannot pull image) └─ no access (401) → fix login
       │
 Pod   │   step 1:  kubectl get pods       (see STATUS + RESTARTS)
broken ┤   step 2:  kubectl describe pod   (read Reason + Exit Code)
       │
       └─ CrashLoopBackOff = a SYMPTOM, not the cause
                │
                ├─ Exit 137  OOMKilled   → out of memory (over its limit)
                │                           fix: use less, or raise the limit
                │
                ├─ Exit 0    Completed   → the app is FINE
                │                           a bad probe killed a healthy app
                │                           fix: the probe, NOT the app
                │
                └─ Exit 1    Error       → the app crashed
                                            fix: read logs (--previous)
```

One line: CrashLoopBackOff is only a symptom. The Exit Code tells you the real cause.
