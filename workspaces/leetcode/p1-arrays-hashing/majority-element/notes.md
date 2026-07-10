# Majority Element 學習筆記

> LeetCode 169. Majority Element
> https://leetcode.com/problems/majority-element/

---

## 這是什麼？（一句話白話解釋）

找出陣列裡「出現次數超過一半」的那個數字。

---

## 用什麼比喻理解？

**選舉投票比喻：**
- 一場選舉有 7 張票：`[2, 2, 1, 1, 1, 2, 2]`
- 候選人 2 得到 4 票，候選人 1 得到 3 票
- 總票數的一半 = 3.5
- 候選人 2 的票數（4）> 3.5 → 當選！

**跟 Top K Frequent 的關係：**
- Top K Frequent = 找前 k 名
- Majority Element = 找第 1 名（而且票數要過半）

---

## 踩過什麼雷？

### 1. `.key()` vs `.keys()`
```python
my_dict.key()   # ❌ 沒有這個方法
my_dict.keys()  # ✅ 要加 s 和 ()
```

### 2. 混淆 key 和 value（超重要！）
```python
my_dict = {3: 2, 2: 1}

for n in my_dict.keys():
    # n 是 key（數字本身）= 3, 2
    # my_dict[n] 是 value（出現次數）= 2, 1

    if n > len(nums) / 2:          # ❌ 錯！這是在比較數字本身
    if my_dict[n] > len(nums) / 2: # ✅ 對！這是在比較出現次數
```

### 3. return 錯東西
```python
return my_dict[n]  # ❌ 這是回傳出現次數
return n           # ✅ 這是回傳數字本身
```

### 4. 定義了函數但沒呼叫
```python
# ❌ 錯誤
class Solution:
    def majorityElement(self, nums):
        def helper(nums):
            ...
        # 沒有 return！

# ✅ 正確：直接寫邏輯，不用內部函數
class Solution:
    def majorityElement(self, nums):
        my_dict = {}
        ...
        return n
```

---

## 最終正確 Code

### 解法一：手動 dict 計數（LeetCode 提交版）
```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        my_dict = {}
        for i in nums:
            if i not in my_dict:
                my_dict[i] = 1
            else:
                my_dict[i] += 1
        for n in my_dict.keys():
            if my_dict[n] > len(nums) / 2:
                return n
```

### 解法二：Counter（簡潔版）
```python
from collections import Counter

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return Counter(nums).most_common(1)[0][0]
```

---

## 複雜度分析

| 解法 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| Counter 版 | O(n) | O(n) |
| 手動 dict 版 | O(n) | O(n) |

---

## 面試怎麼回答？

### Q: 請解釋你的思路

> 「這題要找出現超過 n/2 次的元素。
> 我用 dict 計數，記錄每個數字出現幾次，
> 然後遍歷 dict，找出 count > n/2 的那個 key 回傳。」

### Q: 時間和空間複雜度？

> 「時間 O(n)，空間 O(n)。」

---

## Key vs Value 觀念整理

```python
my_dict = {3: 2, 2: 1}
#          ↑  ↑
#         key value

my_dict.keys()   # → [3, 2]（所有 key）
my_dict.values() # → [2, 1]（所有 value）
my_dict[3]       # → 2（用 key 查 value）
```

**記憶口訣：**
- `for x in dict.keys()` → x 是 key
- `dict[x]` → 用 key 查 value

---

## 學習日期
2026-01-14
