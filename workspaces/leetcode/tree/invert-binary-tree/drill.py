"""#226 Invert Binary Tree - 遞迴第一題

跑法:  python3 drill.py

Given the root of a binary tree, invert the tree, and return its root.
Inverting means: at every node, swap its left and right children.

Constraints:
  - The number of nodes in the tree is in the range [0, 100]
  - -100 <= Node.val <= 100

例:  input  [4,2,7,1,3,6,9]
     output [4,7,2,9,6,3,1]
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root):
        # ── 冷寫區:遞迴三件事 ─────────────────────────────
        # 1. base case  -> 什麼時候不再委派,直接 return
        if not root:
            return None
        # 2. 這一層自己做的事 -> 只做一層,不要往下追
        root.left, root.right = root.right, root.left
        # 3. 委派 -> 呼叫自己兩次
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
        # 4. return 什麼
        
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


def to_list(root):
    """tree -> level-order list,尾巴的 None 修掉,方便比對。"""
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


CASES = [
    ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),   # 題目範例
    ([2, 1, 3], [2, 3, 1]),                            # 三顆
    ([], []),                                          # 空樹
    ([1], [1]),                                        # 單顆
    ([1, 2], [1, None, 2]),                            # 只有左小孩
    ([1, None, 2], [1, 2]),                            # 只有右小孩
    ([1, 2, 3, 4, None, None, 5], [1, 3, 2, 5, None, None, 4]),  # 不對稱
    (list(range(1, 128)), None),                       # 滿樹,只檢查不爆炸 + 翻兩次回原狀
]

if __name__ == "__main__":
    fails = []
    for vals, want in CASES:
        label = f"{vals[:7]}{'...' if len(vals) > 7 else ''}"
        try:
            got = to_list(Solution().invertTree(build(vals)))
        except Exception as e:
            fails.append(f"  ✗ {label} -> {type(e).__name__}: {e}")
            continue
        if want is None:
            # 翻兩次要回到原狀 (involution)
            twice = to_list(Solution().invertTree(build(got)))
            if twice != vals:
                fails.append(f"  ✗ {label} -> 翻兩次沒回到原狀")
            continue
        if got != want:
            fails.append(f"  ✗ {label} -> got {got}, want {want}")
    if fails:
        print(f"{len(fails)}/{len(CASES)} FAIL")
        print("\n".join(fails))
    else:
        print(f"{len(CASES)}/{len(CASES)} PASS ✅")
