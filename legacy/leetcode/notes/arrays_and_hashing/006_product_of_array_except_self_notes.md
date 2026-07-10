# LeetCode 238. Product of Array Except Self

> 完成日期：2026-01-16

---

## 這是什麼？（一句話白話解釋）

給一個陣列，算出每個位置「除了自己以外，其他所有數字的乘積」，而且不能用除法。

---

## 用什麼比喻理解？

**AWS 帳單比喻：**
想像你有一排 EC2 的費用 `[1, 2, 3, 4]`。
老闆問：「如果我關掉每一台機器，剩下的機器費用乘積是多少？」

- 關掉第 1 台：剩下 2×3×4 = 24
- 關掉第 2 台：剩下 1×3×4 = 12
- 關掉第 3 台：剩下 1×2×4 = 8
- 關掉第 4 台：剩下 1×2×3 = 6

答案：`[24, 12, 8, 6]`

**核心觀念：**
每個位置的答案 = 左邊的乘積 × 右邊的乘積

---

## 踩過什麼雷？

### 1. 除法陷阱
最直覺的想法是「全部乘起來再除以自己」，但：
- 題目說不能用除法
- 如果有 0，除法會爆炸（ZeroDivisionError）

### 2. 空 list 不能用 index 賦值
```python
left = []
left[0] = 1  # ❌ IndexError!
```
要用 `append()` 或先建好大小 `[0] * len(nums)`

### 3. 倒著跑的 range 語法
```python
# ❌ 錯誤：括號位置不對
for i in range(len(nums)) -1, -1, -1:

# ✅ 正確：-1 要在括號裡面
for i in range(len(nums)-1, -1, -1):
```

### 4. range 的括號打錯
```python
# ❌ 錯誤
for i in range)len(nums)):

# ✅ 正確
for i in range(len(nums)):
```

---

## 最終正確 Code

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    # Step 1: 建立 left 陣列（從左到右）
    left = []
    for i in range(len(nums)):
        if i == 0:
            left.append(1)  # 最左邊，左邊沒有人
        else:
            left.append(left[i-1] * nums[i-1])

    # Step 2: 建立 right 陣列（從右到左）
    right = [0] * len(nums)
    for i in range(len(nums)-1, -1, -1):
        if i == len(nums) - 1:
            right[i] = 1  # 最右邊，右邊沒有人
        else:
            right[i] = right[i+1] * nums[i+1]

    # Step 3: 把 left 和 right 相乘
    result = []
    for i in range(len(nums)):
        result.append(left[i] * right[i])

    return result
```

---

## 複雜度分析

| | 複雜度 | 原因 |
|---|--------|------|
| 時間 | **O(n)** | 三個 for loop，各掃一次陣列 |
| 空間 | **O(n)** | 用了 left、right、result 三個陣列 |

### 可以優化嗎？
可以！空間可以優化到 O(1)：
- 先把 left 的結果直接存到 result
- 然後從右邊掃的時候，用一個變數累積右邊乘積，邊乘邊更新 result

---

## 面試怎麼回答？

> 「好的，讓我先講一下這題的思路。
>
> **首先，最直覺的想法**是把所有數字乘起來，然後對每個位置除以那個數字。但這個方法有兩個問題：第一，題目說不能用除法；第二，如果陣列裡有 0，除法會出錯。
>
> **所以我換一個角度想**：對於每個位置 i，答案其實就是『左邊所有數字的乘積』乘以『右邊所有數字的乘積』。
>
> **我的做法是**：
> 1. 先從左到右掃一遍，建立 `left` 陣列
> 2. 再從右到左掃一遍，建立 `right` 陣列
> 3. 最後 `left[i] × right[i]` 就是答案
>
> 時間複雜度 O(n)，空間複雜度 O(n)。如果要優化空間，可以只用一個 result 陣列，邊掃邊更新。」

---

## 學到的技巧

### Prefix / Suffix 預處理
這是一個很常見的技巧：
- **Prefix（前綴）**：從左往右累積資訊
- **Suffix（後綴）**：從右往左累積資訊

這個技巧會在很多題目出現！

---

## 相關題目

- [ ] Trapping Rain Water（也用 prefix/suffix）
- [ ] Maximum Product Subarray

---

## 心得

這題一開始想放棄，但其實核心概念不難：
- 不能用除法 → 那就分開算左邊和右邊
- 每個位置的答案 = 左邊乘積 × 右邊乘積

記住這個 pattern：當「不能直接算」的時候，想想能不能「分開算再合併」！
