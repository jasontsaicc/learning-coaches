# #110 Balanced Binary Tree

模式:兔(換皮題,母題 #543 雙軌)。

圖解頁:https://claude.ai/artifact/7X8DRQAu86S36mdc9AGBZ9

## 這題的重點

- 平衡 = **每一個** node 的左右高度差 ≤ 1。不是 node 數量一樣,也不是葉子一樣深。
- 只看 root 不夠:`[1,2,2,3,None,None,3,4,None,None,4]` root 兩邊都高 3,但 node 2 差 2。
- 跟 #543 同一個外殼,**只換記帳那一軌**。往上交的永遠是高度。
- 帳本初始 `True`:`if` 只會寫 `False`,沒找到問題時沒人碰帳本,所以初始值 = 沒問題時的答案。
- 複雜度:O(n) time,O(h) space(call stack)。

```python
class Solution:
    def isBalanced(self, root):
        self.ok = True

        def depth(node):
            if not node:
                return 0
            L = depth(node.left)
            R = depth(node.right)
            if abs(L - R) > 1:
                self.ok = False
            return 1 + max(L, R)

        depth(root)
        return self.ok
```

## 跟母題 #543 差在哪

| | #543 直徑 | #110 平衡 |
|---|---|---|
| 帳本初始值 | `self.ans = 0` | `self.ok = True` |
| 🔴 記帳 | `self.ans = max(self.ans, L + R)` | `if abs(L - R) > 1: self.ok = False` |
| 🟣 往上交 | `return 1 + max(L, R)` | **一樣** |
| 最後回傳 | `return self.ans` | `return self.ok` |

口訣:往上交的永遠是高度,換題只換記帳那一軌。

## L6 逐字稿

Move 3 是換皮題重點:invariant 跟 #543 差在哪一句。

| Move | 說 | 想 | 寫 |
|---|---|---|---|
| 0 | "Does balanced mean every node, or just the root? Is an empty tree balanced?" | 「每一個 node」是這題的陷阱,先問出來 | (手不碰白板) |
| 1 | "Here the root has height 3 on both sides, but node 2 has a left height of 2 and a right height of 0. So this is not balanced." | 自己舉的例子直接打中「只看 root」 | ★ 樹,每個 node 標左高/右高 |
| 2 | "I could call a height function at every node. That's O(n²) on a skewed tree, because I compute the same heights again and again." | 暴力解浪費的情報:小孩的高度算過了,爸爸又重算 | `abs(h(L) - h(R)) <= 1 and bal(L) and bal(R)` |
| 3 | "It's the same shape as Diameter. Each node hands up its height, and I only change what I record: a flag instead of a max." | invariant:高度往上交不變,只換記帳 | 兩軌圖:🟣 往上交、🔴 記帳 |
| 4 | "One post-order pass gives me both numbers at each node, so each height is computed once." | 選後序是因為要先有 L、R | `L = depth(...)`、`R = depth(...)` 在檢查之前 |
| 5 | "That's O(n) time and O(h) space for the call stack. Sound reasonable?" | 從 O(n²) 降到 O(n) 講出來 | `O(n) / O(h)` |
| 6a | "I start by assuming the tree is balanced." | 帳本只會被改成 False | `self.ok = True` |
| 6b | "At each node I get both heights, check the gap, then hand up my own height." | 5 行骨架 | `if not node: return 0` / `L = depth(node.left)` / `R = depth(node.right)` / `if abs(L - R) > 1: self.ok = False` / `return 1 + max(L, R)` |
| 6c | "Run it from the root and return the flag." | 外層只做三件事 | `depth(root)` / `return self.ok` |
| 7 | "On my example, node 2 sees 2 and 0, so the flag flips to false. The root sees 3 and 3, but it can't flip it back." | 用 Move 1 的例子 | 在 node 2 打叉 |
| 8 | "An empty tree returns true, because no node ever touches the flag." | 點名哪個設計讓 edge case 自動對 | `[] -> True` |
| 9 | "To stop early, I could return -1 as a signal for 'unbalanced' and skip the rest." | follow-up:early exit 版 | `if L == -1 or R == -1 or abs(L-R) > 1: return -1` |

### 只給結論 vs 說明推理

| | 只給結論 | 說明推理 |
|---|---|---|
| Move 3 | "I'll use DFS." | "Same shape as Diameter. I only change what I record." |
| Move 6a | 直接寫 `self.ok = True` | "I start by assuming it's balanced, and only a bad node can flip it." |

### Native English

- "It's the same shape as X. I only change what I record."
- "I start by assuming it's true, and only a bad case can flip it."
- "Each height is computed once, so it's O(n)."
- "It can't flip it back."

## 這次的釐清

```
✗ 我以為:平衡 = 左右 node 數量一樣,或葉子都一樣深
✓ 其實是:每個 node 左右「高度」差 ≤ 1
→ 為什麼會搞混:日常用語的平衡;要看「每一個」node,不是只看 root

✗ 我以為:這題把 max 換成相減
✓ 其實是:相減只用在記帳(檢查);往上交的還是 1 + max(L, R)
→ 為什麼會搞混:兩軌混成一軌。爸爸要的是高度,拿到差距就算不出自己的差距

✗ 我以為:左右中 = 前序
✓ 其實是:左右中 = 後序。看「中」放在哪
```

## 檔案

- `drill.py`:9 組 case。空 stub 9/9 FAIL 已驗,參考解 9/9 PASS 已驗。學員版 9/9 PASS。

## 進度

- 2026-09-18:兔模式。「平衡」定義看不懂(以為是 A node 數量 / C 葉子同深),畫高度表 + 反例後懂。
  自己講出後序順序(名字講成前序)、base `0`、`+1`、`> 1`。把往上交也換成相減,
  學員說累要求直接給答案。第一次冷寫:5 行邏輯全對,但直接寫在 `isBalanced` 裡(沒內層函式),
  `if` 裡不知道寫什麼。補外殼 + `self.ok` 紙條圖 + 為什麼初始 `True`。
  第二次:`isBalanced(node.left)` 應為 `depth`、`false` 應為 `False`,指行號後自改,9/9 綠。
  學員回饋:「教得好亂」(一則訊息塞太多件事)、溫度計 ② 不要問要翻 case 清單的題目。
