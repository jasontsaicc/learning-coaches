"""#235 Lowest Common Ancestor of a Binary Search Tree (龜模式,BST 首刷)

跑法:  python3 drill.py

  Given a binary search tree (BST) where all node values are unique, and two
  nodes from the tree p and q, return the lowest common ancestor (LCA).
  A node is allowed to be a descendant of itself.
  例:  root = [5,3,8,1,4,7,9,null,2], p = 3, q = 8   output 5

三列表:
  都比 node 小          -> 往左
  都比 node 大          -> 往右
  其他全部(分邊或相等) -> 答案就是 node
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        # ── 打在這裡 ──────────────────────────────────────
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
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


def find(node, val):
    while node and node.val != val:
        node = node.left if val < node.val else node.right
    return node


TREE = [5, 3, 8, 1, 4, 7, 9, None, 2]
CASES = [
    # (樹,  p,  q,  期望,  這個 case 在考什麼)
    (TREE, 3, 8, 5, "題目原例:第一站就分邊"),
    (TREE, 1, 4, 3, "先一起往左,到 3 分邊"),
    (TREE, 3, 4, 3, "p 就是 node 自己"),
    (TREE, 7, 9, 8, "一起往右"),
    (TREE, 2, 1, 1, "往下走三站,q 是 p 的祖先"),
    (TREE, 2, 9, 5, "最深 vs 最右"),
    ([2, 1], 2, 1, 2, "兩個 node 的樹"),
]

if __name__ == "__main__":
    passed = 0
    for vals, p, q, want, why in CASES:
        root = build(vals)
        got = Solution().lowestCommonAncestor(root, find(root, p), find(root, q))
        got = got.val if got else None
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  p={p} q={q}  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
