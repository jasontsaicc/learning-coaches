# LeetCode 36. Valid Sudoku

> 完成日期：2026-01-19

---

## 這是什麼？（一句話白話解釋）

檢查一個 9×9 數獨是否合法：每一列、每一行、每一個 3×3 小方格都不能有重複數字。

---

## 用什麼比喻理解？

**SRE 檢查 K8s 部署比喻：**

想像你是 SRE，要檢查公司的 Kubernetes 部署是否合法：

| 數獨規則 | K8s 對應 |
|---------|---------|
| 每一 row 不能重複 | 同一個 **namespace** 不能有重複的 service name |
| 每一 col 不能重複 | 同一個 **node** 不能有重複的 port binding |
| 每一 box 不能重複 | 同一個 **AZ** 不能有重複的 PV ID |

**策略：準備三本「登記簿」**
- 掃過每一個 pod/service
- 每看到一個，就檢查三本登記簿有沒有重複
- 沒重複就登記，有重複就告警 `return False`

---

## 踩過什麼雷？

### 1. Box 的 key 怎麼算？

數獨的 9 個 3×3 小方格用 `(row // 3, col // 3)` 作為 key：

```
┌───────┬───────┬───────┐
│ (0,0) │ (0,1) │ (0,2) │   ← row 0~2
├───────┼───────┼───────┤
│ (1,0) │ (1,1) │ (1,2) │   ← row 3~5
├───────┼───────┼───────┤
│ (2,0) │ (2,1) │ (2,2) │   ← row 6~8
└───────┴───────┴───────┘
```

**為什麼 `// 3` 有效？**
整數除法是「分組神器」：`index // group_size` = 屬於第幾組

| row | row // 3 |
|-----|----------|
| 0, 1, 2 | 0 |
| 3, 4, 5 | 1 |
| 6, 7, 8 | 2 |

### 2. Dict of Sets 的初始化

如果 key 不存在，要先建立空 set：
```python
if row not in rows:
    rows[row] = set()
```

或者用 `defaultdict(set)` 更簡潔：
```python
from collections import defaultdict
rows = defaultdict(set)  # 自動建立空 set
```

---

## 最終正確 Code

```python
def isValidSudoku(board: list[list[str]]) -> bool:
    rows = {}     # rows[0] = 第 0 列看過的數字
    cols = {}     # cols[0] = 第 0 行看過的數字
    boxes = {}    # boxes[(0,0)] = 左上角 box 看過的數字

    for row in range(9):
        for col in range(9):
            cell = board[row][col]

            if cell == ".":
                continue

            box_key = (row // 3, col // 3)

            # 如果 key 不存在，先建立空 set
            if row not in rows:
                rows[row] = set()
            if col not in cols:
                cols[col] = set()
            if box_key not in boxes:
                boxes[box_key] = set()

            # 檢查三個維度有沒有重複
            if cell in rows[row]:
                return False
            if cell in cols[col]:
                return False
            if cell in boxes[box_key]:
                return False

            # 沒重複，登記進去
            rows[row].add(cell)
            cols[col].add(cell)
            boxes[box_key].add(cell)

    return True
```

---

## 複雜度分析

| | 複雜度 | 原因 |
|---|--------|------|
| 時間 | **O(1)** | 固定 81 格，每格做 O(1) 的 set 操作 |
| 空間 | **O(1)** | 最多存 81 個數字（固定大小）|

**如果是 n×n 數獨？**
- 時間：O(n²)
- 空間：O(n²)

---

## 面試怎麼回答？

> 「好的，讓我先講一下這題的思路。
>
> **這題要檢查三個維度**：每一列、每一行、每一個 3×3 小方格都不能有重複數字。
>
> **我的策略是**用三組 Hash Set 來記錄「看過的數字」：
> - `rows[i]` 記錄第 i 列看過什麼
> - `cols[j]` 記錄第 j 行看過什麼
> - `boxes[(i//3, j//3)]` 記錄每個 3×3 方格看過什麼
>
> **然後遍歷每一格**，跳過空格，對每個數字檢查三個 set：
> - 如果已經存在 → 有重複 → return False
> - 如果不存在 → 加進去繼續檢查
>
> **關於 box 的 key**：用 `(row // 3, col // 3)` 是因為整數除法會把 0~2 映射到 0、3~5 映射到 1、6~8 映射到 2，剛好分成九宮格。
>
> 時間複雜度 O(1)，因為 board 大小固定是 9×9。」

---

## 學到的技巧

### 1. 整數除法 `//` 是分組神器
當你想把連續數字分成固定大小的組：
- `index // group_size` = 屬於第幾組
- 常用於：分頁、分批處理、grid 座標轉換

### 2. Dict of Sets 追蹤多維度
當你需要在「多個類別」各自追蹤「有沒有重複」：
```python
categories = {}
categories[category_key] = set()
```

### 3. Tuple 可以當 Dict 的 key
`(row // 3, col // 3)` 這種 tuple 可以直接當 dict 的 key！

---

## 相關題目

- [ ] Valid Sudoku II（進階版）
- [ ] Sudoku Solver（回溯法解數獨）

---

## 心得

這題的核心不難：就是「同時檢查三個維度有沒有重複」。

關鍵 insight：
- 想到用 **三組 set** 分別追蹤 row / col / box
- 想到用 **整數除法** 把 9×9 映射到 3×3 的 box key

這個「多維度同時檢查」的 pattern 很常見，記住就好！
