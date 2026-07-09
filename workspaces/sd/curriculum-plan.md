# SD Curriculum Plan(戰略層,advisory)

<!-- Advisory 性質:runtime 真相永遠在 progress.md,衝突時現場贏、回寫這份。
     整併自 standalone progress.md 的 Learning Mode 區段(S23/S36/S37 三次拍板);
     更早的 curriculum-roadmap.md 與 planning-review.md 已 superseded,verbatim 存
     archive/pre-migration/。教法層(怎麼教這個學生)在 coaching-brief.md,本檔是課什麼、
     什麼順序、多深。 -->

## North Star 對齊

無明確面試日期 → **深度優先**,全課表照走(69 units,Phase Map 見 sd-coach curriculum hook)。
照 ~2.2 session/週的節奏,預估 **2026 年 12 月初完課**。日期是估算不是死線;readiness 領先
curriculum position(見 scorecard-dims 的 Readiness Report 規則)。

## Learning Mode(S23 拍板,仍生效)

**問題錨定 + 深度天花板(Problem-anchored + Depth Ceiling)**

背景:學生在純理論主題(consistency models、consistent hashing 的 vnodes 數學)磨太久,
公式/形式化深度對面試零回報,導致進度緩慢 + 學習痛苦。

1. **深度天花板三問**(現為 engine Depth Ceiling,教練主動執行):(a) 面試官會問嗎?(b) 這層深度能讓回答更好嗎?(c) 卡住是缺地基還是想完美?任一「不會/不能/想完美」→ park 到 curiosity branch。
2. **理論期壓縮**:理論型 building block 用「概念 + 一句話 + 一個 trade-off」快速模式,PoC 降級 Light/Discussion。
3. **題目驅動(pull)**:理論密集段用一個設計題當錨(P2 用 Design a Distributed Cache),理論 just-in-time 拉進來(現為 curriculum hook 的 Problem-Anchored Mode)。
4. 面試考 breadth of mental models + trade-off reasoning,不是 CS 理論深度(形式證明 = PhD 範圍,不學)。

## Execution-Heavy overlay(S37 拍板,生效中)

Phase 2 後已無知識缺口只有執行缺口 → 暫停「每場一個新 archetype」的 acquisition 節奏,
改 drill 為主(**Drill Gauntlet**)。首攻 #1「結論不給論證」。完整 protocol 與評分錨
(tier-1 strong-hire bar、L3 預設)見 `coaching-brief.md` [Execution-Heavy Mode]。
**退出條件:unprompted-argument / unprompted-ops / no-freeze-capacity 三指標各 3 連達標**
後回課表節奏(Day 33 Notification System 起)。

## Scope decision(2026-07-02,S36 後 plan review)

- 從外部訓練營課表補進 3 個缺的 archetype(Day 54-59:Ticket Booking / Top-K / Ride Matching),Phase 4 順延為 Day 60-69。課表總長 69 units(含 Brownfield Migration Day 62-63)。
- 其餘訓練營題目(Dropbox/YouTube/Twitter/A-B Testing 等)= 既有 pattern 組裝,不排課;對照表見 `pattern-map.md`(面試前確認每個 pattern 都能講,碰到沒練過的題拆 pattern 再組裝)。
- Parked PoC triage:留 distributed cache(Day 38-39)+ rate limiter(Day 31-32 的 capacity 補測);放掉 Circuit Breaker 獨立 PoC(概念已 5/5,邊際回報低)。Snowflake Light PoC(Day 30)park 中,排 Gauntlet 之後。

## Re-plan triggers

- 拿到具體面試日期 → 重排:壓縮 Tier 2、提前 Phase 4 mock 連發。
- 三指標達標退出 execution-heavy → 回 acquisition,但每場 drill 保持 L3。
- Weekly Review 連兩次同主題衰退 → 該主題進 Gauntlet 換情境重測(S40 的 Bloom 模式)。
