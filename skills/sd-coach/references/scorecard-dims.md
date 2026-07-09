# Scorecard Dimensions

These dimensions stack on the engine's Tiered Scorecard frame (defined in ENGINE.md).
The 60% pass threshold is the engine's and is not redefined here. Each tier adds
dimensions on top of all previous tiers; the primary dimension is present at every tier.

## Primary (always-on) dimension

**Think Aloud:邊想邊講,推理過程說出來。**

Pass:每個決定都聽得到理由,面試官不用挖就知道學員在想什麼。
Fail:沉默地畫圖、直接丟結論,或被問才擠出理由。

這是 SD 面試的底層訊號:面試官評的是推理過程,不是最後那張圖。沉默的正確答案拿不到分。

## Tier 1 (P0-P1) — /3

1. Think Aloud(primary)
2. Scope Negotiation(主動澄清需求、圈範圍:「I'll focus on X. Should I cover Y too?」)
3. Used today's building block(今天學的真的用進設計裡)

## Tier 2 (P2) — /6

Adds:
4. **Trade-off WHY**:不只列出選項,講得出為什麼選這個、代價是什麼。
5. **Operational concerns**:monitoring、部署、營運成本有進到設計裡。
6. **Hint response(接住 redirect)**:接住面試官的提示、跟著 redirect 走、協作而不是固執推自己的路。這是 Google GCA 訊號的核心,跟 think aloud 是兩件事。

## Tier 3 (P3+) — /9

Adds:
7. **Failure modes addressed**:主動講元件怎麼壞、壞了怎麼辦。
8. **Capacity estimation**:數字算得出來也算得合理。
9. **Time/breadth management**:4 步都有蓋到,沒有 rat-hole 在單一 deep-dive。很多強者死在這裡:一個元件講到穿但設計沒做完。turn-based mock 裡看的是 exchanges 之間的廣深平衡,不是時鐘。

## Weekly Review Recall Dims (phase-scaled)

Weekly Review 的 blind recall 用縮編維度計分:

- P0:one-liner + trade-off(/2)
- P1:+ scale trigger + DevOps angle(/4)
- P2:+ capacity estimation(/5)
- P3+:+ failure modes + security(/6)

## Style Adaptation: AWS vs Google

兩家都要深度和 trade-off,但戳的點不同,教學員讀房間:

| | AWS | Google |
|--|-----|--------|
| **Managed services** | 可以用(S3、DynamoDB、SQS)並討論營運/成本;DevOps 背景是加分 | 期待「現在設計 DynamoDB 的內部」;靠 managed service 閃掉難點會扣分 |
| **獵的訊號** | Ownership、operational excellence、成本(「一個月燒多少錢」)、LP(Dive Deep、Are Right A Lot) | 純解題力(GCA)、第一性推理、溝通 |
| **判別句** | 「How would you operate/monitor/oncall this?」 | 「Why does that work? What's the alternative?」往下壓 |

## Readiness Report (domain format)

學員要進度報告或 gate 通過時,從 progress.md 產生:readiness 領頭(building block 熱力圖、classic problems 練過幾題、mock 分數趨勢、top unresolved mistakes、error pattern),curriculum 位置(Day X/69)降級到最後一行,標注「是地圖座標不是死線」。學員在準備面試,不是在趕 69 天日曆。

## Feedback Footer

每次 scorecard 後固定附:

```
💡 Top improvement: [一個具體可行的建議]
🌟 Best moment: [一個做得好的點]
```
