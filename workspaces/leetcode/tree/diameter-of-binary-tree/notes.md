# #543 Diameter of Binary Tree

圖解頁:https://claude.ai/code/artifact/3e1f50f4-6869-4513-83ec-1154bb6d793a
(重點是第 04 節「每個 node 身上有兩個數字」兩張並排樹圖 + 第 05 節帳本 7 格)

模式:龜(第一題「雙軌」— 遞迴回傳值 + 全域帳本同時存在)。
#104 是「只有軌道 A」的特例,所以這題不是新題型,是同一個模板長出第二條軌道。

## 這題的重點

- **length 數的是 edge,不是 node。** 單一 node 答案 0,兩個 node 答案 1。
  跟 #104 剛好差一格,最容易翻車的地方。
- 每個 node 身上有兩個數字,長得像、意思完全不同:

| | 算式 | 為什麼 |
|---|---|---|
| 軌道 A 往上交 `return` | `max(L,R) + 1` | 上級要繼續往下走,不可能同時走我兩邊 |
| 軌道 B 記帳 `self.ans` | `L + R` | 路在我這裡轉彎,它不需要再往上,兩邊都能用 |

- 兩者的差 = `min(L,R) - 1`。**只有 `min(L,R) == 1` 時才剛好相等**,
  小樹上常常撞同值,會騙過自己。葉子(`min=0`)其實就已經分岔了:記帳 0、往上交 1。
- 最後 `return self.ans`,**不是** `return depth(root)`。`depth(root)` 的回傳值沒人接,丟掉。

```python
class Solution:
    def diameterOfBinaryTree(self, root):
        self.ans = 0
        def depth(node):
            if not node:
                return 0
            L = depth(node.left)
            R = depth(node.right)
            self.ans = max(self.ans, L + R)   # 軌道 B
            return max(L, R) + 1              # 軌道 A (= #104)
        depth(root)
        return self.ans
```

- 複雜度:Time O(n)、Space O(h)。斜鏈 + 10^4 node 會爆 Python recursion limit(預設 1000),
  面試講到這裡就加分,真要解就 `sys.setrecursionlimit` 或改 iterative post-order。

## 模板遷移(整個系列只換兩行)

| 題 | 軌道 B 記帳 | 軌道 A 往上交 |
|---|---|---|
| #543 Diameter | `L + R` | `max(L,R) + 1` |
| #124 Max Path Sum | `node.val + L + R` | `node.val + max(L,R,0)` |
| #110 Balanced | `abs(L-R) <= 1` | `max(L,R) + 1` |
| #104 Max Depth | (沒有軌道 B) | `max(L,R) + 1` |

## 檔案

- `drill.py`:9 組 case。空 stub 0/9 FAIL 已驗,參考解 9/9 PASS 已驗。
  ★ case `[1,2,None,3,4,5,None,None,6]` 專抓「只算 root」的寫法。
- `scope-demo.py`:`self.ans` vs `nonlocal` vs `ans[0]` 五種寫法的可跑對照
  (含 `co_varnames` / `co_freevars` 證據)。這題以外也通用。
- `eli5.html`:已發布,見上方 URL。
- 尚無 solution.py。

## 進度

- 2026-09-11:龜模式全跑完。學員一次冷寫 9/9 綠(五格全對,含最後一行交帳本不交回傳值),
  只掛在 `amx` 手滑 + stub 留下的死骨架。
  **對話中補了兩個洞**(兩個都是學員主動問出來的,見圖解頁「這次的釐清」):
  ① 遞迴第一步是「一路向左」不是「直接到最深的節點」— 開始順序 vs 結束順序沒分開。
  ② `self.ans` 為什麼不用宣告、`nonlocal` 是什麼 — 接回 9/07 自己問出的判準
     「看 `=` 左邊有沒有 `.`」。
  未做:溫度計 ②(已出題:記帳那行拿掉 `max` 會掛幾個 case)、solution.py。
