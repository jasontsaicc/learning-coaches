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
| **Current pattern** | Stack |
| **Language** | Python |
| **Session count** | 15 |
| **Last weekly review** | — |
| **Problems solved** | 13 / 136 |

---

## Current Session (Breakpoint)

> ✅ Session 15 完成 (2026-07-02) — Largest Rectangle in Histogram (#84) **Learn 模式** (Hard, NeetCode Stack 最後一題/大魔王)
> Pattern: **Monotonic Stack (遞增)** — 與 #739 完美鏡像 (pop 條件決定方向)
> Problem: #84 Hard — workspace/22, brute + stack 兩版 5/5 pass
>
> ✅ Warm-up 補結 #739 欠的 **O(n) 攤還債** (每 index 一進一出 → 總 pop ≤ n)
> ✅ Brute force **學生自己寫** (fill-in-the-blank 鷹架): 每根當最矮天花板往左右撞矮牆, `width=right-left-1`; 5/5 pass; 這次沒忘 return、max_area 初始化沒忘 (老坑未踩)
> ✅ 「A佔2/B佔1」深挖: 靈魂「撞比我矮的才停、比我高的可鑽過」自己想通; 排隊故事 (push/pop, 右牆=逼你離場的新人、左牆=pop 後新隊尾) 逐步建立
> 🟡 Stack optimal **code 是我給的** (學生累了+趕讀書會、主動要 code 直接看) → **未冷寫**, 下次要 cold re-do 才算 fluency 達標
> 🟡 過程數次「看不懂/太難了」→ 退回純白話故事 (排隊比喻) + 具體例子重建, 有效 (符合視覺 trace 學法)
> 🟡 Mock / 完整 Feynman gate / 教 Yuki closer 都**未做** (時間壓力), 下次補
> 📄 產出讀書會簡報: notes/pattern22-largest-rectangle-histogram.md (講稿) + .html (Fable 視覺版, CSS 長條圖 + 逐格 trace, 已交付)
>
> ⏭️ Next: ① **#84 stack cold re-do** (今天是看的、沒冷寫 → fluency 未達標) ② 教 Yuki (#84 + Car Fleet 兩筆欠) ③ Phase 0 Gate (Stack 6/6 完成可開) ④ Binary Search
> ⏸️ Weekly Review 嚴重到期 (≥15 session 未做)，強烈建議下次優先補
> ⏸️ Parked Feynman 債務 (Transfer Q2/Q3): #239 Sliding Window Maximum, #42 Trapping Rain Water, #11 Container With Most Water
> ⏸️ Queued: Sliding Window 基礎題 #121 / #3 (workspace/14 有 brute) / #567 (workspace/15 到 Step E)

---

## Topic Mastery (per Pattern)

| Pattern | Problems Done | Mastery | Phase Gate | Notes |
|---------|--------------|---------|------------|-------|
| Arrays & Hashing | 5/11 | 🟡 | — | Frequency Counter + Bucket Sort + Length-Prefix + HashSet per row/col/box + Sequence Start Detection learned. #238 (Product of Array Except Self) skipped, revisit later |
| Two Pointers | 2.5/5 | 🟡 | — | + #42 Trapping Rain Water (Hard) 三層算法全綠 (Brute/DP/Two Pointers 18/18) — 加分: 自抓 6 個 bug 全修對；扣分: Q2/Q3 Feynman 沒自答 (看答案)。升 🟢 條件: Day 3 完成 F + G |
| Sliding Window | 1/5 | 🟡 | — | #239 Sliding Window Maximum (Hard, jump-to 跳關做最難的第 6 題): Brute O(n·k) + Optimal Monotonic Deque O(n) 都親手寫過 12/12 tests; Feynman 只過 Q1 (O(n) amortized 講得出); Q2/Q3 + Mock 待補。基礎 5 題 (#121, #3, #424, #567...) 尚未做 |
| Stack | 6/6 | 🟢 | Phase 0 Gate | #20 + #150 + #155 + #739 + #853 + **#84 Largest Rectangle (Hard) ✅** = NeetCode Stack 全清 (Generate Parentheses 屬 backtracking 先跳). #84 stack code 是看的、**未冷寫** (下次 cold re-do). #739 O(n) 攤還債結清. 教 Yuki (#84 + Car Fleet) 待補 |
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
| 9 | Valid Parentheses | Stack | 分支動作放反：開括號該 `append`、閉括號該比對+`pop`，一度寫反 | ✅ Resolved (S9) |
| 9 | Valid Parentheses | Stack | 變數名手滑 `pairs`→`paris`→`pairss` (連三次) — **老毛病: 變數名逐字檢查** | 🟡 Recurring - 同 num/nums, window/windows 家族 |
| 9 | Valid Parentheses | Stack | `return` 寫死 `True`/`False` 來回反，正解是 `return not stack`（掃完空才有效）| ✅ Resolved (S9) |
| 11 | Evaluate RPN | Stack | `stack.append(int(token)` 少一個 `)` — append 的括號沒關 → SyntaxError | ✅ Resolved (S11) - 教訓: 從外往內寫, 打 `(` 先補 `)` |
| 11 | Evaluate RPN | Stack | 忘記 `return`（**第 4 次**, 同 Palindrome×2 + Container）— 症狀: 答案全 `None` | 🟡 Recurring - 反射: 看到 None 先查 return |
| 11 | Evaluate RPN | Stack | `return stack.pop()` 縮排進 `for` 迴圈內 → 只處理第一個 token 就回傳 | ✅ Resolved (S11) - **同 #42 縮排決定 block**; 症狀「只處理第一元素」先查縮排 |
| 11 | Evaluate RPN | Stack | 除法用 `l // r`（floor 向負無窮）→ 負數錯; 正解 `int(l / r)`（truncate 向 0） | ✅ Resolved (S11) - **新坑**: `//`≠砍小數, 是 floor; 面試常考 |
| 13 | Daily Temperatures | Stack (Monotonic) | `while stack is Not` — `is Not` 非 Python 語法, 空 list 本身 falsy | ✅ Resolved (S13) - 慣用語 `while stack:` |
| 13 | Daily Temperatures | Stack (Monotonic) | `stack.top` — Python list 沒有 `.top`; 頂端溫度要 `temperatures[stack[-1]]` | ✅ Resolved (S13) - 存 index 回查溫度 |
| 13 | Daily Temperatures | Stack (Monotonic) | `stack.append(i)` 縮排進 while → 每 pop 一次就 append, stack 清不完 | ✅ Resolved (S13) - append 與 while 平行 (這天最後才排隊) |
| 13 | Daily Temperatures | Stack (Monotonic) | `answes[prev]` 變數名手滑 | 🟡 Recurring - 同 num/nums, paris, window/windows 家族 |
| 13 | Daily Temperatures | Stack (Monotonic) | cold solve `stack, append(i)` 逗點⇄點 → NameError; **自讀錯誤訊息抓出來修好** | 🟡 Recurring - 字元精準度; 但 debug 反射 ✅ 養成中 |
| 13 | Daily Temperatures | Stack (Monotonic) | Yuki 拷問盲點: 把「while 不執行」誤歸因成「ans 初始化=0」(真因是溫度條件為假, 與答案值無關); 攤還 O(n) 需動畫才懂 | 🟡 Re-test (+3d) - 抽問: ① while條件 vs 答案值是兩條獨立線 ② 攤還「每元素一生 pop 一次 → 總 pop ≤ n」 |
| 13 | Daily Temperatures | Stack (Monotonic) | Yuki spot-my-bug: 縮排雷達對 (聞到 return 區塊有問題) 但**指錯行** — 指 `stack.append(i)`(其實對的), 真兇是 `return answer` 卡在 for 內 | 🟡 Re-test (+3d) - 抓蟲下刀要精準到「行」; 方法: 每行問「這動作該做幾次」每圈的留 for 內、只做一次的踢出去 |
| 14 | Car Fleet | Stack + Sort | `if` 開頭行結尾少冒號 `:` | 🟡 Recurring - 同 #42; 反射: 寫完 if/for/while/def 先補 `:` |
| 14 | Car Fleet | Stack + Sort | 邏輯反: 寫 `if stack`(=stack有東西) 但本意「stack 空」應 `not stack`; 且空 stack 時 `stack[-1]` 會 IndexError → `not stack` **必須排第一個**短路才不會爆 | 🟡 Re-test (+3d) - 抽問: ① `if stack:` 是空還是有東西? ② 為什麼 `not stack` 要放 `or` 的左邊 (短路保護 stack[-1]) |
| 14 | Car Fleet | Stack + Sort | `stack.push()` — Python list 沒 `.push` 應 `.append`; 且括號內空的, 要 `stack.append(time)` | 🟡 Recurring - 同 #739 `.top` 錯方法名家族 |
| 14 | Car Fleet | Stack + Sort | (WIN 非錯誤) `cars.sort` 一度縮排在 for 內 → 自己抓出移到外面 | ✅ 老毛病 #42/#150/#739 縮排家族, 這次**自救成功** |
| 15 | Largest Rectangle | Stack (Monotonic) | 時間複雜度反射成 `n log n` (真相 n×n=**n²**); **第 2 次亂加 log** (S1 排序記成 O(log n)) | 🟡 Re-test (+3d) - 抽問: 有砍半/排序才有 log; 巢狀線性掃是相乘 = n² |
| 15 | Largest Rectangle | Stack (Monotonic) | 猜 stack 是「遞減」(其實**遞增**); 沒連結「pop 條件決定方向」 | 🟡 Re-test (+3d) - 抽問: pop「更矮」→遞增、pop「更大」→遞減 (#739 完美鏡像) |
| 15 | Largest Rectangle | Stack (Monotonic) | 右邊界 guard 鏡像錯: 寫 `right <= 0` (把左界的 0 直接抄過來), 應 `right < n` | ✅ Resolved (S15) - 左界 index 0、右界 index n-1 (`< n`) |

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
| Stack 配對 (Stack) | 巢狀結構「最後開的最先關」= FILO；開括號 push、閉括號比對 stack 頂端配不配 (不配/空→False) 再 pop，掃完 stack 空才有效；計數器只管數量會漏型別+順序 (`([)]`)，所以要 Stack — O(n) 時間 O(n) 空間 |
| Stack 後綴求值 / RPN (Stack) | 數字 push 進 stack、運算子來就 pop 兩個 (先 pop=右、後 pop=左, FILO 鏡像) 算完 push 回去，掃完 stack 剩一個=答案；判運算子用白名單 (4 個固定) 別用 isdigit (負數會誤判)；除法 `int(l/r)` 向 0 取整非 `//` — O(n) 時間 O(n) 空間 |
| Monotonic Stack (Stack) | 維護「遞減的等待區」存還沒等到更大值的 index；新元素把頂端比它小的全 pop 掉並結算 (距離 = i - prev) 再 push 自己；存 index 不存值 (要算距離, 用 `temperatures[stack[-1]]` 回查)；每個 index 一進一出 → **O(n) 攤還** (同 #239 deque 論證) — O(n) 時間 O(n) 空間 |
| Largest Rectangle in Histogram (Stack) | 每根長條問「當最矮高度能拉多寬」= 往左右撞到比它矮的牆才停 (比它高的可鑽過去); 單調**遞增** stack 存 index, 新來的比隊尾矮就把高的 pop 結算 (**右牆 = 逼你離場的新人 i、左牆 = pop 後新隊尾 `stack[-1]`, 空則 -1**), `width = 右-左-1`, `area = heights[top]×width`; 收尾剩的右牆當 n; 每 index 一進一出 → **O(n) 攤還** (同 #739); pop「更矮」→遞增, 對比 #739 pop「更大」→遞減 = 完美鏡像 — O(n) 時間 O(n) 空間 |
| Stack + Sort 車隊 / Car Fleet (Stack) | `zip(position,speed)` 綁成車、按位置由大到小排 (靠終點先處理)；從前往後掃, 每台算到達時間 `(target-p)/s`, 比 stack 頂端**慢** (`time > stack[-1]`) → 追不到 → push 一坨新車隊, 否則被前面那坨吸收 (不動)；`len(stack)` = 車隊數；**只看頂端、從不 pop** (後車不可能讓前車消失) → 不用內層 while, 單向 for 即可 (跟 #739 monotonic stack 的差別); 其實一個變數記頂端就夠, stack 只是讓 len 數答案更直覺 — O(n log n) 時間 (排序主導) O(n) 空間 |

---

## Phase Gate Results

| Phase | Date | Problem Used | Score | Result | Weak spots |
|-------|------|-------------|-------|--------|------------|
| | | | | | |
