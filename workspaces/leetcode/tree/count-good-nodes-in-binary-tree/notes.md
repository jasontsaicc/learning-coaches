# #1448 Count Good Nodes in Binary Tree

- Pattern: Tree 前序 + 往下傳值(`dfs(node, max_so_far)`)。龜模式首刷。
- 圖解頁:https://claude.ai/artifact/JzFxwemQcQvzKKHqFbEoNm
- Harness:`drill.py`(7 組,參考解 7/7 PASS 已驗)。

## 紀錄

- 2026-10-09:對照打 7/7 後清空重寫 7/7。修兩格:(5) 交 `node.val` 不是 `new_max`;啟動行用內層名字 `node`。
- 2026-10-13:開場默寫 7/7。新錯:`max(...)` 算了沒接住(補 `new_max =`);外層用 `max_val`(自補 `max_val = root.val`)。
