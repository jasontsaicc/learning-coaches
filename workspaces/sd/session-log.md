# Session Log

<!-- 歷史 session 敘事(新的在上)。S37-S40 的敘事自 standalone progress.md 的 breakpoint
     區段遷入(standalone 時期更早的 session 沒有集中敘事,細節散在 portfolio/sd/notes/ 的
     逐日筆記與 scorecard history);S41 起的 session 摘要續寫於此,progress.md 只留 schema 欄位。

     舊 → 新路徑對照(遷移 2026-07-10):
     - progress.md(repo 根)       → workspaces/sd/progress.md(engine schema)
     - notes/dayXX-topic.md        → portfolio/sd/notes/dayXX-topic.md
     - projects/<poc>/             → portfolio/sd/projects/<poc>/
     - docs/coaching-brief.md      → workspaces/sd/coaching-brief.md
     - docs/pattern-map.md         → workspaces/sd/pattern-map.md
     - docs/curriculum-roadmap.md、docs/planning-review.md → workspaces/sd/archive/pre-migration/
     - sd-coach skill 本體         → skills/sd-coach/(curriculum 詳文=references/curriculum-detail.md) -->

## S40(2026-07-08,execution-heavy:逾期複習清倉收尾 + Drill Gauntlet 首場)

**Part 1 — 逾期複習清倉 4/4 全清(換情境冷測,防概念單鉤子假陽性):**
- **Bloom 重測 ✅ (Box 1→2)**:①FP/FN 嚴重性用**全新通知場景**問 → **答對了**(FP=多查一次可接受 / FN=loss 重要信息不可接受),S39 講反的洞在新情境撈得出 = 真修好。②SSTable 跳讀一開始還是漏「每個 SSTable 配一個」+ 又把「DB 兜底」搬進來(軸摺疊),教完「守門員站每道門」+「省的是讀硬碟不是查 DB」後播放過。多鉤子入庫(快取穿透/通知/SSTable 三場景)。
- **Rate Limiting 機制層 ✅ (Box 2)**:S38 欠的 one-liner 機制補齊。Token Bucket(允許 burst)/Sliding Window(嚴格封頂,自己講出「0:59+1:00 邊界 2×」洞)/兩層(per-user 公平+global 護系統)全對;**CB 三狀態忘了**(S28 resolved 後又掉)→ 用「配電箱電路通不通」重焊 Closed/Open/Half-Open,自己用 AWS 大崩潰例子撞出 Half-Open 防 retry storm。
- **Consistent Hashing ✅ (Box 2→3)**:失敗時間線走出來(換 %11→幾乎全 remap→99% miss→DB 過載雪崩);ring vs vnode **兩軸拆開**(ring=只動 1/N、vnode=負載均勻),vnode 數學自己喊「這是數學題」→ depth ceiling park。
- **Load Balancer ✅ (Box 2)**:S4 四筆老錯結掉三筆(sticky vs Redis 相反策略 / sticky 不均風險 / least robin 命名)。sticky server 死=session 陪葬(非系統 SPOF)校正。**Least Connections 一開始想不起英文名**(WR3 resolved 後 33 天又掉)→ 給演算法對照表重錨。8.8.8.8 trivia 沒測。

**Part 2 — 🥊 Drill Gauntlet 第一場(Distributed Rate Limiter bar-raiser, L3, ~3/9 訓練場):**
- 涵蓋:local counter→5000/min 破表→shared Redis(單一真相來源)→capacity 500K/100K=5 shards(no-freeze ✅ 有給錨)→shard by user_id→race condition/超賣→原子性→INCR(單一命令自足) vs Lua(捆多步 sliding window)。多區域全球限流 preview(A 單一全球 counter 準但跨區延遲 / B 本地+對帳快但近似)後**過載喊停**(教練一次疊太多,pacing 失誤)。
- 🌟 **反脆弱時刻**:「謝謝你拒絕我,逃避心態又來了」+ 頂回去自推 5000/min。知識沒問題,病灶 100% 在「壓力下第一句就縮」。
- ⚠️ **三指標**:unprompted-argument ❌(第一句都裸:"use Redis, cost is low";追問才有論證)/ unprompted-ops ❌(**第 5 次**沒主動收尾監控)/ no-freeze-capacity 🟡✅(沒凍結但半扶)。
- ⚠️ **Step 1 跳過 clarify 直接報解法** + 把剛複習的 LB 演算法亂套(recency bias)。"cost is low" = 初階 tell,已焊「cost 格禁用低/高,一律換具體會咬你的東西」。

## S38(跨機器接續,兩段)

- **(工作 PC) execution-heavy Part 1 逾期複習 1/5:** ✅ **Rate Limiting failure-timeline PASS** — 本地計數陷阱「10 台 ×1000 = 10000/min」冷推出來(S28 的 N×limit 28 天後仍在),補「無聲失敗」點(每台全綠但合計 10 倍 = 監控盲點反例)。→ **Box 1→2**。但 one-liner 機制層(Token Bucket/Sliding Window/兩層/CB)掉了,下次再測(S40 已補)。
- **(家機) Day 31 Distributed Rate Limiter 完整設計 — 全鏈自推:** 從 Rate Limiting 暖身(同上,順接)→ 100 台各跑各的 = 孤島 → N×limit=10,000 → 共享 Redis counter(選對「共享計數器」非「一台限流機器」=SPOF)→ 搶票超賣比喻教 race condition → 學生**自己跳到** Redis 單執行緒 DECR 原子性 → TTL 過期(Fixed Window)取代排程手動補 → 抓到邊界 2 倍破綻 → sliding window「往回看 60s」補洞 → 多步 race 重演 → Lua 捆多步成原子收口。主軸就一個字 atomicity。筆記 `portfolio/sd/notes/day31-distributed-rate-limiter.md`+mindmap。
  - 🌟 **頭號弱點突破**:收尾 One-Liner 主動把「選 sliding window **因為**往回算 request」結論+論證綁一起,沒等追問(execution-heavy 首攻目標本場有一次達標)。
  - 🌟 自抽「**主動 vs 被動**」遷移心法(TTL 過期 > 排程主動清),連到 DevOps 半夜 job 掛。
  - ⚠️ **教練自我教訓**:本場 3 次「有點亂/什麼意思」= 一次塞太多 + 抽象 meta 問句;退小步+具象比喻(搶票、計數紙自燒)後全通。非概念不懂,是 pacing。

## S36(Day 29 Unique ID Generator 設計+理論,Snowflake)

筆記 `portfolio/sd/notes/day29-unique-id-generator.md`。
- **問題錨定教法奏效**:從 KGS(上場)橋接 —「不准中央配號,100 台各自發唯一 ID」→ 學生**自己推出** Snowflake 三段骨架(machineID 不撞跨機器 → 加 counter 同台不撞 → 重啟撞號 → 加 timestamp)。timestamp 放最高位用「日期格式 `2026-06-28` vs `28-06-2026`」比喻打通(「排序由最高位主宰」)。
- **Clock skew(最大雷)**:學生卡在「只覺得很危險」講不出機制 → 用具體數字走「倒退→重入舊毫秒→seq 歸零→重發已發號=撞號」釘死。解法拒發>等>借位,連回 Day27「丟得起 vs 丟不起」。
- **兩條 coaching 設定本場建立(已存 memory)**:[[coaching-no-mechanical-gate-labels]](學生點名「Recall/Transfer」標籤太機械 → 收回,自然問) + [[coaching-aggressive-interviewer-drills]](學生主動要求 Drill 當 bar-raiser 用力追問,他真面試常被追問考倒)。
- **Interview Drill ~4/7(未達 Phase3 線,練習非 Gate)**:✅ think aloud/scope(主動想到 enumeration 洩漏營業額=architect 級,加分)/用 Snowflake;🟡 trade-off WHY(給結論不給論證,被追問才展開=老毛病)/failure modes(SPOF 有 clock skew 沒主動帶);❌ operational(第4次監控掛蛋)+ capacity(「直接放棄」,拆 1024×4 才跟上)。

**當時的 pending(多數已由 S37-S40 消化):** 逾期複習 5 筆(S38-S40 清完)、Security 廣度(OAuth/JWT/session full recall 仍欠,Box 2)、Snowflake Light PoC(park 中)、Circuit Breaker/Replication-lag 獨立 PoC(2026-07-02 triage 放掉,概念已 5/5)。

<!-- S1-S35 無集中敘事;軌跡見 scorecard history(progress.md)、逐日筆記(portfolio/sd/notes/)、
     以及 coaching-brief.md 的 S1-S36 蒸餾。 -->
