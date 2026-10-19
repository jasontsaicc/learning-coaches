"""#98 Validate Binary Search Tree (龜模式,前序 + 往下傳兩張紙條 首刷)

跑法:  python3 drill.py

  Given the root of a binary tree, determine if it is a valid BST:
  - left subtree of a node contains only nodes with keys less than the node's key
  - right subtree contains only nodes with keys greater than the node's key
  - both subtrees are also BSTs
  例:  root = [2,1,3]  -> True     root = [5,1,4,null,null,3,6]  -> False

一句話:
  每個 node 帶兩張紙條往下走: low(我要比它大)、high(我要比它小)
  往左走 high 換成我,往右走 low 換成我
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root):
        # ── 打在這裡 ──────────────────────────────────────
        # (1) def dfs(node, low, high): 走到 None -> 交回 True
        def dfs(node, low, high):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False
            left_ok = dfs(node.left, low, node.val)
            right_ok = dfs(node.right, node.val, high)
            return left_ok and right_ok
        return dfs(root, float('-inf'), float('inf'))
        # (2)     我不在 low < 我 < high 裡面 -> 交回 False

        # (3)     左小孩拿 (low, 我),右小孩拿 (我, high),兩邊都要 True

        # 最後: 從 root 開始走(第一組紙條寫什麼?),交回結果
        
        # ────────────────────────────────────────────────


# ── 以下不用改 ────────────────────────────────────────────
def build(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = [root], 1
    while queue and i < len(vals):
        node = queue.pop(0)
        for side in ("left", "right"):
            if i < len(vals):
                if vals[i] is not None:
                    child = TreeNode(vals[i])
                    setattr(node, side, child)
                    queue.append(child)
                i += 1
    return root


CASES = [
    # (樹,  期望,  這個 case 在考什麼)
    ([2, 1, 3], True, "題目原例 1"),
    ([5, 1, 4, None, None, 3, 6], False, "題目原例 2:右小孩 4 < 5"),
    ([5, 4, 6, None, None, 3, 7], False, "孫子陷阱:3 < 6 沒錯,但 3 在 5 的右邊"),
    ([10, 5, 15, None, None, 6, 20], False, "同一招換數字:6 在 10 的右邊"),
    ([2, 2, 2], False, "相等不行(嚴格小於)"),
    ([1], True, "只有 root"),
    ([3, 1, 5, 0, 2, 4, 6], True, "滿的合法 BST"),
    ([0, -1], True, "負數也要對(紙條起點不能是 0)"),
]

if __name__ == "__main__":
    passed = 0
    for vals, want, why in CASES:
        got = Solution().isValidBST(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {vals}  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
