# Missing Number - 學習筆記

## 這是什麼？

給你一個陣列，裡面有 n 個數字，範圍是 0 到 n，但少了一個。找出那個缺少的數字。

---

## 用什麼比喻理解？

**老師點名法**

你班上應該有 4 個學生：小零、小一、小二、小三。
點名簿上只有：小三、小零、小一。
→ 用「完整名單 - 實際到場 = 缺席的人」來找出小二沒來。

**DevOps 版本**

10 台 server 編號 0-9，清單上只有 9 台，用差集找出哪台失蹤了。

---

## 踩過什麼雷？

### 1. 空的 set 怎麼建？

```python
()       # ❌ 這是 tuple
{}       # ❌ 這是 dict
set()    # ✅ 這才是空的 set
```

### 2. 括號位置很重要！

```python
len(nums + 1)    # ❌ list + int 會爆炸
len(nums) + 1    # ✅ 先算 len，再 +1
```

### 3. 縮排決定邏輯

```python
# ❌ 錯誤：在 for 裡面 return，第一圈就結束了
for i in range(n):
    my_set.add(i)
    return result     # 太早 return！

# ✅ 正確：for 跑完再處理
for i in range(n):
    my_set.add(i)
return result         # for 外面
```

### 4. 從 set 取出元素

```python
result = {2}       # set
result.pop()       # → 2（int）
```

---

## 最終正確 Code

```python
def missingNumber(nums: List[int]) -> int:
    my_set = set()
    for i in range(len(nums) + 1):
        my_set.add(i)
    result = my_set - set(nums)
    return result.pop()
```

---

## 複雜度分析

| | 複雜度 | 說明 |
|---|--------|------|
| 時間 | O(n) | 建立 set 走一遍，差集運算走一遍 |
| 空間 | O(n) | 存了一個大小 n+1 的 set |

---

## 面試怎麼回答？

> **面試官**：請解釋你的思路。

我用 Set 差集來解這題。

首先，我建立一個「完整名單」的 set，包含 0 到 n 的所有數字。
然後把輸入的 nums 也轉成 set。
用「完整名單 - 實際有的」，差集的結果就是缺少的那個數字。
最後用 .pop() 把它從 set 裡取出來回傳。

時間複雜度是 O(n)，空間複雜度也是 O(n)。

> **面試官**：有沒有更省空間的解法？

有！可以用數學解法。
0 + 1 + 2 + ... + n 的總和公式是 n(n+1)/2。
用「應該有的總和 - 實際的總和」，差就是缺少的數字。
這樣空間複雜度可以降到 O(1)。

---

## 延伸思考

- 這題跟 Single Number 有點像，都是「找出落單的那個」
- Single Number 用 XOR，這題用 Set 差集或數學
- 如果要找「多個缺少的數字」，Set 差集更適合
