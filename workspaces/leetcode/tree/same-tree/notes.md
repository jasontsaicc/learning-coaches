# #100 Same Tree

模式:兔(換皮題,母題 #104)。沒有圖解頁,L6 逐字稿與這次的釐清都寫在這裡。

## 這題的重點

- 兩個 node 一起走。煞車有 3 種組合,不是 1 種:

| p | q | 結果 |
|---|---|---|
| ▢ | ▢ | `True` |
| ● | ▢ / ▢ ● | `False` |
| ● | ● | 比值,再往下 |

- **兩個煞車的順序不能換**:先攔「都空」(`and`),再攔「一邊空」(`or`)。
  `or` 單看也會抓到 ▢▢,只是 ▢▢ 在上一行已經 `return` 走了。
- 比值用 `p.val != q.val`,不用 `not p.val`(`val=0` 是 falsy)。
- 本層判斷放在委派**之前**:root 就不同時直接 `return False`,整棵子樹都不用比。
  `and` 本身也 short-circuit,左邊 False 就不呼叫右邊。
- 兩棵樹真的一樣時,還是要比完全部 node。early exit 只在「不同」時省時間。
- 複雜度:O(min(n, m)) time,O(h) space(call stack)。

```python
class Solution:
    def isSameTree(self, p, q):
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

## 跟母題 #104 差在哪

| 零件 | #104 Max Depth | #100 Same Tree |
|---|---|---|
| 參數 | 1 個 node | 2 個 node 一起走 |
| 煞車 | 空 → `0` | 都空 `True`、一邊空 `False` |
| 本層 | 委派之後(要 L、R) | 委派之前(可 early exit) |
| 合併 | `max(L, R) + 1` | `左 and 右` |

## 前序 / 中序 / 後序(本場釐清)

判準看 code:「處理自己」那行在兩個遞迴呼叫的前、中、後。
判準看題目:站在一個 node 上問「答案靠誰給我資料?」

| 資料來源 | 順序 | 題目訊號 | 例 |
|---|---|---|---|
| 小孩交上來 | 後序 | 高度、深度、直徑、子樹、平衡 | #104、#543、#110 |
| 爸爸傳下來 | 前序 | root 到 leaf、沿路加總 | #112 |
| BST 排序 | 中序 | BST + 第 k 小 / 合法 | #98、#230 |
| 自己能先判斷且可能提早結束 | 放前面 | 比較兩棵樹 | #100 |

口訣:子樹的事問小孩,路上的事問爸爸,BST 排序用中序。

## L6 逐字稿

Move 3 是換皮題重點:invariant 跟 #104 差在哪一句。

| Move | 說 | 想 | 寫 |
|---|---|---|---|
| 0 | "Can either tree be empty? Does 'same' mean both shape and values?" | 空樹是這題一半的 edge case,先問清楚 | (手不碰白板) |
| 1 | "So `[1,2]` and `[1,null,2]` have the same values but different shapes. That should return false." | 自己舉的例子直接打中「只比數量」的誤解 | 兩棵樹,空位畫 ▢ |
| 2 | "I could serialize both trees and compare the strings, but I need null markers, and I'd always walk both trees fully." | 暴力解浪費的情報:第一個不同的 node 就能下結論 | `serialize(p) == serialize(q)` |
| 3 | "Two trees are the same if the roots match, the left subtrees are the same, and the right subtrees are the same. That's the same shape as max depth, but I combine two booleans with `and` instead of `max`." | invariant 就是題目定義本身;跟 #104 只差合併運算 | `same(p,q) = p.val==q.val and same(L) and same(R)` |
| 4 | "I check the current values before I recurse, so a mismatch near the root stops early." | 選前序是為了 early exit,不是隨便擺 | 比值那行畫在委派上面 |
| 5 | "Time is O(n) in the worst case, space is O(h) for the call stack. Sound reasonable?" | O(h) 講出是 call stack | `O(n) / O(h)` |
| 6a | "Both empty means they match." | 先攔都空 | `if p is None and q is None: return True` |
| 6b | "If only one is empty, they don't match. Order matters here." | 防 `or` 誤抓 ▢▢ | `if p is None or q is None: return False` |
| 6c | "Compare values, then both children with `and`." | `and` short-circuit | `if p.val != q.val: return False` / `return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)` |
| 7 | "On `[1,2]` vs `[1,null,2]`: roots match, then left is node vs null, so it returns false." | 用 Move 1 的例子 | 在兩棵樹上打勾 |
| 8 | "A root with value 0 works because I check `is None`, not truthiness." | 點名哪個設計讓 edge case 自動對 | `[0] vs [0]` |
| 9 | "This helper is the building block for Subtree of Another Tree: call it at every node." | 解一類不是解一題 | → #572 |

### 只給結論 vs 說明推理

| | 只給結論 | 說明推理 |
|---|---|---|
| Move 4 | "I'll check the value first." | "I check the value before I recurse, so a mismatch near the root stops early." |
| Move 6b | 直接寫兩個 if | "Order matters here: the both-empty case must come first." |

### Native English

- "That's the same shape as X, but I combine the results with Y instead of Z."
- "I check this before I recurse, so a mismatch stops early."
- "Order matters here."
- "This is the building block for the next problem."

## 檔案

- `drill.py`:9 組 case。空 stub 9/9 FAIL 已驗,參考解 9/9 PASS 已驗。學員版 9/9 PASS。

## 進度

- 2026-09-17:兔模式。認型時學員自己提出「從上面開始比,因為越往下 node 越多」(early exit),正確。
  煞車先寫 `== None` 且漏 ●▢,補上後改成 `or` 版(順序原理講過)。本層比值一次寫對,
  沒踩 `not p.val`。委派第一版 `self.isSmaeTree(q.left)`:拼字、少 `p.left`、沒接回傳值也沒 `return`,
  自己覺得怪。`and` 自己答出,委派那行走到階 2 骨架填空後寫對。9/9 綠。
  溫度計 ②(拿掉比值那兩行):答出回傳 True,說成「比數量」,修正為「比形狀」;掛 2 個 case。
