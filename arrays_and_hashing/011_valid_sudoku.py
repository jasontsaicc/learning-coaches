"""
LeetCode 36. Valid Sudoku
https://leetcode.com/problems/valid-sudoku/

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need
to be validated according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes must contain the digits 1-9 without repetition.

Note:
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
- Only the filled cells need to be validated according to the mentioned rules.

Example 1:
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true

Example 2:
Input: board =
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: 第一列 (column 0) 有兩個 "8"，所以不合法

---
中文翻譯：
檢查一個 9x9 的數獨是否有效（只檢查已填入的數字）。
規則：每一行、每一列、每一個 3x3 小方格都不能有重複數字。
"""

def isValidSudoku(board: list[list[str]]) -> bool:
    """
    思路：
    1. 遍歷每一個格子 board[row][col]
    2. 如果是 "." 就跳過
    3. 如果是數字，檢查三件事：
       - 這個數字在「這一 row」有沒有出現過？
       - 這個數字在「這一 col」有沒有出現過？
       - 這個數字在「這一 box」有沒有出現過？
    4. 用三組 set 來記錄「看過的數字」：
       - rows[row] → 第 row 列看過的數字
       - cols[col] → 第 col 行看過的數字
       - boxes[(row//3, col//3)] → 這個 box 看過的數字

    提示：
    - 可以用 dict 來存多個 set，例如：rows = {}
    - rows[0] 就是「第 0 列的 set」
    - 如果 key 不存在，要先建立空 set
    - 記住：box 的 key 是 (row // 3, col // 3)
    """
    # Step 1: 建立三個「書包櫃」，用來裝每一列/行/box 看過的數字
    rows = {}     # rows[0] = 第 0 列看過的數字
    cols = {}     # cols[0] = 第 0 行看過的數字
    boxes = {}    # boxes[(0,0)] = 左上角 box 看過的數字

    # Step 2: 遍歷每一個格子
    for row in range(9):
        for col in range(9):

            # Step 3: 拿到這個格子的值
            cell = board[row][col]

            # Step 4: 如果是空格 "." 就跳過
            if cell == ".":
                continue

            # Step 5: 算出這個格子屬於哪個 box
            box_key = (row // 3, col // 3)

            # Step 6: 如果 key 不存在，先建立空的 set
            if row not in rows:
                rows[row] = set()
            if col not in cols:
                cols[col] = set()
            if box_key not in boxes:
                boxes[box_key] = set()

            # Step 7: 檢查有沒有重複
            if cell in rows[row]:      # 這一列已經有這個數字了
                return False
            if cell in cols[col]:      # 這一行已經有這個數字了
                return False
            if cell in boxes[box_key]: # 這個 box 已經有這個數字了
                return False

            # Step 8: 沒重複，把數字加進去
            rows[row].add(cell)
            cols[col].add(cell)
            boxes[box_key].add(cell)

    # Step 9: 全部檢查完都沒問題
    return True


# 本地測試
if __name__ == "__main__":
    # 測試案例 1：有效的數獨
    board1 = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    result1 = isValidSudoku(board1)
    print(f"測試 1（有效數獨）: {result1}")
    print(f"預期: True")
    print(f"通過: {result1 == True}")
    print()

    # 測試案例 2：無效的數獨（第一列有兩個 8）
    board2 = [
        ["8","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    result2 = isValidSudoku(board2)
    print(f"測試 2（第一列有兩個 8）: {result2}")
    print(f"預期: False")
    print(f"通過: {result2 == False}")
    print()

    # 測試案例 3：同一個 box 有重複
    board3 = [
        ["5","3",".",".","7",".",".",".","."],
        ["6","5",".",".","9",".",".",".","."],  # (1,1) 有 5，跟 (0,0) 的 5 在同一個 box
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    result3 = isValidSudoku(board3)
    print(f"測試 3（同一個 box 有重複）: {result3}")
    print(f"預期: False")
    print(f"通過: {result3 == False}")
