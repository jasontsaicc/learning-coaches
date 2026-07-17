# Session Log

<!-- 歷史 session 敘事(S1-S16)自 standalone session-progress-archive.md 的
     Problem Log 遷入,內容 verbatim。之後每堂課的 session 摘要續寫於此;
     progress.md 只留 engine schema 欄位。 -->

## Standalone Problem Log (S1-S16, verbatim)

| Session | Problem | Difficulty | Pattern | Solved? | Brute | Optimal | Notes |
|---------|---------|-----------|---------|---------|-------|---------|-------|
| 16 | Binary Search (704) | Easy | Binary Search (標準模板, 閉區間) | ✅ | O(n) linear scan | **O(log n) / O(1)** ⭐ | **Learn 模式**, Phase 1 開場全新 pattern; **skeleton 冷寫第一次 100% 對** (l/r/while/mid/三分支/mid±1/return-1); 3 bug 自 debug 讀錯誤訊息 (`else`帶條件SyntaxError / `mid=(l+r)/2`用`/`float索引TypeError→`//` / `r=len`越界→`len-1`); hostile input (target>全部) trace 出 IndexError, 學到 all pass≠正確; Feynman 全過 (排序→丟半安全 / 沒排序命根子); 教 Yuki 全過 (`<=`vs`<` 單元素會漏 / spot-my-bug `l=mid` 死迴圈**指對行**); **未冷寫 re-do** 下次補 |
| 15 | Largest Rectangle in Histogram (84) | **Hard** | Stack (Monotonic, 遞增) | ✅ | O(n²) / O(1) | **O(n) / O(n)** ⭐ | **Learn 模式**, NeetCode Stack 大魔王; brute 學生自寫 fill-in-blank 5/5 (每根當最矮天花板撞左右矮牆, `width=right-left-1`); stack optimal **code 我給的** (累了要直接看) **未冷寫**; 深挖「A佔2/B佔1」+ 排隊故事 (右牆=新人/左牆=隊尾) 通了; 補結 #739 O(n) 攤還債; 數次「看不懂」退回純白話重建有效; 產出讀書會 HTML (Fable) |
| 14 | Car Fleet (853) | Medium | Stack + Sort | ✅ | O(n²) 模擬 / — | **O(n log n) / O(n)** ⭐ | **Cold Solve** (沒看過的題, workspace/21, 6/6 pass); 龜兔比喻自己提; 手算 fleet=3 全對; pattern 自對應 stack + 自己想通「不用 pop/while」靈魂推理; zip/unpacking 學會; **cars.sort 縮排老毛病自救**; 3 bug 提示後修 (少冒號/`if stack`應`not stack`/`.push()`應`.append`); Cold Solve 3/4 (brute 沒自講); 教 Yuki 跳過待補 |
| 13 | Daily Temperatures (739) | Medium | Stack (Monotonic) | ✅ | O(n²) / O(1) | **O(n) / O(n)** ⭐ | Brute (workspace/20) + Monotonic Stack 都寫；引導發現重複掃描→翻轉；8 格動畫親手跑；cold solve (workspace/20b) 從零默 100% 對, 唯一 `stack, append` 逗點⇄點手滑自讀 NameError 修好; **Stack 升 🟢**; Feynman O(n) 攤還跳過待補 |
| 12 | Min Stack (155) | Medium | Stack | ✅ | — | O(1) all ops / O(n) space | 分享會前速成；自己寫出完整 code；理解 [val,min] 雙層結構、self、stack[-1][0/1]；Feynman: 每個元素進來時記錄當下 min |
| 1 | Valid Anagram (242) | Easy | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(1) | Feynman Gate pass, Drill 3/3 |
| 2 | Top K Frequent Elements (347) | Medium | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(n) | Feynman Gate pass, Mock skipped (no time), jump-to |
| 3 | Encode and Decode Strings (271) | Medium | Arrays & Hashing | ✅ | — | O(n) / O(n) | Feynman Gate pass, Mock skipped, jump-to (study group) |
| 4 | Valid Sudoku (36) | Medium | Arrays & Hashing | ✅ | O(1) / O(1) | O(1) / O(1) | Feynman Gate pass, jump-to (同事分享) |
| 5 | Longest Consecutive Sequence (128) | Medium | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(n) | Feynman Gate partial (快速預習), Mock skipped, jump-to (預習) |
| 6 | Valid Palindrome (125) | Easy | Two Pointers | ✅ | O(n) / O(n) | O(n) / O(1) | Brute → Optimal 完整走一次, Feynman Gate Q1 pass (== vs = 終於鎖住), Q2/Q3 skipped (時間壓力), jump-to (明天分享會) |
| 7 (Day 1) | Container With Most Water (11) | Medium | Two Pointers (Converging + Greedy) | 🟡 進行中 | O(n²) / O(1) | O(n) / O(1) | Brute + Optimal 都自己寫出 + 4/4 tests pass; Feynman Q1 pass (講出 Greedy proof + prune); Q2 + Mock + Notes 留 Day 2; jump-to (NeetCode 150) |
| 7 (Day 2) | Trapping Rain Water (42) | **Hard** | Two Pointers + Bounded Computation | ✅ 主體完成 | O(n²) / O(1) | **O(n) / O(1)** ⭐ | 三層階梯全綠 (Brute 6/6, DP 6/6, Two Pointers 6/6 = 18/18); Feynman Q1 pass (Recall), Q2/Q3 看答案 (🟡); Mock + 變題練習留 Day 3; jump-to (NeetCode 150) |
| 8 | Sliding Window Maximum (239) | **Hard** | Sliding Window + Monotonic Deque | 🟡 主體完成 | O(n·k) / O(k) | **O(n) / O(k)** ⭐ | Brute + Optimal 都親手寫 (12/12 tests pass); Feynman Q1 pass (O(n) amortized 自己講出), Q2/Q3 + Mock 待補; 9 個疑問全解 (deque/負索引/return result/i-k 邊界); 4 個語法錯 (num/windows/in/import); 突破點: 用 8 格動畫終於「看到」deque; jump-to (讀書會) |
| 9-10 | Valid Parentheses (20) | Easy | Stack (FILO 配對) | ✅ | — | O(n) / O(n) | Stack 解親手寫 (workspace/17, 8/8 pass); 複雜度自推對; **Feynman Gate 全過** (Recall FILO↔巢狀 + Transfer 單型別退化counter + Constraint stream→O(n)下限); 3 個 code 錯記入 Registry (分支反/變數名手滑/return寫死) |
| 11 | Evaluate RPN (150) | Medium | Stack (FILO — 最近兩運算元) | ✅ | — | O(n) / O(n) | **Drill 冷寫** 5/5 (workspace/18); 4 bug 自 debug (少`)`/忘return第4次/return縮排進迴圈/`//`floor vs `int(l/r)`truncate); 複雜度自推 (修正後 O(n), 教訓「做幾次×每次多貴」); **Feynman Gate 全過** (進左右出右左鏡像 / 白名單勝isdigit負數陷阱 / pop空stack→IndexError) |

## S16 收尾快照 (2026-07-08, verbatim)

> ✅ Session 16 完成 (2026-07-08) — Binary Search (#704) **Learn 模式** (Easy, Phase 1 開場, 全新 pattern)
> Pattern: **Binary Search (標準模板, 閉區間 `[l,r]`)** — workspace/23, all pass + 3 hostile inputs 驗證
>
> ✅ Warm-up 回測: 複雜度亂加 log 老坑 → 用「兩層線性迴圈=n² / log 只在砍半」問答**過關**, 順勢當 Binary Search 引子 (100萬→20步=log₂n)
> ✅ 學生**拒絕**「#739 是遞增還遞減」這種看題號背答案的回測 → 認同並存 memory (以後只考可遷移原理)
> ✅ **skeleton 冷寫第一次就 100% 對** (l/r init, while, mid, 三分支, mid±1 方向, return -1) — 全新 pattern 卻像 Drill 冷寫等級, 概念部分完勝
> ✅ 3 個 bug 全自 debug (讀錯誤訊息定位): ① `else` 帶條件→SyntaxError ② `mid=(l+r)/2` 用 `/` float 索引→TypeError (該 `//`, #11 // 的鏡像) ③ `r=len(nums)` 越界→改 `len-1`
> ✅ **綠燈不是終點**: 手動 trace hostile input (target>全部) 抓出 `r=len` 的 IndexError, 學到「all pass≠正確」
> ✅ Feynman Gate **全過**: Q1 排序→丟掉那半保證全大/全小→安全; Q2 沒排序命根子沒了→砍半瞎猜; 複雜度 O(log n)/O(1) 自推
> ✅ 教 Yuki closer **完成** (首次沒跳過): `<=` vs `<` (單元素 [5] 會漏) + spot-my-bug `l=mid` 死迴圈 **這次指到精準的行** (補回 S13 弱點) + 為什麼卡死 (mid 被 // 壓在 l)
> 🟡 今天是 Learn (有鷹架+我陪 debug) → **未冷寫 re-do**, 下次 cold re-do 0-bug 才算 Binary Search fluency 達標
>
> ⏭️ Next: ① **#704 Binary Search cold re-do** (驗證 fluency) ② #74 Search a 2D Matrix 或 #875 Koko (Binary Search on Answer) ③ 舊債: #84 stack cold re-do / 教 Yuki (#84+Car Fleet) / Phase 0 Gate
> ⏸️ Weekly Review 嚴重到期 (≥16 session 未做)，強烈建議下次優先補
> ⏸️ Parked Feynman 債務 (Transfer Q2/Q3): #239 Sliding Window Maximum, #42 Trapping Rain Water, #11 Container With Most Water
> ⏸️ Queued: Sliding Window 基礎題 #121 / #3 (workspace/14 有 brute) / #567 (workspace/15 到 Step E)

## S18 收尾快照 (2026-07-14, verbatim)

> ✅ Session 18 完成 (2026-07-14) — **#153 Find Minimum in Rotated Sorted Array** (Medium, P3, Binary Search 邊界變體)
> **七步教學 flow 首次啟用** (teaching-elements.md 當日改版):第 0 步模式定位 → 第 1 步換個問法 → 第 2 步視覺化 → 第 3 步推導腳本 → 第 4 步手動模擬 → step D code + harness
>
> ✅ **solution.py 手打零 bug**, harness **19/19 green** (對比 #74 有 2 bug) — workspaces/leetcode/p3-binsearch-linkedlist/find-minimum-rotated/
> ✅ tripwire 改機制:這題計時抓不到 O(n) (掃 10 萬太快) → 改用 `CountingList` 數 `__getitem__` 次數 (budget 100, BS 實測 ~34), 且 `__iter__` 直接 raise 擋掉 `min(nums)`。**計時失效時換可觀測代理指標**
> ✅ **S17 的核心誤解當場打掉**: 學生自己講出「binary search 的前提是**能確定捨棄的那堆沒有答案**」(不是「array 要 sorted」) → one-liner-library 的 Binary Search 條目已修正
> ✅ 學生自己抓到「沒旋轉 → 只有一段」的特例,並理解為何比 `nums[r]` 能零行特例吃掉它 (比 `nums[l]` 要多寫一行擋)
> ✅ 「證人」論證:只比較一次卻能丟掉半邊,靠的是「第一段每個元素 > 第二段每個元素」的結構保證 → `nums[r]` 一人當全部人的證人
>
> 🟡 Step A 4 抽問: A1 半對 (拒絕誘餌 ✅ 但誤以為 `//` 也回 float) / A2 ❌ (只會複誦「index 所以 -1」, 給不出反例) / A3 ✅ / A4 未答 → **A2+A4 學生要求直接說明 = answer-debt, 3 天內白紙重考**
> 🟡 `[5,6,7,1,2,3,4]` mid 誤標第一段 (機制對、標籤反), 靠矛盾點自行修正
> 🔴 **學生自述最高價值弱點**:「`while` 加不加 `=`、`r=mid` 還是 `mid+1`,還不能直覺搞定」→ 已給配對規則口訣 (兩邊都跳 mid → `l<=r`;有一邊留 mid → `l<r`), 進 one-liner-library, 3 天後抽考
> ❌ **Chunk 2 Transfer 未答** (學生喊停): #33 的 ① 迴圈條件用哪種 ② check 比 #153 多做什麼 → **下次開場先答**
>
> ⏭️ Next: ① #33 Transfer 兩問 (Chunk 2 gate) → step E 用 #33 驗收 ② +2 天 (2026-07-16) 白紙重寫 #153
> 🔴 **Weekly Review 第 3 次順延** (逾期 18 sessions) — S19 前置, 不能再推
> ⏸️ 舊債: #704 閉區間版 cold re-do / #74 complexity gate + step E / #84 stack cold re-do / 教 Yuki (#84+Car Fleet) / P0 Gate
