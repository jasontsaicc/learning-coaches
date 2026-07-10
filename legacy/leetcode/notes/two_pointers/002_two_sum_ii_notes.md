# Two Sum II - Input Array Is Sorted 學習筆記

> LeetCode 167 | Medium | Two Pointers
> https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

---

## 這是什麼？（一句話白話解釋）

在**已排序**的 array 中，用兩個指針從頭尾往中間夾，找出兩個數字加起來等於 target。

---

## 用什麼比喻理解？

**相親配對比喻：**

想像你是媒人，要幫一群人配對（找兩人「契合度」= target）。

這群人已經按照「溫柔程度」排好隊：
```
[暴躁] [普通] [溫和] [超溫柔]
  ↑                      ↑
 left                  right
```

- 暴躁 + 超溫柔 = 契合度太高？→ 超溫柔配誰都太高，淘汰他（right 左移）
- 暴躁 + 溫和 = 契合度太低？→ 暴躁配誰都太低，淘汰他（left 右移）
- 剛剛好？→ 配對成功！

**關鍵洞見：** 因為已經排序，最小配最大都不行的話，最大就可以安全淘汰，不會漏掉答案。

---

## 踩過什麼雷？

### 雷 1：大於小於寫反

```python
# ❌ 錯誤
if target > numbers[l] + numbers[r]:  # target 比較大 = 總和太小
    r -= 1  # 右指針左移會讓總和更小！錯！

# ✅ 正確
if target > numbers[l] + numbers[r]:  # 總和太小
    l += 1  # 左指針右移，讓總和變大
```

**記憶口訣：** 總和太小，小的要變大（left 右移）；總和太大，大的要變小（right 左移）

### 雷 2：1-indexed 只加了一邊

```python
# ❌ 錯誤
return [l+1, r]  # r 忘記 +1

# ✅ 正確
return [l+1, r+1]  # 兩邊都要 +1
```

**經驗：** 看到 1-indexed 題目，return 時兩個 index 都要檢查！

---

## 最終正確 Code

```python
def twoSum(numbers: List[int], target: int) -> List[int]:
    l, r = 0, len(numbers) - 1

    while l < r:
        if target > numbers[l] + numbers[r]:
            l += 1  # 總和太小，左指針右移
        elif target < numbers[l] + numbers[r]:
            r -= 1  # 總和太大，右指針左移
        else:
            return [l+1, r+1]  # 找到了！記得 1-indexed

    return []  # 題目保證有解，理論上不會走到這
```

---

## 複雜度分析

| | 複雜度 | 說明 |
|---|--------|------|
| **時間** | O(n) | 每個元素最多被訪問一次（左右指針各走一遍） |
| **空間** | O(1) | 只用兩個指針變數，沒有額外資料結構 |

---

## 跟 Two Sum 的比較

| | Two Sum | Two Sum II |
|---|---------|------------|
| **Array 排序** | ❌ 沒有 | ✅ 已排序 |
| **方法** | Hash Map | Two Pointers |
| **時間** | O(n) | O(n) |
| **空間** | O(n) | O(1) ✅ |
| **回傳** | 0-indexed | 1-indexed |

**選擇時機：**
- 沒排序 → 用 Hash Map（或先排序再用 Two Pointers，但會變 O(n log n)）
- 已排序 + 要求 O(1) 空間 → 用 Two Pointers

---

## 面試怎麼回答？

**面試官問：** 給你一個已排序的 array，找兩個數加起來等於 target。

**回答架構：**

1. **確認條件：** 「請問 array 是排序過的嗎？有空間限制嗎？」

2. **說明思路：**
   > 「因為 array 已經排序，我可以用 Two Pointers。
   > 左指針從頭、右指針從尾，根據總和調整：
   > - 太大就右指針左移（讓總和變小）
   > - 太小就左指針右移（讓總和變大）
   > - 相等就找到了」

3. **說明為什麼不會漏：**
   > 「這樣不會漏掉答案，因為每次淘汰的數字都已經不可能是答案的一部分了。
   > 比如 left + right 已經太大，而 left 是剩餘最小的，
   > 所以 right 配任何其他數字只會更大，可以安全淘汰。」

4. **複雜度：**
   > 「時間 O(n)，空間 O(1)，比 Hash Map 省空間。」

---

## 延伸題目

- **3Sum** — 固定一個數，剩下用 Two Pointers（下一題！）
- **4Sum** — 固定兩個數，剩下用 Two Pointers
- **Two Sum（原版）** — 沒排序，用 Hash Map

---

## 學習日期

2026-01-20
