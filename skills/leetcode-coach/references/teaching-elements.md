# Teaching Elements

Domain content that fills Teaching Flow steps B, C, D, and E. The engine keeps the
mechanics (gates, registries, breakpoints); this coach teaches every NEW problem
through the seven-step flow below (第 0 步 ~ 第 6 步, student-specified 2026-07-14).
The flow serves four outcomes and nothing else: 從頭寫出 code、看到題 10 秒 pattern
match、兩個月後仍寫得出來、永遠用最簡單好懂的解法。

| 七步 | Engine step |
|------|-------------|
| 第 0-1 步 模式定位、換一個問法 | B |
| 第 2-4 步 視覺化、推導腳本、手動模擬 | C |
| 從腳本長出 code + 跑 harness | D |
| 換皮題驗收 | E |
| 第 5 步 面試敘事腳本 | G 的材料 (pattern 收尾時) |
| 第 6 步 留存排程 | H 排程 + A 回收 |

A topic is a pattern. 只有 pattern 的首刷題走完整七步;換皮題由學生自己跑推導腳本
(coach 只在卡住時出手),白紙重寫走留存排程。**Gate economy:** 一道新題恰好兩個
chunk — 「推導」(第 0-3 步; Recall = 學生自己把腳本問答跑一遍) 和「驗證」(第 4 步;
Transfer = 「換皮題的 check 和這題差在哪一行?」)。不要把每行程式碼切成 chunk;
gate 數量正比於學生的痛苦。

Cadence: 每日讀書會 sitting 跑第 0-4 步 + 存檔即停 (engine Micro-mode)。Engine 的
F 與 G 在 pattern 收尾時跑一次 (對整個 pattern 的累積題目),不逐題跑;第 5 步的
敘事腳本就是 G 的材料。讀書會是天然的 Teach-to-Learn 對象:收題時說「明天跟同事
講這題時,準備好被問 X」。

---

## Step B: 模式定位 + 換一個問法 (第 0-1 步)

**第 0 步:模式定位,10 秒內講完。** 固定開場句式:「這題不是 [題名] 題,它是
[pattern] 的實例。」接著列同模式換皮題 (題號 + 一句話差異),再給 2-3 個秒認信號。
全部取自下方模式定位表,不即興發明。

**第 1 步:換一個問法 (降維)。** 把原題翻譯成 pattern 的標準形式 (「求最小 k」→
「在答案空間找第一個 True」),再用表中的 DevOps 類比錨定。

### 模式定位表 (秒認信號 + 換皮題鏈 + DevOps 錨)

| Pattern | 秒認信號 | 換皮題鏈 (題號 → 換皮差異) | DevOps 錨 |
|---------|---------|---------------------------|-----------|
| Hash Map | 「配對 / 次數 / 分組」+ 無序資料 | 1 → 217 (找重複) → 242 (次數比對) → 49 (key 換成排序後字串) | DNS / config store 的 O(1) 查表 |
| Two Pointers | 已排序 + 找一對;回文 | 125 → 167 (排序版 Two Sum) → 15 (外層固定一個 + 內層對撞) → 11 (對撞 + 保留高牆) | 兩份排序 log 各一游標對走 |
| Sliding Window | 「連續」子陣列/子字串 + 最長/最短/大小 k | 121 (窗口退化成追蹤最低點) → 3 (變動窗,遇重複縮左) → 424 (變動窗,可容忍 k 次) → 567 (固定窗 + 字頻比對) | CloudWatch 永遠只看最近 5 分鐘 |
| Stack | 「最近的一個」「配對消除」LIFO | 20 → 155 (疊加最小值) → 739 (單調棧:下一個更大) | rollback:最後改的最先退 |
| Binary Search (index) | 已排序 + 找目標/邊界 | 704 → 74 (2D 攤平成 1D) → 153 (旋轉陣列找有序半邊) → 33 (旋轉 + 找目標) | git bisect |
| Binary Search (answer space) | 「最小化最大值 / 最少需要多少」+ check 單調 | 875 → 1011 (吃香蕉換裝貨) → 1482* (天數換花束) | 容量門檻:FFFTTT 找第一個 True |
| Linked List | 找中點/判環 → fast-slow;反轉/合併 | 206 → 21 (合併兩鏈) → 141 (快慢判環) → 143 (中點+反轉+合併三合一) | middleware chain,handler 指向下一棒 |
| Tree DFS | 整棵樹的性質 / 路徑 | 226 → 104 (深度) → 543 (直徑 = 左右深度和) → 110 (深度 + 早退) | `ls -R` |
| Tree/Graph BFS | 層序 / 最短步數 | 102 → 199 (每層取最右) → 994 (多源 BFS 網格) | `find -maxdepth 2` |
| Heap | 「第 k 大 / 前 k 個」不用全排 | 1046 → 703 (串流第 k 大) → 215 → 973 (距離當 key) | incident queue:P1 永遠先 pop |
| Backtracking (認得就好) | 「所有組合 / 排列」 | 78 → 39 (可重複選) → 46 (排列) | 試遍 config 旗標組合,失敗就 undo |
| Graph | 網格連通塊;依賴順序 | 200 → 695 (count 換 max) → 130 (從邊界反向想);207 → 210 (判環換輸出順序) | terraform graph / CI 依賴解析 |
| 1-D DP | 「幾種方法 / 最小成本」只依賴前幾步 | 70 → 746 (count 換 min cost) → 198 (相鄰限制) → 213 (環狀) | Redis memoize:算過的不再算 |
| Intervals | 區間重疊 / 合併 | 56 → 57 (已排序插入) → 435 (反面:留最多 = 貪心) | 維護窗合併 |
| Greedy | 每步局部最優可證安全 | 53 → 55 (可達性) → 45 (層推進) | autoscaling 選當下最省的機型 |

*1482 不在 NeetCode 150,純換皮練 check。Skeleton code 本體在
`references/pattern-cheatsheet.md`。

---

## Step C: 視覺化 → 推導腳本 → 手動模擬 (第 2-4 步)

**第 2 步:視覺化結構 (若有助理解)。** 一張圖,不堆疊。用題目實際數字畫出核心
結構 (答案空間的 FFFTTT 單調邊界、窗口的進出、棧的推疊)。暴力法重複做的 waste
必須先看得見,優化後的 code 才准出現。

**第 3 步:推導腳本。** 解法拆成 3-6 個依序回答的問題,每問的答案直接長出幾行
code。首刷題由 coach 現場**演出**一次「從空白長出程式碼」:逐問展示、每問配對應
code 片段、最後拼裝。這是演出腳本,不是描述腳本。通用 fallback 是 4 問 bridge
(`references/problem-solving-framework.md` Step 2.5);pattern 有自己的腳本時用
pattern 版。二分搜尋五問 (canonical 範例):

1. 我在找什麼?(一句話,產生待辦清單)
2. check 怎麼寫?(先寫驗證,再寫搜尋)
3. 範圍是什麼?(建立不變量:答案必在 [lo, hi])
4. 試了 mid,結果指向哪半邊?(從「mid 可不可能是答案」推出 hi=mid vs lo=mid+1 的不對稱)
5. 何時結束、答案在哪?(不變量收斂到單點)

**第 4 步:手動模擬。** 用題目給的小例子排表格逐步跑 (逐小時/逐天/逐輪),讓抽象
公式對上具體過程。收斂過程 (二分的 lo/hi/mid 表) 也要跑。

Gradual release 對齊留存排程:首刷 = coach 演出 (I do);換皮題 1 = 學生自己跑
腳本,coach 只答卡點 (we do);+2 天白紙重寫 = you do。

---

## Step D: Hands-On

The lab is a per-problem folder (layout in `portfolio.md`) verified by
`scripts/lab-lc.sh <problem-dir>`: all functional tests green AND the large-N timing
test green (see `lab-manager.md`).

1. 學生從自己的腳本答案長出 code:transcribe 已說出口的句子,不是憑空發明。
2. Code 註解標問句編號 (`# Q2: check`),讓「碼」和「why」對齊。
3. 跑 harness。失敗先由學生從 error message debug,coach 才解釋。

**Answer-debt rule.** 看了非自己寫出的解 (累了、趕時間、「直接給我看」都允許) →
立刻登記白紙重寫 debt,3 天內到期;該 pattern 在白紙零 bug 通過前不得標 fluent。

**Compressed-sitting rule.** 短 sitting 可壓縮流程,但到期 re-test 最少留一題;被
跳過的項目記成 dated debt,下次完整 session 先清 debt 再上新內容。

---

## Step E: 換皮題驗收 (驗收即遷移訓練)

- 驗收 = 同 pattern 的換皮題,不是重述剛學的題 (875 教完用 1011 驗收)。難度剛好
  跨到下一題,驗收本身就是遷移訓練。
- 固定收尾問句:「這題的 check 和上一題差在哪一行?為什麼?」— 變的只有 check,
  骨架不變。
- Skeleton fluency 的標準:白紙 cold 寫 template 零 bug (cold-next-day 才算數,
  一次 blind 成功不算)。
- Transfer 問題問機制 (「負數會不會壞?」「沒排序會怎樣?」),不考題號/標題 trivia。
- 驗收沒 log 到任何 Mistake Registry item = 太簡單,下一輪升級。

---

## 第 5 步: 面試敘事腳本 (engine step G 的材料)

邊寫邊講的標準台詞順序:暴力 baseline → 講出關鍵性質 (「單調性」等得分關鍵字要
點名) → bound 的理由 → 邊寫邊解釋非對稱處 → 主動報複雜度。每題附 2-3 個追問預測
與應答。Pattern 收尾的 G 用這個腳本跑 mock,Tiered Scorecard 照常。

---

## 第 6 步: 留存排程 (retention ladder, 對抗遺忘曲線)

主動回憶,不是重讀。每個 pattern 的首刷題進 `retention.md` (domain registry,
宣告在 `portfolio.md`;ladder 為本 coach 宣告,PROGRESS-SCHEMA section 10 允許):

| Rung | 內容 |
|------|------|
| 今天 | 首刷完成 (harness 綠) |
| +2 天 | 白紙重寫首刷題 + 首刷換皮題 1 |
| +7 天 | 換皮題 2 |
| +21 天 | 換皮題 3 + 口頭跑一遍推導腳本 |
| +60 天 | 從該 pattern 已解題隨機抽一題白紙寫 |

- 白紙 = 空檔案、不看舊 code 或筆記;harness 綠才算過。每寫完照 Step E 問 check
  差異問句。
- Fail:當場用卡住協定修卡點,rung 不前進,3 天後重試同 rung。
- +60 過 → pattern retired (仍留在 P7 sprint 的隨機抽測池)。
- 排程歸 step A 檢查:due rung 是當天 sitting 的主內容 (直接當 step D/E),不佔
  step A 的 2-item 快問額度;多個 overdue 時最低 rung 先。

---

## 卡住協定 (學生說「看不懂」時)

1. **定位卡點:** 問或推斷卡在推導腳本第幾問、或哪一行 code。只針對卡點放大,
   不重講全部。
2. **鏡頭拉近,層層拆解:** 一行緊湊 code = 多個概念疊加,拆成獨立層單獨講透再
   組裝。例:`sum((p+k-1)//k for p in piles)` = ①笨迴圈版本 ②整數向上取整技巧
   ③生成器壓縮。
3. **手動模擬優先於解釋:** 與其解釋公式,不如排逐步表格讓學生看到公式是表格的
   壓縮。先誠實模擬,再壓縮成公式;壓縮是優化不是必要。
4. **微驗收:** 每次拆解後給一個 30 秒手算完、常識可交叉驗證的小例子 (7 根香蕉
   每小時吃 3 根,`(7+3-1)//3` 對上「常識上要 3 小時」)。
5. **技巧存成一句話口訣:** 「整數向上取整 = 加 (除數-1) 再整除」「ceil = 天花板,
   floor = 地板」。標注跨語言/跨題通用才值得記;方言寫法不值得為它卡住。口訣寫進
   `one-liner-library.md`。
6. **重串因果鏈:** 確認理解後,把「規則 → 數學性質 → 程式碼寫法」的完整因果鏈
   重新串一遍,每一環學生自己走過。

---

## 反模式 (禁止)

- 直接貼最優解 + 逐行解釋。複述型學習,兩個月必忘。
- 一次教多個 pattern 或炫技多種解法。收斂原則:最簡單好懂、面試過得了的解法
  優先;更優雅的變體進 curiosity branch,學生好奇時再拉回來。
- 逐行切 chunk、逐行開 gate。一題兩個 chunk 就夠 (推導 / 驗證)。
- 卡住時重講全部。只修卡點。

---

## Skeleton Registry (domain registry)

Declared in `portfolio.md`; rows reuse the registry fields from PROGRESS-SCHEMA.md
section 7. One row per core skeleton, with a one-line "when to use" trigger. The
canonical skeleton list and code live in `references/pattern-cheatsheet.md`; the
registry tracks recall scheduling only.

| Skeleton | When to use (trigger) |
|----------|----------------------|
| Frequency counter (hash map) | "count / group / frequency" over unsorted data |
| Complement lookup (hash map) | "find a pair summing to X" without sorting |
| Converging two pointers | sorted input + pair/containment question |
| Fixed sliding window | contiguous subarray/substring of known size k |
| Variable sliding window | longest/shortest contiguous run under a constraint |
| Monotonic stack | "next greater/smaller element", histogram spans |
| Binary search (index) | sorted array + find target/boundary |
| Binary search (answer space) | "minimize the max / find the threshold" with a monotonic feasibility check |
| Tree DFS (recursive) | whole-tree property or path question |
| Tree/graph BFS (deque) | level order or shortest unweighted path |
| Backtracking template | "all combinations/permutations" (recognition only) |
| 1-D DP table | "how many ways / min cost" with overlapping subproblems |
