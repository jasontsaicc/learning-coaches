# Phase Gates

The engine enforces the 3-attempt cap, the failure protocol, and the blind Examiner
mechanics; this file defines what "pass" means per phase. Gates are scope-based, not
timed: mini / full mock 指的是學員要蓋掉多少範圍(由 turns 與追問執行),不是分鐘數。
Scorecard tiers 見 `scorecard-dims.md`;retry 一律換題。

## P0 Gate — Thinking Framework

**Pass condition:** 用 4-step framework 回答一個簡單 SD 題,四步都有、結構合理。

**Examiner inputs:** the student's verbatim 4-step answer (all four steps, unedited).

Specifically, the student must:
1. 先澄清需求(functional + non-functional),有 scope negotiation。
2. 給出 high-level design 並講出元件之間的關係。
3. 至少一處講出 trade-off(即使淺)。

## P1 Gate — Core Building Blocks

**Pass condition:** 任一 building block 的 mini-mock 過 Tier 1 scorecard 門檻(≥2/3):clarify + high-level design + 1 個 deep-dive,面試官每 2-3 個來回 redirect 一次。

**Examiner inputs:** the mock Q&A verbatim (every interviewer question/redirect and the student's answers) and the Tier 1 dimensions.

Specifically, the student must:
1. 被 redirect 時接得住,不固執原路。
2. Deep-dive 講到機制層(為什麼這樣設計),不只名詞。
3. 帶到 Observability Mini(這個 block 該量什麼、alert 什麼)。

## P2 Gate — Distributed Systems Core

**Pass condition:** 完整 mock:設計 multi-region session store,4 步全跑,面試官中途改一個需求,過 Tier 2 門檻(≥4/6)。

**Examiner inputs:** the mock Q&A verbatim, the mid-mock requirement change and the student's pivot, and the Tier 2 dimensions.

Specifically, the student must:
1. 用上 P2 的分散式核心(consistency model 的選擇與代價、replication 策略)並講出 why。
2. 需求被改時 pivot 得動,講出改動牽動哪些元件。
3. Operational concerns 有進設計(不是事後補一句 monitoring)。

## P3 Gate — Classic SD Problems

**Pass condition:** Tier 1 經典題 full mock,4 步 + 追問壓到知識邊界,過 Tier 3 門檻(≥6/9)。

**Examiner inputs:** the full mock transcript verbatim (including boundary-pushing follow-ups and any planted wrong hint), and the Tier 3 dimensions.

Specifically, the student must:
1. Capacity estimation 算得出來且數量級合理。
2. 主動講 failure modes 與緩解,不等面試官問。
3. 面試官埋的錯誤提示要頂回來(有理由地),不盲從。
4. 4 步都蓋到,無 rat-hole。

## P4 Gate — Advanced & Mocks

**Pass condition:** Final mock(brutal mode,L3 壓力全程):一題未練過的題 + 一個 brownfield 變體,過 Tier 3 門檻。

**Examiner inputs:** the full mock transcript verbatim, the brownfield pivot exchange, and the Tier 3 dimensions.

Specifically, the student must:
1. 未練過的題也能用 building blocks 現場組合出合理設計(理解可遷移的最終證明)。
2. Brownfield 限制(不能砍掉重練、要遷移)有被尊重,遷移路徑講得出步驟與風險。
3. 全程扛住 L3 壓力:被否決一個決策後 pivot,並 debrief 得出自己剛才哪裡差點垮。
