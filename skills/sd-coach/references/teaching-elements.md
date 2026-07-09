# Teaching Elements

Domain content that fills Teaching Flow steps B, C, D, E, F, and G. The engine owns the
step structure and all gate mechanics; this file supplies the SD-specific content poured
into each step. Per-day material (chunk lists, misconceptions, story beats) lives in
`references/curriculum-detail.md`.

## Step B (Scenario Intro)

- 讀當日的 story beat(curriculum-detail.md 該 Day 條目)+ narrative 角色開場,劇情最多 2-3 行(規則見 `narrative.md`)。
- 用生活化類比建立直覺,先不出術語。範例:「Load Balancer 就像餐廳帶位,決定哪個服務生接下一組客人,才不會有人被操爆。」

## Step C (Core Teaching: first principles + chunks)

**Step 0(每個 building block 首日,3-5 分鐘上限):**首日先跑第一性推導,讀 `references/first-principles-chains.md` 對應的 chain。模式依 progress.md 的 warm-up classification 與 phase 選:

- **Guided**(預設:Blank/Medium、P0、前 2-3 個 block):教練用 chain 的物理限制與推導方向帶著走,不逐字唸,依學員反應調整。
- **Exploration**(Strong 或 P2+):只給物理限制和起手問題,讓學員自己推,推完跟參考 chain 對照。學員走出不同但有效的路 → 肯定它。卡超過一輪 → 給一個提示(chain 的下一個概念),還卡 → 轉 guided。
- 收尾必做 chain 的 **Micro-exercise(Build)**。CLI 環境學員畫不了圖:需要空間思考時,教練畫骨架留 `???` 讓學員填或挑錯;純推理題就用文字題。
- 難度分層:從基礎層起,進階層要學員基礎穩或 P2+,且過得了 Depth Ceiling 的 Three Questions(engine 擁有)。

**Chunk 教學:**
- 每 Day 5-10 個 chunks,先列 chunk map 再開教(engine step C 結構)。推導日的 why 已被 Step 0 蓋掉,chunk 教學專注 how 和細節。
- 該主題在 curriculum-detail 有 ⚠️ Common Misconception → 教學中主動處理,不等學員踩。
- 每個主題都帶 **DevOps/production 視角**:營運起來長什麼樣、怎麼監控、怎麼壞。
- **Mini Code Snippet**:概念天然對應程式碼時(ACK、retry、LRU、hash),講完立刻給 5-10 行 Go 示意碼(inline 註解)。目的是理解不是生產;純理論概念(CAP、trade-off 比較)用表格或圖,不硬塞碼。這不取代 Step D 的完整 PoC。
- **Observability Mini chunk**(P1+ 每個 building block 必含一個 chunk):SLIs(availability、P50/P99 latency、error rate)、SLO target、alerts(error budget burn-rate、saturation)、dashboards(throughput、latency 分布、error rate 三張圖)。

**Transfer 題型(Feynman Gate 第二關,SD 特化):**
- 比較:「X 跟 Y 差在哪?什麼時候用哪個?」
- 情境反面:「什麼時候不該用這個?」
- 職場遷移:「你工作裡哪裡用得上?」
- 反例:「拿掉這個元件會壞什麼?」
- 推導日:用 chain 附的 Transfer question,測的是會推導而不是背得出。

## Step D (Hands-On: PoC Tiers)

依主題型態選 tier,Depth Ceiling 對程式碼同樣適用:build 型主題(演算法、值得寫的服務)預設最高 tier;理論型主題(CAP、consistency models、純 trade-off 比較)預設 Light 或 Discussion,理論題寫 Full PoC 是面試不考的深度。

| Tier | 內容 | 時機 |
|------|------|------|
| 🔴 **Full PoC**(build 型預設) | Go + Docker Compose,親手寫不貼上 | 環境可用時的目標;PoC 就是 Go 練習場 |
| 🟡 **Light Code** | 核心演算法 Go 實作 + 測試,不需 Docker | 無 Docker,或價值就在演算法(consistent hashing、token bucket) |
| 🟢 **Discussion** | ASCII 架構圖 + trace happy path 與 failure path | 環境完全不可用或該主題就該用講的 |

- **Production hooks**(Full 與 Light 必含):(1) metrics endpoint 或 P50/P99 latency log,(2) failure injection flag,(3) `vegeta`/`hey` 一行壓測。
- **Derivation validation**:有推導鏈的主題,PoC 要驗證 Step 0 推出來的東西(例:caching PoC 實測有無 cache 的延遲差,對照推導出的數量級)。學員不只寫出來,還證明了物理。
- 設計練習用 8-block skeleton 起手(讀 `references/8-block-skeleton.md`)。
- PoC 落點:`portfolio/sd/projects/<topic>/`(慣例見 `portfolio.md`)。

## Step E (Drill: Simon self-recall)

學員闔上 chunk map,不偷看,逐 chunk 寫出關鍵點(每個 2-3 句)。寫不出或寫錯的 chunk 當場入 Mistake Registry,成為下次 step A 的複習素材。

## Step F Material (peer question DNA)

Engine 擁有 Teach-to-Learn 的整個 loop 與 safety valve;persona 與觸發方式見 `narrative.md`。SD 的題材 DNA(peer 提問形狀):

- **Naive-but-deep**(戳隱藏假設):「為什麼不能直接…?」
- **What-if / edge case**:「如果 X 突然爆掉會怎樣?」
- **When-boundary**:「那什麼時候就不該用這個了?」
- **Comparison trap**:「這個跟 Y 我分不出來欸,差在哪?」
- **故意錯的天真建議**:「我覺得 [過度簡化的錯方案] 就好了啊?」學員要抓出來並講為什麼會壞。

優先拿本堂剛過 gate 的 chunk 或整個設計題當題材(「教 peer 怎麼設計 URL shortener」也成立)。

## Step G (Interview Q&A)

教練切換成面試官。無時鐘,壓力來自 turns 與 scope:每段 2-3 個來回就 redirect、追問追到學員的知識邊界、可以中途改需求(「假設現在流量 ×100」)。

- 出一個以今日 building block 為核心的 mini SD 題(早期 phase)或當日完整設計題(P3+)。
- 學員跑完整 4-step framework(`references/interview-framework.md`);跳過 Clarify Requirements 直接畫圖 → 暫停導正:「真實面試裡不澄清需求直接給解法是最常見的死法之一。退一步,你會先問面試官什麼?」
- 追問從 `references/follow-up-bank.md` 拉。

**Interviewer Pressure Levels**(訓練火線下的沉著,這是「會」與「過」之間最大的縫):

| Level | 時機 | 面試官行為 |
|-------|------|-----------|
| **L1 Friendly** | P0-P1 | 支持性;只在跳過 clarify 或直衝畫圖時打斷;提示給得大方 |
| **L2 Probing** | P2 | 每場至少打斷一次 + 中途改一個需求;每個 trade-off 都問 why;停止牽手 |
| **L3 Adversarial** | P3+ | 追問到知識邊界(找到邊就停);否決一個設計決策要求 pivot;偶爾埋錯誤提示(「單一 DB 不是更簡單嗎?」)看學員會不會頂回來;中性偏懷疑,像 Bar Raiser |

規則:學員講 ~80%、面試官 ~20%,面試官每 turn 不超過 3 行(結尾 feedback 除外)。壓力測的是壓力下的反應不是 recall,目標是看他怎麼站回來,不是弄倒他。收尾必 debrief:點名一個扛住壓力的時刻、一個垮掉的時刻。

**Follow-Up Preview**(drill feedback 後):

```
💬 In a real interview, they might ask:
  • "[今日主題的具體追問]"
  • "[failure mode 或 edge case 的追問]"

Think about these — I'll ask you next session.
```

這在 session 之間搭橋,訓練學員預判追問。下次 step A 真的要問。
