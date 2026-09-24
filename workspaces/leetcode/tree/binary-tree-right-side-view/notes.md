# #199 Binary Tree Right Side View

模式:兔(換皮題,母題 #102 Level Order)。Harness:`drill.py`(6 組,改前 1/6、參考解 6/6 已驗)。
圖解頁:沿用 #102 的 https://claude.ai/artifact/KQJwrWzUqYZGukafwmZ1LZ(「口訣加模板」換皮表第一列)。

## 這題的重點

- 每層最右邊那個 = `level[-1]`。跟 #102 只差 `res.append(level)` → `res.append(level[-1])`。
- 最右邊不一定長在右子樹:`[1,2,3,4]` 第 3 層只有 4,在左邊。一直走 `.right` 會得到 `[1, 3]`。
- 複雜度:O(n) time,O(w) space(w = 最寬一層,最壞約 n/2)。

## L6 逐字稿

Move 3 是換皮題重點:跟 #102 差在哪一句。

| Move | 說 | 想 | 寫 |
|---|---|---|---|
| 0 | "Is 'visible from the right' the last node of each level, even if it sits in the left subtree?" | 先把「右子樹」陷阱問出來 | (手不碰白板) |
| 1 | "In this tree, 3 has no children, but 2 has a left child 4. So I see 1, 3, and 4." | 自己舉的例子直接打中陷阱 | `[1,2,3,4]` 樹,每層圈最右邊 |
| 2 | "Just walking right children gives 1 and 3. It misses 4." | 暴力想法錯在哪 | `[1, 3]` 打叉 |
| 3 | "It's level order traversal. I only change what I keep from each level: the last value instead of the whole list." | invariant 跟 #102 一樣:每圈開始 q 剛好是一層 | `res.append(level[-1])` |
| 4 | "The queue keeps left-to-right order, so the last node I pop in a round is the rightmost one." | 為什麼 `[-1]` 一定是最右 | |
| 5 | "Each node goes in and out once, so O(n) time. The queue holds one level, so O(width) space." | | `O(n) / O(w)` |
| 6 | "Same code as level order, one line changed." | 不用重講整份模板 | 整份 #102 code,改一行 |
| 7 | "On my example: round one keeps 1, round two keeps 3, round three keeps 4." | 用 Move 1 的例子 | |
| 8 | "Empty tree returns an empty list, because of the guard at the top." | | `[] -> []` |

## 紀錄

- 2026-09-24:兔模式 6/6。「怎麼從 levelOrder 輸出變答案」答「index 0, 1」→ 表格後「從右邊數」。
  改哪行答成 `popleft`、填空答 `popright`,連錯 2 次給答案。溫度計 ②(只走 `.right` 漏什麼)一次對。
