"""#110 Balanced Binary Tree - 換皮題(母題 #543,雙軌)

跑法:  python3 drill.py

Given a binary tree, return True if it is height-balanced.
Height-balanced: for EVERY node, the heights of its left and right subtrees
differ by at most 1.

Constraints:
  - The number of nodes in the tree is in the range [0, 5000]
  - -10^4 <= Node.val <= 10^4

例:  [3,9,20,None,None,15,7]        -> True
     [1,2,2,3,3,None,None,4,4]      -> False
     []                             -> True
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root):
        # ── 冷寫區 ────────────────────────────────────────
        self.ok = True
        def depth(node):
            if not node:
                return 0
            L = depth(node.left)
            R = depth(node.right)
            if abs(L -R) > 1:
                self.ok = False
            return 1+max(L, R)
        depth(root)
        return self.ok 


# ── 以下不用改 ────────────────────────────────────────────
def build(vals):
    """LeetCode level-order list -> tree。None 代表沒有小孩。"""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = [root], 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals):
            if vals[i] is not None:
                node.left = TreeNode(vals[i])
                queue.append(node.left)
            i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


CASES = [
    ([3, 9, 20, None, None, 15, 7], True, "題目範例"),
    ([1, 2, 2, 3, 3, None, None, 4, 4], False, "題目範例,左邊深 2 層"),
    ([], True, "空樹算平衡"),
    ([1], True, "單一 node"),
    ([1, 2], True, "差 1 層,還算平衡"),
    ([1, 2, None, 3], False, "左斜鏈 3 個 node,root 差 2"),
    ([1, 2, None, 3, 4], False, "node 2 自己平衡,root 不平衡"),
    ([1, 2, 2, 3, None, None, 3, 4, None, None, 4], False, "★ root 兩邊一樣高,但下面的 node 不平衡"),
    ([1, 2, 3, 4, 5, 6, 7], True, "滿樹"),
]

if __name__ == "__main__":
    fails = []
    for vals, want, why in CASES:
        try:
            got = Solution().isBalanced(build(vals))
        except Exception as e:
            fails.append(f"  ✗ {vals} -> {type(e).__name__}: {e}   ({why})")
            continue
        if got is not want:
            fails.append(f"  ✗ {vals} -> got {got}, want {want}   ({why})")
    if fails:
        print(f"{len(fails)}/{len(CASES)} FAIL")
        print("\n".join(fails))
    else:
        print(f"{len(CASES)}/{len(CASES)} PASS ✅")
