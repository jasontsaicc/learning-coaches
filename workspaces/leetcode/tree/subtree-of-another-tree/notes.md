# #572 Subtree of Another Tree

兔模式,母題 `#100 Same Tree`。2026-09-20。

- 圖解頁:https://claude.ai/artifact/Wx6LVP4dEoGXNVBqPJ4gQ5
- drill:`drill.py`(9 組 case。空 stub 9/9 FAIL 已驗、參考解 9/9 PASS 已驗、學員版 9/9 PASS)

## 解

```python
def isSubtree(self, root, subRoot):
    if not root:
        return False
    if self.isSameTree(root, subRoot):
        return True
    return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

`isSameTree` 是 `#100` 原封不動搬過來當 helper。Time `O(m*n)`,Space `O(h)`。
follow-up:serialize 兩棵樹(要有 null marker)+ KMP → `O(m+n)`。

## 口訣

**找一個 → `or`。比全部 → `and`。**
`#572` 是找(藏在哪都行),`#100` 是比(每個 node 都要一樣)。

## 家族表

| 題 | 交回什麼 | 這一站做的事 | 順序 | 借了誰 |
|---|---|---|---|---|
| #104 | 數字(高度) | `1 + max(L, R)` | 後序 | — |
| #543 | 數字(直徑) | 記帳 `max(ans, L+R)` | 後序 | #104 |
| #110 | bool | 記帳 `abs(L-R) > 1` | 後序 | #104 |
| #100 | bool | `p.val != q.val` | 前序 | — |
| #572 | bool | `isSameTree(root, subRoot)` | 前序 | #100 |

前序 vs 後序判準:**這件事需不需要等小孩的答案?** 不需要 → 前序(可 early exit)。需要 → 後序。

## 這次的釐清

1. ✗ 以為 `#100` 是「相減、不小於 0」 → ✓ 那是 `#110`。`#100` 沒碰過數字。
2. ✗ 以為 `#100` 是後序 → ✓ 前序,`p.val != q.val` 在兩個委派前面。
3. ✗ `if not node:` → ✓ `if not root:`。frame 裡只有 `self` / `root` / `subRoot`。
4. ✗ `self.isSubtree(root, subRoot)` 當比對用 → ✓ `self.isSameTree`。參數原封不動傳給自己 = 問題沒變小 = infinite recursion。
5. ✗ code 寫在冷寫區註解旁邊 → ✓ 註解不算一層縮排,要刪掉再寫。
6. `SyntaxError`(少冒號)在整個檔案讀進來時就炸,會蓋掉後面的 `NameError`。
7. harness 掛了先看 fail/pass 分布。1/9 的那筆 PASS 是「小樹=大樹」,直接指向「只走第一站」。

L6 逐字稿(Move 0-9)在圖解頁的摺疊區塊。
