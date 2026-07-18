# Curriculum

4 週衝刺,對準 AWS ProServe Delivery Consultant (Cloud Architect, Taiwan) 的面試 loop,申請約在 2026-07-20 送出。Phase 依序推進,engine 透過 Routing branch 5 檢查前置 gate。每個 phase 給一句話焦點加一個綁在前一關 gate 的前置條件。

時間框架是計畫、不是承諾。一旦 phone screen 或 full loop 的日期落地,整個排程繞著那個日期重排,mock 往前提、覆蓋度往後讓。日期是外部硬約束,學習進度會讓路。下面的週數是「沒有外部日期時」的預設節奏。

LP behavioral(領導力原則的行為面試)整段走 `fsi-devops-english`,從 week 1 就平行開跑,不在這個 coach 的範圍內。

## Warm-Up Diagnostic (new students / week 1 intake)

先確認兩件事,順序不能反:

1. 申請狀態:履歷送出了嗎?有沒有拿到 recruiter 回覆、phone screen 或 loop 的日期?任何一個日期都會重排整個計畫(見開頭的時間框架),所以先問清楚再談內容。
2. Resume thread-pull 練習:學員一行一行讀自己的履歷,每讀一行就預測「這行會被面試官追問什麼」。coach 把預測清單記進 progress file。

這份 thread-pull 清單有兩個下游用途:它是 P0 的產出(personalized thread-pull list)的原料,也決定 `references/linux-interview-bank.md` 的練習優先序(履歷挖得越深的 Linux 點,越早練)。

warm-up 的分類(new / mid / strong)寫進 progress.md 的 warm-up classification 欄位,依 PROGRESS-SCHEMA.md 第 2 節,作為 routing 與 pacing 的依據。

## P0 意識定向 (0.5 week)

**焦點**:搞清楚這份工作在做什麼、這個 loop 在測什麼,再開始練技術。前置:無(入門 phase)。

- ProServe Delivery Consultant 的日常:帶 customer workshop、交付 migration、寫 architecture doc。這是 client-facing 顧問職,不是純後端工程師,講不清楚等於做不到。
- Loop 結構:phone screen(LP 加輕量技術)通常在 full loop 前 1-2 週到;full loop 約一半的分數壓在 LP 上,而且每個面試官都會打 LP。這代表技術強但 LP 弱一樣過不了,所以 LP 那條線 week 1 就得在 `fsi-devops-english` 平行跑。
- 產出:personalized thread-pull list,由 warm-up 的 resume thread-pull 練習彙整而成,往下餵 linux-interview-bank 的優先序。

## P1 Networking Gap-Scan (0.5 week)

**焦點**:用掃描的方式找出 AWS networking 的洞,不上課、不做 lab。前置:P0 完成。

- 跑 `references/gap-scan-aws-networking.md`。
- 規則(來自 spec decision 3):「熟悉」要被測、不被相信。學員答得到 mechanism level(講得出運作機制,不是背名詞)就跳過;卡住的那一題,當場變成一堂 mini-lesson。
- 這一關沒有 lab,重點是定位缺口,不是動手做。

## P2 Migration (1 week)

**焦點**:把 migration 的判斷力練到能對著沒看過的 workload 推理。前置:P1 gate 通過。

- 三階段:Assess / Mobilize / Migrate & Modernize。
- 7R decision logic:rehost、replatform、repurchase、refactor、relocate、retain、retire,重點是對著 workload 的限制(licensing、耦合度、時程、成本)推出選哪個 R,講得出 why。
- 工具鏈對應到階段:MGN(server migration)、DMS/SCT(資料庫遷移與 schema 轉換)、DataSync/Snowball(資料搬運)、Migration Hub(進度追蹤)。
- Landing zone:Control Tower、multi-account 結構。
- Hybrid connectivity 與 hybrid DNS:這是對 P1 topic 的第二遍。第一遍(P1)問的是「這是什麼」,這一遍問的是「什麼情況下你會選它」。
- 案例驅動,素材走 `references/case-bank.md`。
- 收尾是第一場 mini-mock。

## P3 Case Drills + Mocks (2 weeks)

**焦點**:把案例練到被追問也守得住,最後用全英文 mock 驗收。前置:P2 gate 通過。

- 白板案例走 `references/case-bank.md`:migration assessment、hybrid architecture、cost optimization、consultant pushback(面試官反駁你的設計時怎麼接)。
- Well-Architected 五大支柱只當評分框架用,不當上課主題。
- Week 4:全英文 full mock 連發,加上弱點重測(前面卡過的點回頭再打一次)。

## Sidecar: Linux Interview Bank

2 個 session,插在 P2 / P3 這幾週之間交錯進行,素材走 `references/linux-interview-bank.md`。

優先序:兩個真實踩過的洞先練,IRQ/softirq 與 static vs shared library。這是履歷 thread-pull 會挖到的深度,也是這個 loop 的隱藏 gate,不能只練架構層。
