# Valid Sudoku (36)
> Pattern: Arrays & Hashing (HashSet per row/col/box)
> Date: 2026-04-13 | Session: 4 (jump-to, 同事分享)

## Pattern 摘要
> 用三組 HashSet（rows, cols, boxes）分別記錄每一列、每一行、每個 3x3 box 出現過的數字，掃描一次就能判斷有沒有重複。

## 解法 (Approach)
- **暴力法 = 最佳解（同一個做法）：** 一次掃描 9x9 棋盤，每格查三個 set 有沒有重複，沒有就 add 進去 — Time O(1), Space O(1)（棋盤固定 81 格）
- **關鍵洞察 (Key Insight)：** 數獨的三條規則（row 不重複、`col 不重複、box 不重複）可以用三組獨立的 set 同時檢查。box 的定位靠 `(r // 3, c // 3)` 把 9x9 映射到 3x3。

## 💻 My Code

```python
from typing import List
from collections import defaultdict


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        boxes = defaultdict(set)

        for r in range(9):
            for c in range(9):
                num = board[r][c]

                if num == ".":
                    continue
                if num in rows[r]:
                    return False
                if num in cols[c]:
                    return False
                if num in boxes[(r // 3, c // 3)]:
                    return False
                rows[r].add(num)
                cols[c].add(num)
                boxes[(r // 3, c // 3)].add(num)
        return True
```

## ⚡ Edge Cases
- 棋盤有大量 `.`（空格多）— 要 skip，不能當成值處理
- 同一個數字在同 row 和同 box 同時重複 — 只要任一個 set 查到就夠，不用全查
- 棋盤全空（全是 `.`）— 應該 return True（沒有違規）

## 🔴 我的錯誤

| 我以為 | 實際上 | 為什麼錯 |
|--------|--------|----------|
| `cols[r]` 檢查 column | 應該是 `cols[c]`，r 是 row index，c 才是 column index | 變數名搞混，r = row, c = column |
| 只要查 set 就好，不用 add | 不 add 的話 set 永遠是空的，永遠查不到重複 | 忘了「先查再記」的流程，查和記缺一不可 |
| `{}` 可以當空 set | `{}` 是空 dict，空 set 要用 `set()` | Python 語法特例，`{}` 被 dict 搶走了 |

## 🎤 How to Say It in Interview

**Opening (30 sec):**
> "I'd use three groups of HashSets — one for rows, one for columns, one for 3x3 boxes. I scan each cell once: if the number already exists in any of the three sets, it's invalid. Otherwise I add it to all three."

**Key trick:**
> "To map any cell (r, c) to its 3x3 box, I use (r // 3, c // 3) as the key. Integer division groups 0-2, 3-5, 6-8 into three buckets."

**Complexity:**
> "Time and space are both O(1) since the board is always 9x9 — fixed size, no scaling."

**Edge cases:**
> "I skip '.' cells immediately. The board can be mostly empty and still valid."

## C# vs Python 比較（同事解法）

| 差異 | Python | C# |
|------|--------|-----|
| 初始化 | `defaultdict(set)` 一行 | `new HashSet<char>[9]` + 迴圈逐一 `new HashSet()` |
| boxes 結構 | dict + tuple key `(r//3, c//3)` | 2D array `boxs[r,c]` |
| 查 + 記 | 分兩步：`if num in set` + `set.add(num)` | 一步：`!set.Add(val)` 同時查和記 |
| 反轉布林 | `not` | `!` |

C# 的 `HashSet.Add()` return `bool`（成功 true，已存在 false），Python 的 `set.add()` return `None`，所以 Python 只能分兩步。

## 學到的 Python 知識

| 概念 | 重點 |
|------|------|
| `defaultdict(set)` | 存取不存在的 key 時自動建 `set()`，括號裡放 function 不加 `()` |
| `//` 整數除法 | 只取整數，小數砍掉。`7 // 3 = 2` |
| tuple 當 dict key | tuple 是 immutable 所以 hashable，可以當 key；list 不行 |
| `in` 查 set | O(1) 查找，比 list 的 O(n) 快 |
