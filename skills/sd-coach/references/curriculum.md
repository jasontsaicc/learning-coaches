# Curriculum

5 個 phase,「Day」是內容單位不是日曆天(一個 Day 可跨多次 sitting,一次 sitting 也可能推進不到一個 Day)。完整的逐日教材(chunk 清單、misconception、story beat、derivation chain 對應)在 `references/curriculum-detail.md`,**只在進到該 Day 時讀對應段落**,不要在 session 開始時整檔讀完。

每學員的戰略層規劃(面試窗口、pattern 地圖、複習策略)在 `workspaces/sd/curriculum-plan.md`,advisory 性質;runtime 真相以 progress.md 為準,衝突時現場贏、回寫該檔。

## Warm-Up Diagnostic (new students only)

先給課程地圖(5 phases),再跑快速診斷,讓互動從第一分鐘開始:

> "Imagine you're in an interview and the interviewer says: **'Design a simple URL shortener.'** Don't worry about getting it right, just talk me through how you'd approach it in 2-3 minutes."

- **Strong**(提到 requirements、components、trade-offs)→ Phase 0 可加速。
- **Medium**(知道片段但無結構)→ Phase 0 剛好。
- **Blank**(不知從何下手)→ 安撫,這正是 Phase 0 要教的。

結果寫進 progress.md 的 warm-up classification 欄位,作為 routing、pacing 與 Step 0 模式選擇的依據。

## Phase Map

| Phase | 一句話焦點 | 前置 | 教材段落 |
|-------|-----------|------|---------|
| **P0 Thinking Framework**(Day 1-3) | SD 面試在測什麼、估算、4-step 答題框架 | 無(入門 phase) | curriculum-detail.md Phase 0 |
| **P1 Core Building Blocks**(Day 4-16) | LB、caching/CDN、database、MQ、API design、security/auth、consistent hashing | P0 gate | curriculum-detail.md Phase 1 |
| **P2 Distributed Systems Core**(Day 17-26) | CAP、consistency models、replication/leader election、rate limiting、observability、bloom/gossip | P1 gate | curriculum-detail.md Phase 2 |
| **P3 Classic SD Problems**(Day 27-59) | Tier 1 必做 8 題 → Tier 2 應做 7 題(Tier 3 選做) | P2 gate | curriculum-detail.md Phase 3 |
| **P4 Advanced & Mocks**(Day 60-69) | trade-off 深潛、brownfield migration、mock 連發(最後一場 brutal mode) | P3 gate | curriculum-detail.md Phase 4 |

## Problem-Anchored Mode

理論密集段(P2 尤其)預設不逐日上課,改為錨定一個設計題:設計驅動、理論 just-in-time 拉進來、拉到 interview depth 為止。這正是知識在面試裡被使用的方式(服務一個設計,不是講課主題)。P2 的錨定題與 pull map 在 curriculum-detail.md Phase 2 開頭。每個被拉進來的概念仍走自己的 Feynman Gate、仍寫各自的筆記;curriculum-detail 的逐日條目就是該概念被拉進來那一刻的教材。

## Cross-Cutting Requirements

- **Observability Mini**:P1 起每個 building block 都要定義 SLIs、SLO target、alerts、dashboards(四格表)。把 monitoring 織進 SD 回答是面試的差異化訊號。
- **Milestones**:P1 結束與 P2 結束的 gate 本身就是 mini-mock;P3 每題收尾都是一次完整 drill。

## Cross-Phase References

| 檔案 | 用途 |
|------|------|
| `references/curriculum-detail.md` | 逐日教材主檔(69 Days + gates + PoC 語言工具) |
| `references/first-principles-chains.md` | Step C Step 0 的推導鏈(每個 building block 首日) |
| `references/interview-framework.md` | 4-step 答題框架(Step G 與所有 mock) |
| `references/follow-up-bank.md` | 面試官追問題庫(Step G) |
| `references/answer-comparisons.md` | L4 vs L6 答案對照(P3+ mock 前,或學員問「好答案長怎樣」) |
| `references/estimation-cheatsheet.md` | 估算數字表(P0 Day 2 與任何估算練習) |
| `references/8-block-skeleton.md` | 白板架構圖起手式(Step D 設計練習) |
| `references/phase4-drills.md` | P4 陷阱與 pivot 劇本 |
| `references/notes-template.md` | Step H 筆記模板(含 mind map 規格) |
