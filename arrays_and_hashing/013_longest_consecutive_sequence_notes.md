# Longest Consecutive Sequence (128)
> Pattern: Arrays & Hashing (HashSet + Sequence Start Detection)
> Date: 2026-04-14 | Session: 5 (jump-to, 預習)

## Pattern 摘要
> 把所有數字丟進 set，只從「起點」(num-1 不在 set) 開始往上數連續長度，每個數字最多被碰一次，O(n)。

## 解法 (Approach)

### Brute Force: 排序 + 掃描
- 排序後掃一遍，相鄰差 0 跳過、差 1 加一、差 > 1 重設
- Time O(n log n) / Space O(n)

### Optimal: HashSet + Sequence Start Detection
- 所有數字丟進 `set(nums)` — O(n) 建立，O(1) 查詢
- 掃每個數字，`num - 1 not in numSet` → 這是起點
- 從起點往上 while 數到斷掉，追蹤 max
- **Time O(n) / Space O(n)**
- 關鍵洞察：每個數字最多被「碰」兩次（一次判斷起點、一次被 while 數到），所以是 O(n) 不是 O(n^2)

## 💻 My Code

### Brute Force
```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        counter = 1
        max_len = 1
        if not nums:
            return 0

        sort_num = sorted(nums)
        for i in range(1, len(sort_num)):
            if sort_num[i] - sort_num[i - 1] == 0:
                continue
            elif sort_num[i] - sort_num[i - 1] == 1:
                counter += 1
                max_len = max(max_len, counter)
            else:
                counter = 1
        return max_len
```

### Optimal
```python
class SolutionOptimal:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        max_len = 0

        for num in numSet:
            if num - 1 not in numSet:
                length = 1
                while num + length in numSet:
                    length += 1
                max_len = max(max_len, length)

        return max_len
```

## ⚡ Edge Cases
- `nums = []` — 回傳 0
- `nums = [5]` — 只有一個數字，回傳 1
- `nums = [1,1,1,1]` — 重複不算連續，回傳 1（set 自動去重）
- 負數 — 一樣適用，`-3, -2, -1` 也是連續序列

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| `counter = {}` 用 dict 追蹤計數 | counter 就是一個整數 `counter = 1` | 搞混「計數器」和「資料結構」 |
| `=` 和 `==` 混用（第四次） | `=` 是賦值（給），`==` 是比較（問） | 口訣：一個等號「給」，兩個等號「問」 |
| `counter += i-1` 加 index | `counter += 1` 每次固定加 1 | i 是位置，不是要加的量 |
| `couter` 拼錯 | `counter` | 注意拼字 |
| 起點是「前面有值的」 | 起點是「前面沒有值的」(num-1 not in set) | 邏輯反了，前面沒人 = 你是第一個 = 起點 |

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd put all numbers into a HashSet for O(1) lookup. Then I iterate through the set — for each number, I check if it's the start of a sequence by verifying num-1 is NOT in the set. If it is a start, I count consecutive numbers going up."

**Why O(n):**
> "Each number is visited at most twice — once in the main loop, once in the while loop counting from its sequence start. Non-start numbers are skipped with an O(1) check, so the total work is linear."

**Edge cases:**
> "Empty array returns 0. Duplicates are handled naturally since we use a set. Works with negative numbers too."
