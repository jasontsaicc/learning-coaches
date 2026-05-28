# Student Progress Tracking

> This file is the single source of truth for student progress.
> Updated by Claude at the end of every session (Step I) and when sessions are interrupted.
> Read by Claude at the start of every session to determine where to resume.

---

## Student Info

| Field | Value |
|-------|-------|
| **Start date** | 2026-03-17 |
| **Current phase** | Phase 0 |
| **Current pattern** | Two Pointers |
| **Language** | Python |
| **Session count** | 7 |
| **Last weekly review** | — |
| **Problems solved** | 7 / 136 |

---

## Current Session (Breakpoint)

> 🔄 Session 8 (2026-05-28) 進行中
> Problem: Sliding Window Maximum (#239) **Hard** — jump-to (讀書會分享)
> Current step: H 完成 (Notes → notes/pattern16)；F 只過 Q1 (Recall: O(n) amortized)，Q2 (改成 min) / Q3 (constraint) + G Mock 待補
>
> ⏸️ Queued: Permutation in String (#567) workspace/15 (前一場 05-22 做到 Step E)；Best Time to Buy and Sell Stock (#121) Sliding Window 第 1 題；Longest Substring (#3) workspace/14 已有 brute force
> ⏸️ Weekly Review 到期 (8 - 0 ≥ 7)，優先排
> ⏸️ Parked: Trapping Rain Water (#42) F Q2/Q3 + G Mock；Container With Most Water (#11) F Q2/G/H；Two Sum II (#167) Step E bug

---

## Topic Mastery (per Pattern)

| Pattern | Problems Done | Mastery | Phase Gate | Notes |
|---------|--------------|---------|------------|-------|
| Arrays & Hashing | 5/11 | 🟡 | — | Frequency Counter + Bucket Sort + Length-Prefix + HashSet per row/col/box + Sequence Start Detection learned. #238 (Product of Array Except Self) skipped, revisit later |
| Two Pointers | 2.5/5 | 🟡 | — | + #42 Trapping Rain Water (Hard) 三層算法全綠 (Brute/DP/Two Pointers 18/18) — 加分: 自抓 6 個 bug 全修對；扣分: Q2/Q3 Feynman 沒自答 (看答案)。升 🟢 條件: Day 3 完成 F + G |
| Sliding Window | 1/5 | 🟡 | — | #239 Sliding Window Maximum (Hard, jump-to 跳關做最難的第 6 題): Brute O(n·k) + Optimal Monotonic Deque O(n) 都親手寫過 12/12 tests; Feynman 只過 Q1 (O(n) amortized 講得出); Q2/Q3 + Mock 待補。基礎 5 題 (#121, #3, #424, #567...) 尚未做 |
| Stack | 0/6 | ⬜ | Phase 0 Gate | |
| Binary Search | 0/6 | ⬜ | — | |
| Linked List | 0/9 | ⬜ | — | |
| Trees | 0/13 | ⬜ | — | |
| Heap / Priority Queue | 0/6 | ⬜ | Phase 1 Gate | |
| Backtracking | 0/9 | ⬜ | — | |
| Tries | 0/3 | ⬜ | — | |
| Graphs | 0/12 | ⬜ | — | |
| Advanced Graphs | 0/5 | ⬜ | Phase 2 Gate | |
| 1-D Dynamic Programming | 0/12 | ⬜ | — | |
| 2-D Dynamic Programming | 0/6 | ⬜ | — | |
| Greedy | 0/7 | ⬜ | — | |
| Intervals | 0/6 | ⬜ | — | |
| Math & Geometry | 0/8 | ⬜ | — | |
| Bit Manipulation | 0/7 | ⬜ | Final Gate | |

> Mastery levels: ⬜ Not started │ 🔴 Needs work │ 🟡 Developing │ 🟢 Solid

---

## Problem Log

| Session | Problem | Difficulty | Pattern | Solved? | Brute | Optimal | Notes |
|---------|---------|-----------|---------|---------|-------|---------|-------|
| 1 | Valid Anagram (242) | Easy | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(1) | Feynman Gate pass, Drill 3/3 |
| 2 | Top K Frequent Elements (347) | Medium | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(n) | Feynman Gate pass, Mock skipped (no time), jump-to |
| 3 | Encode and Decode Strings (271) | Medium | Arrays & Hashing | ✅ | — | O(n) / O(n) | Feynman Gate pass, Mock skipped, jump-to (study group) |
| 4 | Valid Sudoku (36) | Medium | Arrays & Hashing | ✅ | O(1) / O(1) | O(1) / O(1) | Feynman Gate pass, jump-to (同事分享) |
| 5 | Longest Consecutive Sequence (128) | Medium | Arrays & Hashing | ✅ | O(n log n) / O(n) | O(n) / O(n) | Feynman Gate partial (快速預習), Mock skipped, jump-to (預習) |
| 6 | Valid Palindrome (125) | Easy | Two Pointers | ✅ | O(n) / O(n) | O(n) / O(1) | Brute → Optimal 完整走一次, Feynman Gate Q1 pass (== vs = 終於鎖住), Q2/Q3 skipped (時間壓力), jump-to (明天分享會) |
| 7 (Day 1) | Container With Most Water (11) | Medium | Two Pointers (Converging + Greedy) | 🟡 進行中 | O(n²) / O(1) | O(n) / O(1) | Brute + Optimal 都自己寫出 + 4/4 tests pass; Feynman Q1 pass (講出 Greedy proof + prune); Q2 + Mock + Notes 留 Day 2; jump-to (NeetCode 150) |
| 7 (Day 2) | Trapping Rain Water (42) | **Hard** | Two Pointers + Bounded Computation | ✅ 主體完成 | O(n²) / O(1) | **O(n) / O(1)** ⭐ | 三層階梯全綠 (Brute 6/6, DP 6/6, Two Pointers 6/6 = 18/18); Feynman Q1 pass (Recall), Q2/Q3 看答案 (🟡); Mock + 變題練習留 Day 3; jump-to (NeetCode 150) |
| 8 | Sliding Window Maximum (239) | **Hard** | Sliding Window + Monotonic Deque | 🟡 主體完成 | O(n·k) / O(k) | **O(n) / O(k)** ⭐ | Brute + Optimal 都親手寫 (12/12 tests pass); Feynman Q1 pass (O(n) amortized 自己講出), Q2/Q3 + Mock 待補; 9 個疑問全解 (deque/負索引/return result/i-k 邊界); 4 個語法錯 (num/windows/in/import); 突破點: 用 8 格動畫終於「看到」deque; jump-to (讀書會) |

---

## Interview Drill Scorecard History

| Session | Problem | Pattern | Score | Details |
|---------|---------|---------|-------|---------|
| 1 | Permutation check (variation) | Arrays & Hashing | 3/3 | Think aloud ✅, Pattern ID ✅, Code runs ✅ |

---

## 🔴 Mistake Registry

| Session | Problem | Pattern | Mistake | Status |
|---------|---------|---------|---------|--------|
| 1 | Valid Anagram | Arrays & Hashing | Python 布林值大小寫 false→False | ✅ Resolved (S3) |
| 1 | Valid Anagram | Arrays & Hashing | sorted() 是函式不是 method | ✅ Resolved (S2) |
| 1 | Valid Anagram | Arrays & Hashing | = 賦值 vs == 比較 | ✅ Resolved (S2) |
| 1 | Valid Anagram | Arrays & Hashing | 判斷邏輯反轉（== 0 vs != 0） | ✅ Resolved (S3) |
| 1 | Valid Anagram | Arrays & Hashing | 排序複雜度記成 O(log n) 而非 O(n log n) | ✅ Resolved (S2) |
| 1 | Valid Anagram | Arrays & Hashing | 固定字元集 O(1) vs 無限字元集 O(n) | ✅ Resolved (S3) |
| 2 | Top K Frequent | Arrays & Hashing | Bucket 的 value 以為是 nums 的 index，實際是元素本身 | ✅ Resolved (S2) |
| 2 | Top K Frequent | Arrays & Hashing | freq.get() 加了括號，key= 要傳 function 本身不加 () | ✅ Resolved (S2) |
| 2 | Top K Frequent | Arrays & Hashing | 忘記 from collections import Counter | ✅ Resolved (S2) |
| 2 | Top K Frequent | Arrays & Hashing | Reverse scan complexity 以為 O(k)，實際 O(n) | ✅ Resolved (S2) |
| 3 | Encode Decode | Arrays & Hashing | 用 len(strs) 取 list 長度，應該用 len(s) 取每個字串長度 | ✅ Resolved (S3) |
| 3 | Encode Decode | Arrays & Hashing | 以為 length-prefix 安全是因為「只看第一個 #」，實際是靠長度數字元 | ✅ Resolved (S3) |
| 4 | Valid Sudoku | Arrays & Hashing | cols[r] 寫成 row index，應該是 cols[c] | ✅ Resolved (S4) |
| 4 | Valid Sudoku | Arrays & Hashing | 只查 set 沒有 add，set 永遠是空的查不到重複 | ✅ Resolved (S4) |
| 5 | Longest Consecutive | Arrays & Hashing | = 和 == 混用（第四次） | ✅ Resolved (S6) - Feynman Gate Q1 能講清楚「= 改變世界、== 問問題」 |
| 5 | Longest Consecutive | Arrays & Hashing | counter += i-1 用 index 而非固定 +1 | ✅ Resolved (S5) |
| 5 | Longest Consecutive | Arrays & Hashing | 起點判斷邏輯反了（有值→沒值） | 🟡 Parked - 補課時理解，尚未自主應用測試 |
| 6 | Valid Palindrome | Two Pointers | Optimal 版忘記 `.lower()`，`s[l] != s[r]` 比較大小寫 | ✅ Resolved (S6) |
| 6 | Valid Palindrome | Two Pointers | 比較完忘記 `l += 1; r -= 1` 移動指標（會無限迴圈） | ✅ Resolved (S6) |
| 6 | Valid Palindrome | Two Pointers | function 最後忘記 `return True`（Python 回 None → 被當 False） | ✅ Resolved (S6) |
| 6 | Valid Palindrome | Two Pointers | Brute force 也忘記 return（同一 session 兩次） | ✅ Resolved (S6) |
| 7 | Container With Most Water | Two Pointers | Edge cases 亂猜「負數」沒對照 constraints (`0 <= h[i]`) | ✅ Resolved (S7) - 教訓：先讀 constraints 再列 edge cases |
| 7 | Container With Most Water | Two Pointers | `area = if (j-i)*min(...)` — Python `if` 不能當 expression | ✅ Resolved (S7) |
| 7 | Container With Most Water | Two Pointers | `l++` / `r--` 直接寫（C/Java 寫法）— Python 沒有這運算子 | ✅ Resolved (S7) - **重大語法觀念補完** |
| 7 | Container With Most Water | Two Pointers | `l = l += 1` 兩個運算子合用（語法錯誤）| ✅ Resolved (S7) |
| 7 | Container With Most Water | Two Pointers | `while l > r:`（方向反了，loop 不會跑）| ✅ Resolved (S7) - 學到「代真實數字 trace 驗證」|
| 7 | Container With Most Water | Two Pointers | `max_area = max(max_area, area)` 之前忘記初始化 `max_area = 0` | ✅ Resolved (S7) |
| 7 | Container With Most Water | Two Pointers | `if ...:` 留佔位符忘記填邏輯（`...` 是 Ellipsis 永遠 truthy）| ✅ Resolved (S7) |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | `for i in range(len(height)) - 1` — range object 不能減 1，且本意不該 -1 | ✅ Resolved (S7-D2) - Python `range(n)` 已含 0..n-1 |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | `for` 結尾忘記 `:` (第二次踩) | ✅ Resolved (S7-D2) |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | `total +=` 之前忘記初始化 `total = 0` (第二次踩, 同 max_area 教訓) | ✅ Resolved (S7-D2) |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | `min(left_max[i], right_max[i] - height[i])` — `)` 位置錯，括號決定優先順序 | ✅ Resolved (S7-D2) - **重大語法觀念**: 括號改變語意 |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | 鏡像對稱沒做完整：右邊分支只有 if (更新)、缺 else (加水) | ✅ Resolved (S7-D2) - 對稱寫法要兩邊都檢查 |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | `r -= 1` 縮排錯位，跑到 `else` block 外，每輪都 -1 | ✅ Resolved (S7-D2) - **重大語法觀念**: 縮排決定 block |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | Q2 (`[5,4,3,2,1]` 為什麼 0) Feynman Variation 沒自答 | 🟡 Parked - Day 3 Step A 重抽 |
| 7 (Day 2) | Trapping Rain Water | Two Pointers + Bounded | Q3 (heights 允許負數會壞掉) Feynman Constraint Change 沒自答 | 🟡 Parked - Day 3 Step A 重抽 |
| 8 | Sliding Window Maximum | Sliding Window + Deque | `num` vs `nums` 變數名少 s → NameError | ✅ Resolved (S8) |
| 8 | Sliding Window Maximum | Sliding Window + Deque | `windows` vs `window` 單複數不一致 | ✅ Resolved (S8) |
| 8 | Sliding Window Maximum | Sliding Window + Deque | `in` / `import` 關鍵字被 IDE 自動補全塞進來 → SyntaxError | ✅ Resolved (S8) - 教訓: 打完 i 別按 Tab/Enter |
| 8 | Sliding Window Maximum | Sliding Window + Deque | 以為 sliding window「指針 vs deque」二選一 | ✅ Resolved (S8) - 兩者並存: 指針管邊界, deque 管 max 候選 |
| 8 | Sliding Window Maximum | Sliding Window + Deque | 以為窗戶每滑一格就「直接 popleft 最左」 | ✅ Resolved (S8) - 只有真過期 (dq[0]<=i-k) 才踢, deque≠window, 最左常是答案 |
| 8 | Sliding Window Maximum | Sliding Window + Deque | 窗戶 [1,3,-1] 以為 -1 也可丟 (新+小) | ✅ Resolved (S8) - 規則單方向: 只有「舊+小」可丟 |
| 8 | Sliding Window Maximum | Sliding Window + Deque | `max(current_max, window)` 跨窗戶累積 vs 單窗戶獨立 max | ✅ Resolved (S8) |

---

## 🎯 Pattern One-Liner Library

| Pattern | One-Liner |
|---------|-----------|
| Frequency Counter (Arrays & Hashing) | 用 hash map 計算字元頻率 — 一個 +1 一個 -1，全部歸零就一致 |
| Bucket Sort (Arrays & Hashing) | 用 Frequency Counter 數頻率，建 Bucket Array（index=頻率），從後往前掃取 top k — O(n) 不用排序 |
| Length-Prefix (Arrays & Hashing) | 每個字串前面加「長度#」，decode 時讀數字往後數字元 — 靠長度不靠分隔符，什麼字元都不怕 |
| HashSet per row/col/box (Arrays & Hashing) | 三組 HashSet 分別追蹤 row、col、3x3 box 出現過的數字，掃一次棋盤就能查重複 |
| Sequence Start Detection (Arrays & Hashing) | 丟進 set，只從起點 (num-1 不在 set) 開始往上數連續長度，每個數字最多碰一次，O(n) |
| Converging Two Pointers (Two Pointers) | 左右兩個指標從兩端往中間走，邊走邊對稱比較，遇標點/非字元跳過 — O(n) 時間 O(1) 空間 |
| Two Pointers + Greedy (Two Pointers) | 從兩端逼近，每輪移動「較矮的指標」— 因為動較高的會讓寬縮、高度被矮的卡住，永遠不可能更好；可安全 prune 一大堆 pair — O(n) 時間 O(1) 空間 |
| Two Pointers + Bounded Computation (Two Pointers) | 每位置水量 = `min(left_max, right_max) - h[i]`；左右指標逼近，每輪動較矮側並算水 — 較高側保證有牆，較矮側水量瓶頸鎖在自己的 max，現在就能算 — O(n) 時間 O(1) 空間 |
| Prefix Maximum DP (通用) | 邊掃邊記累積 max（或 min/sum/count），下一格直接從上一格累積 + 自己這格推出來 — 把 O(n²) 重複計算壓到 O(n) — 是 DP 最簡形式 |
| Monotonic Deque (Sliding Window) | deque 存「可能當 max 的候選 index」呈遞減排列；新元素進場時把右邊比它小的 pop 掉、過期的從左 popleft，最左永遠是當前窗戶 max；每元素一生進出各一次 → O(n) 攤還 |

---

## Phase Gate Results

| Phase | Date | Problem Used | Score | Result | Weak spots |
|-------|------|-------------|-------|--------|------------|
| | | | | | |
