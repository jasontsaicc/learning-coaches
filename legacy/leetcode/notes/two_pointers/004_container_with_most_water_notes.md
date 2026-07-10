# Container With Most Water (LeetCode 11) — Two Pointers

> **Session 7 (2026-05-07, Day 1)** — Steps A→F Q1 完成 ✅，Q2 + Mock + 收尾留 Day 2

---

## Pattern 摘要

> **Two Pointers (Converging + Greedy)：從兩端往中間逼近，每輪移動較矮的指標 — 因為移動較高的指標寬度變小、高度被矮的卡住，永遠不可能更好。O(n) 時間、O(1) 空間。**

---

## 解法 (Approach)

### 暴力法 (Brute Force)
窮舉所有 `(i, j)` pair，計算每組的水量，追蹤最大值。

- **公式：** `area = (j - i) × min(height[i], height[j])`
- **Time：** O(n²) — 雙層 loop
- **Space：** O(1) — 只有幾個固定變數

### 最佳解 (Optimal — Two Pointers Converging + Greedy)
左右兩端各放一個指標，每輪算當下的水量，更新 `max_area`，然後**移動較矮的那根**。

- **Time：** O(n) — 兩根指標總共最多走 n 步
- **Space：** O(1)

### 關鍵洞察 (Key Insight)
**為什麼動矮的、不動高的？**

- 每輪不管動誰，**寬度一定變小**（往中間靠）
- 動高的：高度仍被矮的卡住 (min) → 寬縮、高不變或變更小 → **面積一定變小**
- 動矮的：賭後面有更高的線 → 高度可能變高 → **有機會贏**

→ 所以「動矮的」才是有意義的選項；動高的可以**直接剪枝（prune）**。

---

## 💻 My Code

```python
# Brute Force — O(n²) time, O(1) space
class Solution:
    def maxArea(self, height: list[int]) -> int:
        maxarea = 0
        n = len(height)
        for i in range(n):
            for j in range(i + 1, n):
                area = (j - i) * min(height[i], height[j])
                if area > maxarea:
                    maxarea = area
        return maxarea


# Optimal: Two Pointers (Converging + Greedy) — O(n) time, O(1) space
class SolutionOptimal:
    def maxArea(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_area = 0
        while l < r:
            area = (r - l) * min(height[l], height[r])
            max_area = max(max_area, area)
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_area
```

---

## ⚡ Edge Cases

- ✅ `[1, 1]` (n=2 最短陣列) → 1
- ✅ `[4, 3, 2, 1, 4]` (兩端最高) → 16
- ✅ `[1, 2, 1]` (中間最高) → 2
- ✅ `[0, ...]` (允許高度為 0) — constraints 明示 `0 <= height[i]`
- ⚠️ 不會出現負高度（constraint 卡死最小是 0，**不要被「直覺」誤導去想負數**）
- ⚠️ 全部一樣高的陣列 (e.g. `[3,3,3,3]`) → 取最寬 → `3 × (n-1)`

---

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| Edge cases 想到「負數」就是有想到了 | constraints 寫 `0 <= height[i]` 已經卡死，不會有負數 | **沒對照 constraints 列 edge cases**，直覺亂猜 |
| `area = if (j - i) * min(...)` 可以這樣寫 | Python 中 `if` 是 statement 不能當 expression（不像 Rust）| 把賦值跟條件判斷混在同一行 |
| `l++` / `r--` (C/Java 寫法) | Python **沒有** `++` `--` 運算子 | 直接套其他語言肌肉記憶 |
| `l = l += 1` 兩個運算子可以合用 | 語法錯誤 — 二選一就好（`l = l + 1` 或 `l += 1`）| 把不同寫法混合在一起 |
| `while l > r:` (Two Sum II 的延伸) | 應該是 `l < r`（沒撞到就繼續）| 沒有用實際數字 trace 驗證 |
| `max_area = max(max_area, area)` 寫之前不用先初始化 | Python 看到右邊的 `max_area` 找不到變數會 NameError | 忘記變數要先生出來才能讀取 |
| if 條件留 `...` 就好 | `...` 是 Python 的 Ellipsis，會永遠 truthy（else 永遠不跑）| 留佔位符忘記填邏輯 |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd approach this with **Two Pointers — converging from both ends**. The key insight is that the water area is bounded by the shorter line (`min(h[l], h[r])`), so the shorter line is the bottleneck."

**Brute Force first (always mention):**
> "Brute force would try every pair `(i, j)` — O(n²) time. For each pair, area = `(j - i) * min(h[i], h[j])`. We track the max."

**Optimization (the meaty part):**
> "We can do **O(n)** with two pointers. Start `l` at 0, `r` at `n-1`. Each iteration, compute the area, update `max_area`, then move the **shorter pointer** inward. We **never move the taller one** — here's why: width always shrinks, and the height is bottlenecked by the shorter line, so moving the taller pointer can only make area shrink or stay the same. We **prune** all those pairs safely."

**Complexity:**
> "Time **O(n)** because each pointer moves at most `n/2` steps, total `n`. Space **O(1)** — just a few variables, independent of input size."

**Edge cases:**
> "Constraints say `n >= 2` and `height[i] >= 0`, so the smallest input is two non-negative lines. I'd test `[1,1]`, `[4,3,2,1,4]` (max at endpoints), and `[1,2,1]` (max in middle) to verify."

**Follow-up readiness:**
> "If asked to **return the indices** (not just the area), I'd switch from `max(...)` to an explicit `if area > max_area:` so I can capture `l, r` at the moment of update — `max()` doesn't tell us when the value actually changed."

---

## 🧠 Take-Aways（Day 1 學到的通用觀念）

1. **Big-O 是「總工作量」不是「單次操作」**
   Two Pointers 每輪只動一根，但**兩根加起來最多 n 步** → O(n)。
   Aggregate Analysis 的概念，後面 Sliding Window、Linked List 都會用。

2. **Python 沒有 `++` 跟 `--`**
   永遠用 `+= 1` 跟 `-= 1`。這是 Python 跟 C/Java/JS 最大的語法差異之一。

3. **追值 vs 追值 + 伴隨資料**
   - 只追值 → `max(x, new)` 一行
   - 追值 + 伴隨（例如 index）→ 必須用 `if` 才能抓到「更新瞬間」

4. **寫 code 之前先用白話講一遍**
   Pseudocode 階段抓 bug 比 Python 階段便宜 10 倍 — 今天靠這個習慣抓出 4 個 bug。

5. **Edge cases 要「對照 constraints」推導**
   不要憑直覺亂猜（例如「會不會有負數？」） — 看 constraint 已經寫了什麼。

---

## 📋 Day 2 待辦（明天 Session 7 接續）

- [ ] **Step F Q2** — Constraint Change：如果公式從 `min` 改成 `max`，Greedy 還對嗎？為什麼？
- [ ] **Step G** — Mock Interview（變題 + Scorecard）
- [ ] **Step H** — 補完 Notes 的 Mock 心得
- [ ] **Step I** — 更新 progress.md（mastery 升級、session count +1）
- [ ] **回頭收 Two Sum II (#167) Step E** — 修 `l + 1` / `r + 1` 那 bug
