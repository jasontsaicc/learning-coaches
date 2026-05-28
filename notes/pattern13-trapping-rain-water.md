# Trapping Rain Water (LeetCode 42) — Two Pointers + Bounded Computation

> **Session 7 (2026-05-08, Day 2)** — Steps A→F (partial) + H 完成 ✅，Step G (Mock) 留 Day 3
>
> **Difficulty: Hard** — 三層算法階梯全攻克 (Brute → DP → Two Pointers)

---

## Pattern 摘要

> **每個位置的水量被「左邊最高的牆」和「右邊最高的牆」中較矮的那個鎖住：`water[i] = min(left_max, right_max) - height[i]`。Two Pointers 最佳解：從兩端向中間，每輪動較矮側並算水（因為較高側已保證有牆，較矮側水量現在就能算）。O(n) 時間 O(1) 空間。**

---

## 三層解法階梯

### Level 1：Brute Force — O(n²) time, O(1) space

對每個位置 `i`，用 `max(height[:i+1])` 和 `max(height[i:])` 即時算左右最高，加總水量。

- **Time：** O(n²) — 外層 for n × 內層 max() 掃 n
- **Space：** O(1) — 沒有額外陣列
- **重複代價**：每一輪 max 都掃過之前看過的元素

### Level 2：DP / Precompute — O(n) time, O(n) space

預先建兩個陣列 `left_max[]`、`right_max[]`，再一次掃描加總。

- **Time：** O(n) — 三個 single pass
- **Space：** O(n) — 兩個陣列
- **遞推式 (Recurrence)：**
  - `left_max[i] = max(left_max[i-1], height[i])` (從左掃)
  - `right_max[i] = max(right_max[i+1], height[i])` (從右掃)
- **核心 idea：** 用空間換時間 — 把重複計算的 prefix max 存起來

### Level 3：Two Pointers — O(n) time, O(1) space ⭐ Optimal

左右兩指標逼近，只追蹤兩個 scalar `left_max` 和 `right_max`，每輪動較矮側。

- **Time：** O(n) — 兩指標加起來最多走 n 步
- **Space：** O(1) — 只有 5 個 scalar (l, r, left_max, right_max, total)
- **核心 Insight：** 較矮那側的水量現在就能算，因為較高那側保證了至少這麼高的牆

---

## 🔑 三大關鍵 Insights

### Insight 1：水位被「兩邊最高牆中較矮的」鎖住

```
water[i] = min(left_max, right_max) - height[i]
           └────水位上限────┘    └自己佔的空間┘
```

物理直覺：水會從較矮的牆**溢出**。較矮牆 = 水位天花板。

### Insight 2：矮 bar 不擋水（連通性）

中間的小 bar 即使比水位矮，也**不會把水切斷**。水形成連通水池，水面平在 `min(left_max, right_max)`。矮 bar 只是「池底凸起」，佔走它頭頂上方那塊水。

### Insight 3 ⭐：較矮側水量「現在就能算」

當 `height[l] < height[r]`：
- 真正的 right_max（位置 l 看右邊）≥ height[r]（因 r 在右側）
- 所以 right_max **保證 > height[l]** → 瓶頸不是 right_max
- 瓶頸鎖在 left_max → 水量 = `left_max - height[l]`，**不需要知道 right_max 真實值**
- 動 l 前進、繼續

→ **這就是 Two Pointers 把 O(n) space 壓到 O(1) 的關鍵**

---

## 💻 My Code

### Brute Force — O(n²) time, O(1) space

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        total = 0
        for i in range(len(height)):
            left_max = max(height[: i + 1])
            right_max = max(height[i:])
            total += min(left_max, right_max) - height[i]
        return total
```

### DP / Precompute — O(n) time, O(n) space

```python
class SolutionDP:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        # Step 1: build left_max[]
        left_max = [0] * n
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Step 2: build right_max[]
        right_max = [0] * n
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Step 3: sum up water
        total = 0
        for i in range(n):
            total += min(left_max[i], right_max[i]) - height[i]
        return total
```

### Two Pointers — O(n) time, O(1) space ⭐

```python
class Solution2P:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        l, r = 0, n - 1
        left_max, right_max = 0, 0
        total = 0

        while l < r:
            if height[l] < height[r]:
                if height[l] >= left_max:
                    left_max = height[l]
                else:
                    total += left_max - height[l]
                l += 1
            else:
                if height[r] >= right_max:
                    right_max = height[r]
                else:
                    total += right_max - height[r]
                r -= 1
        return total
```

---

## ⚡ Edge Cases

- ✅ `[1]` (單元素) → 0（left_max == right_max == 自己）
- ✅ `[0, 0, 0]` (全平) → 0（沒牆 = 沒容器）
- ✅ `[3, 3, 3]` (同高) → 0（有牆但無凹槽）
- ✅ `[5, 4, 3, 2, 1]` (嚴格遞減) → 0（單調無凹）
- ✅ `[5, 0, 1, 0, 3]` 複雜地形 → 8
- ⚠️ Constraints: `0 <= height[i] <= 10^5` — **不允許負數**
  - 如果允許負數，`left_max = 0` 初始值會壞掉（見 Q3 Feynman 答案）

---

## 🔴 我的錯誤 (Session 7 Day 2)

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| `for i in range(len(height)) - 1` 可以這樣寫 | `range()` 回傳 range object，不能直接 -1；且本意是 `range(len(height))` 不要 -1 | 把「想表達的範圍」混入 range() 內外 |
| `for` 結尾不用 `:` | Python `for/if/while/def` 結尾**一定**要 `:` | 還沒鎖死 Python 區塊規則 |
| `total += ...` 不用先初始化 | Python 看到右邊找不到 `total` 會 NameError | 變數要先生出來才能讀（同 #11 的 max_area 教訓） |
| `min(left_max[i], right_max[i] - height[i])` | `)` 位置決定語意 — `min` 的兩個 arg vs 「先 min 再減」 | **括號決定優先順序**，Python 嚴格按括號分組 |
| 右邊分支只寫 if (沒寫 else 加水) | 鏡像對稱要求 if-else 兩條規則都有 | 對稱性沒做完整 |
| `r -= 1` 縮排跟 `else:` 同層 | 應該在 else block **內部**（多縮 4 格）— 不然每輪都 -1 | **縮排決定 block 範圍**，是 Python 語法不是裝飾 |
| Q2/Q3 Feynman 沒自答 (要看答案) | 🟡 應該能講出單調陣列 = 無水、`left_max=0` 在負數 input 會壞 | 學完 code 沒做 Transfer 練習 — 明天 Step A 重抽 |

---

## 🎤 How to Say It in Interview

### Opening (30 sec)
> "I'd approach this with **Two Pointers + Bounded Computation**. The key formula is: water at position i = `min(left_max, right_max) - height[i]` — bounded by the shorter of the two surrounding maxes. The Two Pointers trick moves the shorter side first, which lets us compute its water immediately without knowing the full other side's max."

### Brute Force (always mention)
> "Brute force: for each i, scan left for max and scan right for max. O(n²) time, O(1) space. Works but slow."

### DP / Precompute step
> "Optimization 1: precompute `left_max[]` and `right_max[]` arrays in two single passes. The recurrence is `left_max[i] = max(left_max[i-1], height[i])`. Then a third pass sums up water. Now we're O(n) time, O(n) space."

### Two Pointers (the meaty part)
> "Optimization 2: I can drop the arrays. Two pointers `l, r` from both ends, plus two scalars `left_max, right_max`.
>
> The insight is: when `height[l] < height[r]`, the right side has a wall of at least `height[r]`, which is taller than `height[l]`. So whatever water sits at position `l`, the bottleneck is `left_max`, not `right_max`. I can compute water at `l` immediately as `left_max - height[l]`, then move `l` forward.
>
> Symmetric on the right when `height[l] >= height[r]`. O(n) time, **O(1) space.**"

### Complexity
> "Time O(n) — each pointer moves at most `n/2` steps. Space O(1) — five scalars total."

### Edge cases
> "I'd test `[1]` (single bar = 0 water by definition), `[0,0,0]` (no walls, no container), `[3,3,3]` (walls but no valley), and `[5,4,3,2,1]` (strictly decreasing — no right wall ever taller, so 0 water)."

### Follow-up readiness
> "If `height[i]` could be negative, my code breaks because I init `left_max = 0`. I'd need to init to `float('-inf')` or to `height[0]` so the first iteration always triggers the update branch."

---

## 🧠 Take-Aways (今天學到的通用觀念)

1. **DP 的最簡形式 = Prefix Max**
   邊掃邊記累積統計量（max / min / sum / count），下一格直接用上一格結果。任何「對每個位置算它左右某種統計」的題都可能用上。

2. **空間換時間 vs 兩個都省：分階段優化**
   Brute O(1) space → DP O(n) space → Two Pointers O(1) space。最佳解不一定一步達到，**先換時間，再壓空間**。Two Pointers 是「優化的優化」。

3. **括號和縮排是 Python 的硬語法**
   - `min(a, b - c)` ≠ `min(a, b) - c` — 括號分組改變語意
   - 縮排決定 block 範圍 — `r -= 1` 在 `else:` 內 vs 平行差很多
   - Python 比 C/Java 對縮排更嚴格

4. **連通水池的物理直覺**
   矮 bar 不切水，水位看「兩邊牆中較矮的」。這個觀念在「陷阱題」（如水壩、城市天際線、容器類）反覆出現。

5. **較矮側 = 可決定側 (Two Pointers + Bounded)**
   面試金句：「較高側給了一個保證，較矮側現在就能下決定」。這個「**對稱資訊不對等**」的 insight 是 Two Pointers 的核心精神，#11 #42 都靠它。

6. **Constraints 是初始值的根據**
   `left_max = 0` 在「heights ≥ 0」是合理 sentinel；放寬約束後就不再合理。**改 constraint = 重新檢查初始化**。

---

## 🔄 Day 3 (明天) 接續事項

- [ ] **Step A 重抽 Q2 / Q3 Feynman** — 確認單調陣列與負數 constraint 變化能自答
- [ ] **Step G (Mock Interview)** — 用變題 + Scorecard
- [ ] **回頭收 Two Sum II (#167) Step E** — 修 `l + 1` / `r + 1` bug
- [ ] **回頭收 Container With Most Water (#11) Day 2** — Step F Q2 (max 變體) + Mock + Notes 收尾
