# 153. Find Minimum in Rotated Sorted Array

S18 (2026-07-14) · P3 · Binary Search (index) — 邊界變體 · 七步 flow 首刷

## 第 0 步 模式定位

> 這題不是「找最小值」題,它是 **Binary Search (index)** 的實例。

換皮題鏈:704(原型)→ 74(2D 攤平)→ **153(旋轉,找有序半邊)** → 33(旋轉 + 找 target)

秒認信號:① 原本 sorted 只是被旋轉 → 局部仍單調 ② 題目明寫 **O(log n)** ③ 找的是**邊界/斷點**不是值

## 第 2 步 視覺化

旋轉 = sorted array 切一刀,後半段搬到前面:

```
原本:  [0, 1, 2, | 4, 5, 6, 7]
旋轉:  [4, 5, 6, 7, | 0, 1, 2]
        └─第一段──┘  └第二段┘   ← 兩段各自遞增,第二段整段比第一段低

值
 7 |          *
 6 |       *
 5 |    *
 4 | *
 2 |                      *
 1 |                   *
 0 |                *          ← 斷崖底部 = 最小值 = 第二段第一格
   +--------------------------
     0  1  2  3    4  5  6
```

**結構保證(整題的命根子):第一段的每個元素 > 第二段的每個元素。**
特例:沒旋轉 → 只有一段,最小值 = `nums[0]`。

## 第 3 步 推導腳本(五問)

| # | 問 | 答 → code |
|---|---|---|
| Q1 | 我在找什麼? | 第二段的第一格 = 斷崖底部 |
| Q2 | check 怎麼寫? | `nums[r]` 是免費地標(永遠在尾段)→ `nums[mid] > nums[r]` 就在第一段 |
| Q3 | 範圍/不變量? | 答案永遠在 `[l, r]` → `l, r = 0, len(nums)-1` |
| Q4 | 試了 mid 指向哪半? | **不對稱**(見下)→ `l = mid+1` vs `r = mid` |
| Q5 | 何時停、答案在哪? | 沒 target 可命中 → `while l < r`,收斂到單點 → `return nums[l]` |

### Q4 的不對稱 = 證人論證

「證明 X 不是最小值」的唯一方法:**在陣列裡指出一個比它小的元素當證人。**

| 情況 | mid 有證人嗎? | 動作 |
|---|---|---|
| `nums[mid] > nums[r]` | 有 — `nums[r]` 就比它小 | `l = mid + 1` **丟掉 mid** |
| `nums[mid] < nums[r]` | 沒有 — 它自己可能就是最小值 | `r = mid` **留住 mid** |

程式只比較一次(`nums[mid]` vs `nums[r]`),卻能一口氣丟掉左半 4 個元素 ——
靠的是上面那條**結構保證**:mid 在第一段、r 在第二段 → 第一段全部 > `nums[r]`,
所以 `nums[r]` 一個人當了全部人的證人。

### 為什麼比 `nums[r]` 不比 `nums[l]`

沒旋轉時(整段遞增):
- 比 `nums[r]`:每圈 `nums[mid] < nums[r]` → 一路 `r = mid` → 收斂到 index 0 ✅ **零行特例**
- 比 `nums[l]`:`nums[mid] > nums[l]` → 規則說往右找 → **答錯**,得多寫 `if nums[l] < nums[r]: return nums[l]`

## Code

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        l = 0
        r = len(nums) - 1
        while l < r:                    # Q5: 沒 target 可命中,收斂到單點
            mid = (l + r) // 2          # // 保證 mid < r,r=mid 才不會卡住
            if nums[mid] > nums[r]:     # Q2: mid 在第一段
                l = mid + 1             # Q4: mid 有證人 nums[r],安全丟
            else:                       # Q2: mid 在第二段
                r = mid                 # Q4: mid 可能是答案,不能丟
        return nums[l]                  # Q5: l == r
```

O(log n) 時間 / O(1) 空間。

## 開閉區間配對規則(本題最大收穫)

`while` 的 `=` 和 `mid` 的 `±1` **是同一個決定**。判準:**「mid 檢查完還需要留著嗎?」**

| | 不需要留 | 需要留 |
|---|---|---|
| 動作 | `l=mid+1` / `r=mid-1`(兩邊都跳過 mid) | `r=mid`(留住) |
| 迴圈 | `while l <= r` | `while l < r` |
| 收尾 | 迴圈外 `return -1`(區間縮成空) | 迴圈外 `return nums[l]`(區間縮成單點) |
| 題 | #704, #74 | **#153**,所有找邊界題 |

**配錯就死:** `l<=r` 配 `r=mid` → `l==r` 時 `mid=l`、`r=mid=l`,區間不再縮小 → **死迴圈**。

## Harness

```
./scripts/lab-lc.sh workspaces/leetcode/p3-binsearch-linkedlist/find-minimum-rotated/
19 passed
```

**tripwire 換了機制:** 這題計時抓不到 O(n)(掃 10 萬個元素太快)。改用 `CountingList`
包住陣列數 `__getitem__` 次數(binary search ~34 次,budget 100),並讓 `__iter__` 直接
raise —— `min(nums)` / `for x in nums` 當場被擋。**計時抓不到最優性時,換一個可觀測的
代理指標(讀取次數 / 比較次數)。**

## 本次 bug

**零。**(對比 #74 的 2 個 bug。)

## 待補

- Chunk 2 Transfer 未答:#33 的 ① 迴圈條件用哪種 ② check 比 #153 多做什麼
- step E 驗收題:#33 Search in Rotated Sorted Array
