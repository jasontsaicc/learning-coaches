# 4-Step SD Interview Framework

Every design answer follows this structure. The time ranges describe a real 45-minute
interview's shape; in coaching mocks pressure comes from turns and scope, not a clock.

```
Step 1: Clarify Requirements (0-5 min)
  - Functional: What does the system DO?
  - Non-functional: Scale, latency, availability, consistency
  - Scope negotiation: "I'll focus on X. Should I cover Y too?"

Step 2: High-Level Design (5-15 min)
  - API design (REST/gRPC endpoints)
  - Data model (entities, relationships, access patterns)
  - Architecture diagram (start with the 8-block skeleton)

Step 3: Deep Dive (15-35 min)
  - Pick 1-2 core components
  - Show depth: algorithms, data structures, trade-offs
  - Interviewer may redirect — follow their lead

Step 4: Scale & Trade-offs (35-45 min)
  - Bottlenecks and how to address them
  - Failure modes and mitigation
  - Monitoring, alerting, operational concerns
```

常見死法對照(教練在 Step G 盯這些):

- Step 1 被跳過:直衝畫圖。真實面試最常見的失分點,當場暫停導正。
- Step 2 沒有 data model:只有框框和箭頭,沒有 entities 與 access patterns。
- Step 3 rat-hole:一個元件講到穿,設計沒做完(scorecard 的 time/breadth 維度)。
- Step 4 只有 scale 沒有 failure:瓶頸講了,但沒人問就不講怎麼壞、怎麼恢復。
