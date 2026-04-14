# Top K Frequent Elements (LeetCode 347)

- **Pattern:** Arrays & Hashing — Frequency Counter + Bucket Sort
- **Difficulty:** Medium
- **Date:** 2026-04-07
- **Session:** 2 (jump-to)

---

## Pattern 摘要
> 先用 Frequency Counter 數頻率，再用 Bucket Array 把元素放到頻率對應的 index，從最後面往前走就能找到前 k 個 — 不用排序，O(n) 搞定。

## 解法 (Approach)
- **暴力法 (Brute Force):** Counter 數頻率 → sorted 按頻率排序 → 取前 k 個 — Time O(n log n), Space O(n)
- **最佳解 (Optimal):** Counter 數頻率 → 建 Bucket Array（index=頻率, value=元素）→ 從高頻往低頻掃 → 取 k 個 — Time O(n), Space O(n)
- **關鍵洞察 (Key Insight):** Bucket Array 的 index 本身就代表頻率大小，天然有序，不需要 comparison sort，所以能突破 O(n log n) 的排序下限。

## 💻 My Code

```python
# Brute Force
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        sorted_keys = sorted(freq, key=freq.get, reverse=True)
        return sorted_keys[:k]

# Optimal — Bucket Sort
class SolutionOptimal:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, count in freq.items():
            buckets[count].append(num)

        result = []
        for i in range(len(buckets) - 1, -1, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result
```

## ⚡ Edge Cases
- 只有一個元素：`nums = [1]`, k=1 → 直接回傳 `[1]`
- 全部相同：`nums = [5,5,5]`, k=1 → `[5]`，bucket 只有一格有東西
- k 等於不同元素數量：等於全部回傳，reverse scan 會走完所有非空 bucket

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| Bucket 的 value 放的是 nums 的 index | value 放的是「出現該頻率的元素本身」 | 搞混了 bucket 的用途，bucket 是按頻率分類，不是按位置 |
| `freq.get()` 加括號 | `freq.get` 不加括號傳給 sorted | `key=` 要的是 function 本身，不是呼叫結果 |
| 忘記 `from collections import Counter` | Counter 在 collections 模組裡，要 import | 不熟悉 Python 標準庫的模組結構 |
| Reverse scan 的 complexity 是 O(k) | 是 O(n)，因為要掃過整個 buckets array | 空的 bucket 也要走過去，不是只走 k 步 |

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd approach this with a frequency counter and bucket sort. First, count element frequencies with a hash map. Then use bucket sort where the index represents frequency — this avoids comparison sorting entirely."

**Optimization:**
> "The brute force is O(n log n) because of sorting, but we can do O(n) by using a bucket array where index equals frequency. Since the array index is naturally ordered, we just scan from the highest index backwards to collect the top k elements."

**Edge cases:**
> "I'd handle the case where k equals the number of unique elements — the scan would just collect everything. Also, the bucket size needs to be len(nums) + 1 since an element could appear n times."

## 重要語法筆記

| 語法 | 用法 | 說明 |
|------|------|------|
| `Counter(nums)` | 數頻率 | 需要 `from collections import Counter` |
| `sorted(freq, key=freq.get, reverse=True)` | 按 value 排序 dict 的 key | `key=` 接 function 本身，不加 `()` |
| `[[] for _ in range(n)]` | 建 n 個獨立的空 list | 不能用 `[[]] * n`（會共用同一個 list） |
| `freq.items()` | 取出 dict 的 (key, value) | 用 `for num, count in freq.items()` |
| `range(n-1, -1, -1)` | 從 n-1 倒著走到 0 | start, stop(不含), step |
| `list[:k]` | 取前 k 個元素 | Python slice 語法 |
