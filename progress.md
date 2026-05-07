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
| **Session count** | 6 |
| **Last weekly review** | — |
| **Problems solved** | 6 / 136 |

---

## Current Session (Breakpoint)

> 🔄 Session 7 paused (2026-05-07, 待 2026-05-08 接續)
> Problem: Container With Most Water (#11) — jump-to (NeetCode 150)
> Pattern: Two Pointers (Converging + Greedy decision)
> Current step: F (Feynman Gate) — Q1 (Variation) ✅ 過, Q2 (Constraint Change: max instead of min) ⏸️ 待答
>
> 已完成今天: A (Review) → B (Read Problem) → C (Pattern Teaching) → D (Brute Force, 4/4 tests pass) → E (Optimal, 4/4 tests pass) → F Q1
> 明天接續: F Q2 → G (Mock Interview) → H (Notes) → I (Progress Update)
>
> ⏸️ Parked: Two Sum II (#167) Step E — optimal 版有 bug：`l + 1` / `r + 1` 沒寫成 `l += 1` / `r -= 1`，下次回來修

---

## Topic Mastery (per Pattern)

| Pattern | Problems Done | Mastery | Phase Gate | Notes |
|---------|--------------|---------|------------|-------|
| Arrays & Hashing | 5/11 | 🟡 | — | Frequency Counter + Bucket Sort + Length-Prefix + HashSet per row/col/box + Sequence Start Detection learned. #238 (Product of Array Except Self) skipped, revisit later |
| Two Pointers | 1.5/5 | 🟡 | — | Converging Two Pointers learned via Valid Palindrome (sharing talk); Container With Most Water Day 1 完成 (Greedy + prune 概念抓到, Day 2 收 Q2 + Mock); Two Sum II Step E parked |
| Sliding Window | 0/5 | ⬜ | — | |
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

---

## Phase Gate Results

| Phase | Date | Problem Used | Score | Result | Weak spots |
|-------|------|-------------|-------|--------|------------|
| | | | | | |
