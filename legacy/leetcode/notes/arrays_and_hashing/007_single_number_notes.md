# Single Number - 學習筆記

## 這是什麼？（一句話白話解釋）

每個數字都有配對（出現兩次），只有一個落單（出現一次），找出那個落單的。

---

## 用什麼比喻理解？

**DevOps 情境：對帳 Request**
> Server A 送出 5 個 request，Server B 收到 4 個。
> 每個成功的 request 會有「送出」和「收到」兩筆紀錄。
> 只出現一次的那個 = 丟失的 request。

**配對遊戲**
> 一堆襪子裡找落單的那隻。成對的都拿掉，最後剩下的就是落單的。

---

## 踩過什麼雷？

### 1. `discard` 拼成 `discord`
```python
my_set.discord(i)  # ❌ AttributeError
my_set.discard(i)  # ✅ 正確
```

### 2. 回傳 Set 而不是數字
```python
return my_set      # ❌ 回傳 {1}，但題目要 1
return my_set.pop() # ✅ 把元素彈出來
```

---

## 最終正確 Code

### 解法一：Set 配對消除法

```python
def singleNumber(nums: List[int]) -> int:
    my_set = set()
    for i in nums:
        if i not in my_set:
            my_set.add(i)      # 第一次出現：加進去
        else:
            my_set.discard(i)  # 第二次出現：拿掉
    return my_set.pop()        # 最後剩下的就是答案
```

### 解法二：XOR 位元運算（面試加分！）

```python
def singleNumber_xor(nums: List[int]) -> int:
    result = 0
    for num in nums:
        result ^= num   # 成對的會抵消變 0，落單的留下
    return result
```

**為什麼 XOR 可以？**
- `a ^ a = 0`（相同的數字 XOR 會抵消）
- `0 ^ a = a`（0 XOR 任何數 = 那個數）
- 所以成對的都消掉，剩下落單的

---

## 複雜度分析

| 解法 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| Set 配對消除法 | O(n) | O(n) |
| XOR 位元運算 | O(n) | O(1) ← 面試加分！ |

---

## Set 語法備忘

```python
my_set = set()        # 建立空 Set
my_set.add(x)         # 加進去
my_set.discard(x)     # 拿掉（不存在也不報錯）
my_set.remove(x)      # 拿掉（不存在會報錯）
my_set.pop()          # 彈出任意一個元素
x in my_set           # 檢查是否存在 → True/False
```

---

## 面試怎麼回答？

**面試官：** 「給你一個陣列，每個元素出現兩次，只有一個出現一次，怎麼找？」

**我的回答：**

> 「我可以用 Set 來解。遍歷陣列，第一次看到的數字加進 Set，第二次看到就從 Set 拿掉。最後 Set 裡剩下的就是只出現一次的數字。時間 O(n)，空間 O(n)。」
>
> 「如果要優化到 O(1) 空間，可以用 XOR 位元運算。因為 a XOR a = 0，所有成對的數字 XOR 完會變 0，最後剩下的就是落單的那個。」

---

## 延伸問題

- 如果每個數字出現**三次**，只有一個出現一次呢？（不能用 XOR）
- 如果有**兩個**數字只出現一次呢？（LeetCode 260）
