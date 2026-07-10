# Top K Frequent Elements 學習筆記

> LeetCode 347. Top K Frequent Elements
> https://leetcode.com/problems/top-k-frequent-elements/

---

## 這是什麼？（一句話白話解釋）

找出陣列裡「出現次數最多」的前 k 個數字。

---

## 用什麼比喻理解？

**DevOps 看 Log 比喻：**
- 你有一堆 server 錯誤代碼：`[404, 500, 404, 200, 404, 500]`
- 老闆問：「最常出現的前 2 個錯誤代碼是什麼？」
- 先數數量 → `{404: 3, 500: 2, 200: 1}`
- 再按數量排序 → 取前 2 個 → `[404, 500]`

**核心思路：計數 → 排序 → 取前 k 個**

---

## 踩過什麼雷？

### 1. `Counter` 拼錯
```python
count = Count(nums)    # ❌ NameError: name 'Count' is not defined
count = Counter(nums)  # ✅ 正確
```

### 2. 變數名不一致
```python
count = Counter(nums)
most_common = counter.most_common(k)  # ❌ counter 不存在，應該是 count

count = Counter(nums)
most_common = count.most_common(k)    # ✅ 正確
```

### 3. list comprehension 變數不一致
```python
result = [x[0] for i in most_common]  # ❌ 用 i 迭代，卻取 x[0]
result = [i[0] for i in most_common]  # ✅ 正確：變數名要一致
```

### 4. 拼字錯誤
```python
return resul   # ❌ 少打一個 t
return result  # ✅ 正確
```

---

## 最終正確 Code

### 解法一：笨方法（dict + sorted keys）
```python
def topKFrequent(nums, k):
    my_dict = {}
    for i in nums:
        if i not in my_dict:
            my_dict[i] = 1
        else:
            my_dict[i] += 1
    sorted_key = sorted(my_dict.keys(), key=lambda x: my_dict[x], reverse=True)
    return sorted_key[:k]
```

### 解法二：用 .items() 排序
```python
def topKFrequent_v2(nums, k):
    my_dict = {}
    for i in nums:
        if i not in my_dict:
            my_dict[i] = 1
        else:
            my_dict[i] += 1
    items = my_dict.items()  # [(key, value), ...]
    sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
    result = [x[0] for x in sorted_items[:k]]
    return result
```

### 解法三：用 Counter.most_common（最簡潔）
```python
from collections import Counter

def topKFrequent_counter(nums, k):
    count = Counter(nums)
    most_common = count.most_common(k)
    result = [i[0] for i in most_common]
    return result
```

---

## 複雜度分析

| 解法 | 時間複雜度 | 空間複雜度 | 說明 |
|------|-----------|-----------|------|
| 解法一 | O(n log n) | O(n) | sorted 排序 |
| 解法二 | O(n log n) | O(n) | sorted 排序 |
| 解法三 | O(n log n) | O(n) | most_common 內部用排序 |
| Bucket Sort（進階） | O(n) | O(n) | 不排序，用桶子 index 代表次數 |

### 為什麼是 O(n log n)？
- 遍歷 nums 計數：O(n)
- 排序：O(n log n)
- 取前 k 個：O(k)
- 總共：O(n log n)

---

## 面試怎麼回答？

### Q: 請解釋你的思路

> 「這題要找出現頻率最高的 k 個元素。
> 我的思路是：**先計數，再排序，最後取前 k 個**。
> 用 dict 或 Counter 計算每個數字出現幾次，
> 然後按次數從大到小排序，取前 k 個 key 回傳。」

### Q: 時間複雜度？

> 「O(n log n)。
> 計數是 O(n)，排序是 O(n log n)，取前 k 個是 O(k)。
> 排序主導，所以總共是 O(n log n)。」

### Q: 能不能優化到 O(n)？

> 「可以用 **Bucket Sort**。
> 因為出現次數最多就是 n 次，可以建立 n+1 個桶子，
> 桶子的 index 代表出現次數，把數字丟進對應的桶子，
> 然後從後往前撿 k 個。
> 這樣不需要排序，時間複雜度是 O(n)。」

### Q: 為什麼用 Counter 而不是手動 dict？

> 「Counter 是 Python 內建的工具，專門做計數。
> 而且它有 most_common(k) 方法可以直接取前 k 個，
> 程式碼更簡潔、更不容易出錯。
> 在實務上，善用內建工具是好習慣。」

---

## 學到的語法

| 語法 | 用途 | 範例 |
|------|------|------|
| `Counter(list)` | 自動計數 | `Counter([1,1,2])` → `{1:2, 2:1}` |
| `.most_common(k)` | 取前 k 常見 | `count.most_common(2)` → `[(1,2), (2,1)]` |
| `dict.items()` | key-value 變 tuple list | `{1:2}.items()` → `[(1, 2)]` |
| `lambda x: x[1]` | 匿名函數取 index | 排序時指定按哪個欄位 |
| `sorted(..., reverse=True)` | 從大到小排序 | 降冪排列 |
| `[x[0] for x in list]` | list comprehension 取特定元素 | 只取 tuple 的第一個 |

---

## 延伸思考

### Bucket Sort 概念（進階）
```
nums = [1,1,1,2,2,3], k = 2
計數：{1: 3, 2: 2, 3: 1}

桶子（index = 出現次數）：
buckets[0] = []
buckets[1] = [3]     ← 3 出現 1 次
buckets[2] = [2]     ← 2 出現 2 次
buckets[3] = [1]     ← 1 出現 3 次

從後往前撿 2 個 → [1, 2]
```
優點：O(n) 不用排序
之後再練習！

---

## 學習日期
2026-01-14
