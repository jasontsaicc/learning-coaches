"""開場默寫(2 分鐘)- 雙軌題的「外殼」

跑法:  python3 drill.py

這次考的不是邏輯,是外殼。9/18 #110 你把 5 行邏輯寫對了,但直接寫在
isBalanced 裡面,外殼組不起來。所以今天邏輯我給你,外殼你補。

#543 Diameter of Binary Tree
  Given the root of a binary tree, return the length of the diameter of the tree.
  The diameter of a binary tree is the length of the longest path between any two
  nodes in a tree. This path may or may not pass through the root.
  The length of a path between two nodes is represented by the number of EDGES
  between them.
  Constraints:
    - The number of nodes in the tree is in the range [1, 10^4]
    - -100 <= Node.val <= 100
  例:  input [1,2,3,4,5]  output 3   (路徑 4 - 2 - 1 - 3,3 條邊)

2 分鐘寫不出來就說「不會」,走卡住協定,不糾纏。
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root):
        self.ans = 0

        def depth(node):
            if not node:
                return 0
            L = depth(node.left)
            R = depth(node.right)
            self.ans = max(self.ans, L + R)   # 🔴 記帳
            return 1 + max(L, R)              # 🟣 往上交

        depth(root)
        return self.ans


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
    # (輸入 level-order,                 期望答案, 這個 case 在考什麼)
    ([],                                0,  "空樹,煞車要頂得住"),
    ([1],                               0,  "單一 node,0 條邊"),
    ([1, 2],                            1,  "一條邊"),
    ([1, 2, 3, 4, 5],                   3,  "題目原例:4-2-1-3"),
    ([1, 2, None, 3],                   2,  "左斜鏈"),
    ([4, 2, 6, 1, 3, 5, 7],             4,  "滿樹,穿過 root"),
    ([1, 2, 3, None, None, 4, None, 5], 4,  "★ 最左不等於最深"),
    ([1, 2, None, 3, 4, 5, None, None, 6], 4, "★ 最長路徑不穿過 root"),
]


def main():
    s = Solution()
    passed = 0
    for vals, want, why in CASES:
        got = s.diameterOfBinaryTree(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {str(vals):<36} want={want} got={got}   {why}")
    print(f"\n{passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
