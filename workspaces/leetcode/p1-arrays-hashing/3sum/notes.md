# 3Sum 學習筆記

> LeetCode 15 | Medium | Two Pointers
> https://leetcode.com/problems/3sum/

---

## 這是什麼？（一句話白話解釋）

從一堆數字裡，找出所有 **三個數加起來 = 0** 的組合，不能重複。

---

## 用什麼比喻理解？

**倉庫平衡比喻：**

你是倉庫管理員，每個箱子有正負重量。老闆說找出所有「三個箱子一組、重量剛好平衡 = 0」的組合：

```
先把箱子按重量排好隊：
[-4, -1, -1, 0, 1, 2]

固定一個箱子（-1），問題就變成：
「從剩下的箱子裡，找兩個加起來 = 1 的」
→ 這不就是 Two Sum II 嗎！
```

**核心洞見：** 3Sum = 固定一個數 + Two Sum II，把三數問題降級成兩數問題。

---

## 踩過什麼雷？

### 雷 1：找到答案後沒跳過重複值

```python
# ❌ 只移動一步，遇到重複值會產生重複答案
else:
    result.append([nums[i], nums[l], nums[r]])
    l += 1
    r -= 1

# ✅ 移動後繼續跳過重複值
else:
    result.append([nums[i], nums[l], nums[r]])
    l += 1
    r -= 1
    while l < r and nums[l] == nums[l - 1]:  # l 跳過重複
        l += 1
    while l < r and nums[r] == nums[r + 1]:  # r 跳過重複
        r -= 1
```

**範例：** `[-2, 0, 0, 2, 2]` 找到 `[-2, 0, 2]` 後，`l` 移到下一個 `0`、`r` 移到下一個 `2`，又配出一樣的答案。

### 雷 2：跳過重複有兩個地方

| 地方 | 怎麼跳 | 為什麼 |
|------|--------|--------|
| 外層 `i` | `if i > 0 and nums[i] == nums[i-1]: continue` | 固定的第一個數一樣，後面答案一定重複 |
| 內層找到答案後 | `while` 跳過 `l` 和 `r` 的重複 | 同一組答案不要加兩次 |

少了任何一個都會有重複！

### 雷 3：while 跳重複要加 `l < r` 防越界

```python
# ❌ 危險：可能 l 跳過 r
while nums[l] == nums[l - 1]:
    l += 1

# ✅ 安全：加上邊界檢查
while l < r and nums[l] == nums[l - 1]:
    l += 1
```

---

## 最終正確 Code

```python
def threeSum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []

    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # 外層跳過重複

        l, r = i + 1, len(nums) - 1

        while l < r:
            if nums[i] + nums[l] + nums[r] < 0:
                l += 1          # 總和太小，左移
            elif nums[i] + nums[l] + nums[r] > 0:
                r -= 1          # 總和太大，右移
            else:
                result.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:  # 內層跳過 l 重複
                    l += 1
                while l < r and nums[r] == nums[r + 1]:  # 內層跳過 r 重複
                    r -= 1

    return result
```

---

## 複雜度分析

| | 複雜度 | 說明 |
|---|--------|------|
| **時間** | O(n²) | 外層 O(n) × 內層 Two Pointers O(n)，排序 O(n log n) 被吃掉 |
| **空間** | O(1) | 不算排序和輸出的話，只用了幾個指針變數 |

---

## 跟前兩題的關係

| | Two Sum | Two Sum II | 3Sum |
|---|---------|------------|------|
| **排序** | ❌ | ✅ 已排序 | 自己排 |
| **方法** | Hash Map | Two Pointers | for loop + Two Pointers |
| **找幾個數** | 2 個 | 2 個 | 3 個（降級成 2 個） |
| **時間** | O(n) | O(n) | O(n²) |
| **空間** | O(n) | O(1) | O(1) |
| **重複處理** | 不需要 | 不需要 | 外層 + 內層都要跳 |

**套路：** kSum 問題都是「固定 k-2 個數，剩下用 Two Pointers」。

---

## 面試怎麼回答？

**面試官問：** 找出 array 中所有三數之和等於 0 的組合，不能重複。

**回答架構：**

1. **確認條件：** 「答案不能有重複組合對吧？array 可以有重複的數字嗎？」

2. **說明降級思路：**
   > 「3Sum 可以拆成：固定一個數 nums[i]，剩下就變成在 sorted array 裡找兩數之和 = -nums[i]，就是 Two Sum II 的做法。」

3. **說明排序 + Two Pointers：**
   > 「先排序 O(n log n)，外層 for loop 固定第一個數，內層用雙指針從兩端往中間夾。」

4. **強調去重（面試官最在意的！）：**
   > 「去重有兩個地方：
   > - 外層：nums[i] 跟 nums[i-1] 一樣就跳過
   > - 內層：找到答案後，l 和 r 都要跳過相同的值」

5. **複雜度：**
   > 「時間 O(n²)，空間 O(1)。排序的 O(n log n) 被 O(n²) 吃掉了。」

---

## 延伸題目

- **4Sum** — 再多一層 for loop，固定兩個數，剩下用 Two Pointers → O(n³)
- **kSum** — 遞迴版，固定 k-2 個數，底層都是 Two Pointers
- **3Sum Closest** — 不找等於 0，找最接近 target 的三數之和

---

## 學習日期

2026-02-10
