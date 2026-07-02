# Sliding Window Maximum (#239) — Hard

> Pattern: Sliding Window + Monotonic Deque（單調遞減雙端佇列）
> Session 8 · jump-to（讀書會分享）· 2026-05-28

---

## Pattern 摘要

> 用一個「單調遞減 deque」存**還可能成為 max 的候選人 index**：新元素進場時把右邊比它小的全踢掉（pop），最舊的滑出窗戶就從左邊踢掉（popleft），deque 最左邊永遠是當前窗戶的 max。每個元素一生最多進出 deque 各一次 → O(n)。

---

## 解法 (Approach)

### 暴力法 (Brute Force) — Time O(n·k), Space O(k)
對每個窗戶位置 `i`（共 `n-k+1` 個），用 slicing 取出 k 個元素，再用 `max()` 掃一遍找最大值。**問題**：每個窗戶都從零重掃，但相鄰窗戶其實重疊 `k-1` 個元素，做了大量重複工作。`k=5000` 時 `O(n·k) ≈ 5億次` → **TLE**。

### 最佳解 (Optimal) — Time O(n), Space O(k)
維護一個 **monotonic decreasing deque**，裡面存 **index**（不是值）：
1. **POPLEFT（清過期）**：最左 index 滑出窗戶（`dq[0] <= i - k`）→ 踢掉
2. **POP RIGHT（清小弟）**：最右的值比新元素小（`nums[dq[-1]] < nums[i]`）→ 踢掉
3. **APPEND（新人進場）**：把當前 index `i` 加到右邊
4. **READ（記答案）**：窗戶滿了（`i >= k-1`）→ `nums[dq[0]]` 就是 max

### 關鍵洞察 (Key Insight)
**「舊 + 小」的元素永遠不可能成為 max**：當更大的新元素還在窗戶時輪不到它，等大元素離開時它早就先離開了（index 更小先過期）。所以可以安全丟掉，deque 自然維持遞減。
**O(n) 的原因（Amortized Analysis）**：每個元素一生最多被 append 一次、被 pop/popleft 一次，總操作 ≤ 2n。雖然 for 裡套了 2 個 while，但所有 while 加總一輩子最多跑 2n 次。

---

## 💻 My Code

```python
from typing import List
from collections import deque


# Brute Force — O(n*k) time, O(k) space
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        result = []

        for i in range(n - k + 1):
            window = nums[i : i + k]
            current_max = max(window)
            result.append(current_max)

        return result


# Optimal — Monotonic Deque, O(n) time, O(k) space
class SolutionOptimal:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        result = []
        dq = deque()  # stores INDICES; values are monotonically decreasing

        for i in range(n):
            # 1. POPLEFT — drop leftmost index if it fell out of the window
            while dq and dq[0] <= i - k:
                dq.popleft()

            # 2. POP RIGHT — drop smaller values from the right
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()

            # 3. APPEND — add current index
            dq.append(i)

            # 4. READ — once the window is full, record the max
            if i >= k - 1:
                result.append(nums[dq[0]])

        return result
```

---

## 🧠 心智模型：Deque = 「等當國王（max）的候選人名單」

```
deque: [國王, 太子, 太孫, ...]   ← 左大右小（遞減）
        ↑
     最左 = dq[0] = 現任國王 = 當前 max

規則1（pop右）：新人來了，打趴所有比他弱的小弟（右邊）
規則2（popleft左）：國王只有「滑出窗戶」才退位，沒事不換人
```

**動畫驗證**（`nums=[1,3,-1,-3,5,3,6,7], k=3`）：

```
        dq（工具，一直變）        result（答案，只增加）
i=2:    [3, -1]                  [3]
i=3:    [3, -1, -3]              [3, 3]
i=4:    [5]          ← 大洗牌    [3, 3, 5]   (3過期popleft + -1,-3被pop)
i=7:    [7]                      [3, 3, 5, 5, 6, 7]  ← return result
```

---

## ⚡ Edge Cases

- **單一元素** `nums=[7], k=1` → `[7]`
- **窗戶 = 陣列長度** `nums=[5,2,9], k=3` → `[9]`（只有 1 個窗戶）
- **嚴格遞減** `nums=[9,8,7,6,5], k=3` → `[9,8,7]`（deque 會裝滿，最左永遠是 max）⚠️ 這個 case 證明「不能盲目 popleft」
- **嚴格遞增** `nums=[1,2,3,4,5], k=3` → `[3,4,5]`（每次新人都打趴全部，deque 永遠只有 1 個）
- **負數**：本題值可為負，`nums[dq[-1]] < nums[i]` 比較照樣成立（沒有用 0 當初始值的陷阱）

---

## 🔴 我的錯誤

### A. 語法 / 變數名稱（同一家族錯誤，踩了 4 次）

| 我寫的 | 正確 | 為什麼錯 |
|--------|------|----------|
| `num[i:i+k]` | `nums[i:i+k]` | 參數叫 `nums`，少一個 `s` → NameError |
| `windows` | `window` | 單複數不一致 → NameError |
| `nums[in]` | `nums[i]` | `in` 是 Python 保留字（IDE 自動補全害的）→ SyntaxError |
| `dq.append(import)` | `dq.append(i)` | `import` 是保留字（IDE 自動補全）→ SyntaxError |

> **教訓**：打完 `i` 不要按 Tab/Enter（會被補成關鍵字）。debug NameError 第一步：對著參數名「逐字比對」。

### B. 觀念誤解

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| Sliding Window「用指針 **或** deque」二選一 | 指針管「窗戶在哪」、deque 管「裡面 max 是誰」，**兩者並存** | Sliding Window 是策略不是實作，工具隨「要算什麼」而變 |
| 每次窗戶滑動「直接 popleft 最左邊」就好 | 只有最左 index **真的過期**（`dq[0] <= i-k`）才 popleft | deque 裝的是候選人不是整個窗戶，最左邊通常就是 max，盲目踢=丟答案 |
| 窗戶 `[1,3,-1]` 裡 `-1` 也可以丟 | `-1` 是最新的，**不能丟**（可能熬出頭當未來 max） | 規則是單方向：只有「舊+小」能丟，「新+小」要留著當保險 |
| `current_max = max(current_max, window)` | `current_max = max(window)` | 每個窗戶 max 是**獨立**的，不是跨窗戶累積最大值 |
| 相鄰窗戶「不變 k 個」 | 不變 `k-1` 個（進1、出1） | 窗戶大小 k，重疊部分是 k-1 |
| Brute force「每個窗戶排序」 | 只要 `max()` 掃一遍（O(k)），不用排序（O(k log k)） | 只需要最大值，排序是做了多餘的工作 |

---

## ❓ 我的疑問（已解決）

| 疑問 | 答案重點 |
|------|----------|
| 什麼是 deque？ | 雙端佇列，兩端進出都 O(1)，內部是 doubly linked list |
| 為什麼用到 linked list？ | Python deque 內部 = doubly linked list，所以「左邊進出」也是 O(1)（list 的 `pop(0)` 是 O(n)） |
| `for i in range(n)` 為什麼不是 `range(n-k+1)`？ | optimal 的 `i` 是「新元素進場」計數，每個元素都要進場一次 → `range(n)`；brute 的 `i` 是「窗戶起點」 → `range(n-k+1)` |
| `dq[0] <= i - k` 什麼意思？ | `dq[0]`=最舊 index，`i-k`=過期邊界，問「最左的國王滑出窗戶了沒」。`dq and ...` 是短路保護避免空 deque 取 `dq[0]` 爆 IndexError |
| 為什麼不能每次踢左邊？ | 最左邊常常就是 max，沒過期就踢=丟答案（嚴格遞減 case 第一個窗戶就會錯） |
| `nums[dq[-1]]` 為什麼是 `-1`？ | Python 負索引，`dq[-1]`=最右=最新=deque 裡最小值。pop 右邊要比「值」所以包 `nums[...]`（deque 存的是 index） |
| return 是 dq 嗎？ | **不是**，return `result`。dq 是工具（草稿紙，裝 index），result 是答案（裝每個窗戶的 max 值） |

---

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "The brute force is to slide a window of size k and take the max of each window, which is O(n·k). That's too slow when k is large. I'll use a **monotonic decreasing deque** that stores indices of candidate maxima, which brings it down to O(n)."

**Core idea:**
> "The key insight is that if an element is both **older and smaller** than another, it can never be the max — the bigger one beats it now, and it leaves the window first anyway. So I keep the deque decreasing: when a new element comes in, I pop all smaller elements from the right, then append it. The front of the deque is always the current window max."

**Two removals (be explicit — interviewers love this):**
> "There are two different removals: I `popleft` from the front when the leftmost index falls out of the window (`dq[0] <= i - k`), and I `pop` from the back while the back's value is smaller than the new element. I store **indices, not values**, because I need the index to check expiry."

**Optimization / complexity:**
> "It's O(n) by amortized analysis: each element is appended once and removed at most once, so total deque operations are bounded by 2n — even though there are nested while loops."

**Edge cases:**
> "I'd check k=1 (returns the array itself), k equal to array length (one window), and a strictly decreasing array, which is the case that proves you can't just always popleft."

---

## Cross-Verification TODO
> 上 NeetCode / LeetCode discussion 看別人的寫法。重點看：有人用 `<=` 而非 `<` 在 pop right（處理重複值時 deque 更小，但答案一樣對）。下次帶來討論。
