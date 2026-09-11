"""#104 Maximum Depth of Binary Tree - 第一題「要吃下屬回傳值」的遞迴

跑法:  python3 drill.py

Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Constraints:
  - The number of nodes in the tree is in the range [0, 10^4]
  - -100 <= Node.val <= 100

例:  input  [3,9,20,null,null,15,7]   output 3
     input  [1,null,2]                output 2
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root):
        # ── 冷寫區:遞迴三格 ───────────────────────────────
        # 1. 煞車  -> 什麼時候不再委派?回傳什麼型別?
        #             (判準:上一層要拿它來算什麼)
        if not root:
            return 0
        # 2. 委派  -> 呼叫自己兩次,把回傳值接住
        left = maxDepth(left)
        right = maxDepth(right)

        # 3. 組裝  -> 用下屬的兩個答案,算出「我這一層」的答案
        reuturn max(left, right)+1
        # ────────────────────────────────────────────────
        


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


def chain(n):
    """單邊長鏈 n 節,測「不能隨便選一邊」。回傳 (root, 深度)。"""
    root = TreeNode(0)
    cur = root
    for _ in range(n - 1):
        cur.left = TreeNode(0)
        cur = cur.left
    return root


CASES = [
    ([3, 9, 20, None, None, 15, 7], 3),   # 題目範例
    ([1, None, 2], 2),                    # 只有右小孩
    ([1, 2], 2),                          # 只有左小孩
    ([], 0),                              # 空樹 -> 煞車的回傳值直接被考
    ([1], 1),                             # 單顆
    ([1, 2, 3, 4, None, None, None, 5], 4),  # 左邊深,右邊淺 -> 選錯邊會答 2
    ([1, None, 2, None, 3, None, 4], 4),     # 右邊一路到底
    (list(range(1, 128)), 7),             # 滿樹 7 層
]

if __name__ == "__main__":
    fails = []
    for vals, want in CASES:
        label = f"{vals[:7]}{'...' if len(vals) > 7 else ''}"
        try:
            got = Solution().maxDepth(build(vals))
        except Exception as e:
            fails.append(f"  ✗ {label} -> {type(e).__name__}: {e}")
            continue
        if got != want:
            fails.append(f"  ✗ {label} -> got {got}, want {want}")
    # 額外:單邊 500 節長鏈,測有沒有「只挑一邊」
    try:
        got = Solution().maxDepth(chain(500))
        if got != 500:
            fails.append(f"  ✗ 單邊長鏈 500 -> got {got}, want 500")
    except Exception as e:
        fails.append(f"  ✗ 單邊長鏈 500 -> {type(e).__name__}: {e}")

    total = len(CASES) + 1
    if fails:
        print(f"{len(fails)}/{total} FAIL")
        print("\n".join(fails))
    else:
        print(f"{total}/{total} PASS ✅")
