# 33. Search in Rotated Sorted Array

S19 (2026-07-23) · P3 · Binary Search (index) · #153 的換皮題(step E 驗收)

## 第 0 步 模式定位

> 這題不是「旋轉陣列」題,它是 **Binary Search (index)** 的實例。

換皮題鏈:704(原型)→ 74(2D 攤平)→ 153(旋轉,找斷崖)→ **33(旋轉 + 找 target)**

跟 #153 同一個陣列形狀,換一個問題:#153 找**最小值**,#33 找**特定 target**。

## 第 2 步 視覺化

```
原本(升序):  [0, 1, 2, 4, 5, 6, 7]
旋轉:        [4, 5, 6, 7, 0, 1, 2]
              └─段1(高)┘ └段2(低)┘
```

**關鍵性質:從任何一個 mid 切開,左右兩半至少有一半是完整有序的**(斷崖只有一個,
只能落在其中一半)。有序的那一半才有辦法用大小關係判斷 target 在不在裡面。

## Code

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:                          # Q5: 兩邊都丟 mid -> 閉區間
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid                            # 這行一跑,下面就確定 mid 不是答案

            if nums[left] <= nums[mid]:               # Q2 第一層: 左半有序
                if nums[left] <= target < nums[mid]:  # Q2 第二層: target 在左半嗎
                    right = mid - 1
                else:
                    left = mid + 1
            else:                                     # 右半有序
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1                                     # 區間縮成空
```

O(log n) 時間 / O(1) 空間。

## check 比 #153 多做什麼(第 4 步的核心)

| | #153 | #33 |
|---|---|---|
| check 層數 | **一層**:mid 在第一段還第二段(`nums[mid] > nums[r]`) | **兩層**:① 哪半有序 ② target 在不在那半裡 |
| 免費地標 | `nums[r]` 永遠在尾段,一個證人擋全部 | 沒有免費地標;要先確認哪半有序才敢比大小 |
| mid | 有一邊留著(`r = mid`) | 相等就 `return`,兩邊都丟(`mid±1`) |
| 迴圈 | `while l < r` | `while l <= r` |
| 收尾 | `return nums[l]`(縮成單點) | `return -1`(縮成空) |

## 本次 bug(1 個)

**第 11 行 `while left < right` 應為 `left <= right`。**

- **症狀:14 fail / 17 pass,且分布有規律 —— 「找得到的全掛、找不到的全綠」。**
- 成因:兩邊都丟 mid,區間會縮到剩一格(`left == right`);`<` 讓最後一格永遠沒被
  檢查就掉出迴圈回 `-1`。target 不在陣列時剛好蒙對,所以那半測試全綠。
- 🔴 **同型第 2 次**:S17 #74 的 `return False` 卡在 `while` 內,症狀一模一樣
  (期望 True 全掛 / 期望 False 全綠)。**「部分綠」的 bug 不報錯,比 syntax error 危險。**
- **診斷法(要養成的反射):harness 掛了先看 fail/pass 的分布,不要先看 code。
  分布會直接指出是哪一類邏輯錯。**

## Answer-debt

- `while` 那行的 fix 由 coach 指出(學生喊「直接說哪裡有問題」)。
- 前段的邊界配對規則表由 coach 串。
- → 兩筆都登記白紙重寫,3 天內到期(2026-07-26)。

## Harness

```
./scripts/lab-lc.sh workspaces/leetcode/p3-binsearch-linkedlist/search-rotated/
31 passed
```

## 待補

- Step E 固定收尾問句 Q②(#33 的 check 比 #153 多做什麼)**由學生自己講一遍** — 上表是
  coach 整理的版本,不算學生的答案。S20 重考。
