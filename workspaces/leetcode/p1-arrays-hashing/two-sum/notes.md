# Two Sum 學習筆記

> 學習日期：2026-01-05

---

## 這是什麼？（一句話白話解釋）

用 dict 建立「反向索引」，把 O(n²) 的暴力配對變成 O(n) 的秒查。

---

## 用什麼比喻理解？

### 比喻 1：飯店找房客
- **笨方法（O(n²)）**：一間一間敲門問「你是不是 80%？」
- **聰明方法（O(n)）**：查電話簿，直接用名字找房號

### 比喻 2：DevOps 場景
找兩台 server，CPU 使用率加起來 = 100%
- 不用每台都跟每台比
- 建一張「CPU → server index」的查詢表

### 比喻 3：反向索引
| 原本的查法 | 反向索引 |
|-----------|----------|
| 用 index 找數字 | 用數字找 index |
| list 天生會的 | dict 的超能力 |

---

## 踩過什麼雷？

### 雷 1：賦值方向寫反
```python
# ❌ 錯誤
target - v = val     # Python 說：cannot assign to expression

# ✅ 正確
val = target - v     # 把計算結果放進變數
```
> 記法：「杯子 = 水」，不是「水 = 杯子」

---

### 雷 2：dict 放在迴圈裡面
```python
# ❌ 錯誤
for i, v in enumerate(nums):
    my_dict = {}     # 每次都建新的空 dict，之前存的都不見了！
    ...

# ✅ 正確
my_dict = {}         # 放在迴圈外面
for i, v in enumerate(nums):
    ...
```

---

### 雷 3：key 和 value 放反
```python
# ❌ 錯誤
my_dict[i] = val     # key=index, value=需要的partner
# 這樣查 "2 在不在 dict" 會找不到，因為 key 是 0, 1, 2... 不是數字本身

# ✅ 正確
my_dict[v] = i       # key=數字本身, value=它的index
# 這樣才能用數字去查它的 index
```
> 記法：我要「用數字查 index」，所以 key=數字，value=index

---

### 雷 4：value 存錯東西
```python
# ❌ 錯誤
my_dict[v] = v       # 存了數字本身
my_dict[v] = val     # 存了需要的 partner

# ✅ 正確
my_dict[v] = i       # 存 index，因為最後要回傳的是兩個 index
```

---

### 雷 5：只回傳一個 index
```python
# ❌ 錯誤
return my_dict[val]          # 只回傳 partner 的 index

# ✅ 正確
return [my_dict[val], i]     # 回傳 [partner的index, 目前的index]
```

---

## 最終正確的 Code

```python
def two_sum(nums: List[int], target: int) -> List[int]:
    my_dict = {}                          # 1. 在迴圈外建空 dict
    for i, v in enumerate(nums):          # 2. 遍歷每個數字
        val = target - v                  # 3. 算出需要的 partner

        if val in my_dict:                # 4. partner 在 dict 裡嗎？
            return [my_dict[val], i]      #    ✅ 在 → 回傳兩個 index
        my_dict[v] = i                    #    ❌ 不在 → 存目前的數字
```

---

## 複雜度分析

| 方法 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 暴力解（雙層迴圈） | O(n²) | O(1) |
| Hash Table 解 | O(n) | O(n) |

> 用空間換時間：多用一個 dict 的記憶體，省下大量運算時間

---

## 面試怎麼回答？

> 「Two Sum 可以用 Hash Map 解。遍歷陣列時，對每個數字計算它需要的 partner，然後查 Hash Map 看 partner 存不存在。如果存在就回傳兩個 index；如果不存在就把目前的數字存進 Hash Map。這樣只需要 O(n) 時間，因為 Hash Map 的查詢是 O(1)。」

---

## 模擬面試問答紀錄

### 問題 1：為什麼用 Hash Table？暴力解有什麼問題？

> **我的回答**：暴力解用兩個 loop 是 O(n²)，用 Hash Table 可以做到 O(n)。使用 reverse index，把 value 當 key 來快速查找。

---

### 問題 2：value 要存什麼？為什麼？

> **我的回答**：value 存 index，因為 output 需要的是 index。

---

### 問題 3：先把所有數字存進 dict，還是邊遍歷邊存？

> **我的回答**：邊遍歷邊存。如果第一次跑就查到的話，就不用全部都存。

---

### 問題 4：空間複雜度是多少？Trade-off 值得嗎？

> **我的回答**：空間複雜度 O(n)。值得，因為可以節省運算時間，而記憶體是可以重複利用的。Time is money！

**補充學習 - 什麼是 Trade-off？**

Trade-off = 取捨、權衡。像 AWS 選機器：
- 大記憶體 → 快但貴
- 小記憶體 → 便宜但慢

這題的 trade-off：

| | 暴力解 | Hash Table 解 |
|---|--------|---------------|
| 時間 | O(n²) 慢 | O(n) 快 ✅ |
| 空間 | O(1) 省 ✅ | O(n) 多用記憶體 |

> 面試加分說法：「在現代系統中，記憶體便宜、CPU 時間貴。O(n) 的額外空間通常可以接受，但 O(n²) 的時間複雜度在資料量大的時候會讓系統變慢。而且這個 dict 用完就可以釋放，不會長期佔用資源。」

---

### 問題 5：Edge Case — `nums = [3, 3]`, `target = 6` 會正確嗎？

> **我的回答**：會正確！

手動模擬：
```
回合 1：i=0, v=3, val=3 → 不在 dict → 存 my_dict[3] = 0
回合 2：i=1, v=3, val=3 → 在 dict！ → return [0, 1] ✅
```

關鍵：「**先查再存**」的順序。如果先存再查，回合 1 就會自己配對自己。

---

### 問題 6：延伸題 — Three Sum 怎麼做？

> **我的回答**：固定一個數字 a，剩下的 b + c = target - a 就是 Two Sum，再跑一次！

```
對每一個數字 a：               ← O(n) 次
    對剩下的數字做 Two Sum      ← O(n)

總共：O(n) × O(n) = O(n²)
```

---

### 面試評分標準（自我檢查用）

| 項目 | 說明 |
|------|------|
| 解題思路 | 能清楚說明暴力解 → 優化解 |
| 複雜度分析 | 時間 O(n)、空間 O(n) 都要會講 |
| Trade-off 理解 | 能解釋為什麼用空間換時間 |
| Code 品質 | 簡潔正確，沒有多餘的程式碼 |
| Edge Case | 能手動模擬特殊情況 |
| 延伸思考 | 題目變化時能舉一反三 |

---

## 學到的核心觀念

1. **反向索引**：把「要查的東西」當 key，「想得到的資訊」當 value
2. **邊走邊記**：不需要先建完整個 dict，查不到就存、查到就回傳
3. **用空間換時間**：多用記憶體，換取更快的執行速度

---

## 下一步

- [ ] 不看筆記，自己重寫一次
- [ ] 在 LeetCode 上提交看看
- [ ] 嘗試下一題：Contains Duplicate
