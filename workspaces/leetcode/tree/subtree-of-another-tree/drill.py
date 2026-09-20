"""#572 Subtree of Another Tree  (兔模式,母題 #100 Same Tree)

跑法:  python3 drill.py

Given the roots of two binary trees root and subRoot, return true if there is a
subtree of root with the same structure and node values of subRoot and false
otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and
all of this node's descendants. The tree tree could also be considered as a
subtree of itself.

Constraints:
  - The number of nodes in the root tree is in the range [1, 2000]
  - The number of nodes in the subRoot tree is in the range [1, 1000]
  - -10^4 <= root.val, subRoot.val <= 10^4

例:  root = [3,4,5,1,2]                 subRoot = [4,1,2]    -> True
     root = [3,4,5,1,2,null,null,null,null,0]  subRoot = [4,1,2]  -> False
       (大樹的 node 2 底下還掛著一個 0,整塊剪下來就不一樣了)

isSameTree 是你 9/17 自己寫的那份,原封不動。這題只要寫外層。
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSubtree(self, root, subRoot):
       # ── 冷寫區:五行 ──────────────────────────────────
        # 1. 煞車   -> 走到空的大樹,代表什麼?交回什麼?
        if not root:
            return False
        # 2. 問一次 -> 站在這一站,拿 isSameTree 比一下。像的話呢?
        if self.isSameTree(root, subRoot):
            return True
        # 3. 委派   -> 左右各走一次。兩邊用 and 還是 or?
        
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
        # ────────────────────────────────────────────────

    # ── 你 9/17 寫的 #100,不要改 ────────────────────────
    def isSameTree(self, p, q):
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# ── 以下不用改 ────────────────────────────────────────────
def build(vals):
    """LeetCode level-order list -> tree。None 代表沒有小孩。"""
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
    # (root,                                      subRoot,       期望, 這個 case 在考什麼)
    ([3, 4, 5, 1, 2],                             [4, 1, 2],     True,  "題目原例,藏在 node 4"),
    ([3, 4, 5, 1, 2, None, None, None, None, 0],  [4, 1, 2],     False, "★ 多一個 0,不能只剪一半"),
    ([3, 4, 5, 1, 2],                             [3, 4, 5, 1, 2], True, "整棵樹是自己的 subtree"),
    ([1, 2, 3],                                   [2],           True,  "單一 node 的葉子也算"),
    ([1, 2, 3],                                   [1, 2],        False, "★ 值對但結構不對:root 有右小孩"),
    ([1, 2, 3],                                   [1, 3, 2],     False, "★ 值一樣,左右顛倒"),
    ([4, 2, 6, 1, 3, 5, 7],                       [6, 5, 7],     True,  "藏在右子樹"),
    ([1, 1],                                      [1, None, 1],  False, "★ 左小孩不等於右小孩"),
    ([3, 4, 5, 1, 2],                             [4, 1],        False, "★ 少剪一顆也不算"),
]


def main():
    s = Solution()
    passed = 0
    for r, sub, want, why in CASES:
        got = s.isSubtree(build(r), build(sub))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  root={str(r):<38} sub={str(sub):<16} want={want} got={got}   {why}")
    print(f"\n{passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
