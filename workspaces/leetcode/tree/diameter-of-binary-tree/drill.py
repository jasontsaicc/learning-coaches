"""#543 Diameter of Binary Tree - 第一題「雙軌遞迴」(回傳值 + 全域帳本)

跑法:  python3 drill.py

Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two
nodes in a tree. This path may or may not pass through the root.
The length of a path between two nodes is represented by the number of edges
between them.

Constraints:
  - The number of nodes in the tree is in the range [1, 10^4]
  - -100 <= Node.val <= 100

例:  input  [1,2,3,4,5]   output 3    (路徑 4-2-1-3, 3 條邊)
     input  [1,2]         output 1

口訣: 往上交要挑一邊 (max), 記帳本可以吃兩邊 (+)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root):
        # ── 冷寫區 ────────────────────────────────────────
        # 0. 帳本  -> 全域最大值放哪?初始值是多少?
        self.ans = 0

        def depth(node):
            # 1. 煞車  -> 空的 node 往下最深幾格?
            if not node:
                return 0
            # 2. 委派  -> 左右各叫一次,把回傳值接住 (注意 node.)
            L = depth(node.left)
            R = depth(node.right)
            self.ans = max(self.ans, L+R)
            
            # 3. 記帳  -> 穿過「我」的最長路是幾條邊?跟帳本比大小
            return max(L, R) + 1
        depth(root)
            # 4. 往上交 -> 上級只能走我其中一邊

        # 5. 啟動 + 交答案 -> 回傳值要不要接?最後 return 什麼?
        return self.ans
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


CASES = [
    # (輸入 level-order,            期望答案, 這個 case 在考什麼)
    ([1, 2, 3, 4, 5],                  3, "題目原例,最長路穿過 root"),
    ([1, 2],                           1, "兩個 node = 1 條邊,不是 2"),
    ([1],                              0, "單一 node,沒有邊,答案 0 不是 1"),
    ([],                               0, "空樹 (LeetCode 保證 >=1,但煞車要頂得住)"),
    ([1, 2, None, 3, None, 4, None, 5], 4, "左斜鏈 5 個 node = 4 條邊"),
    ([1, 2, 3, 4, 5, 6, 7],            4, "滿樹,4-2-1-3-6"),
    ([1, 2, None, 3, 4, 5, None, None, 6], 4, "★ 最長路「不」經過 root"),
    ([1, 2, 3, 4, None, None, 5, 6, None, None, 7], 6, "兩側都深,轉彎在 root"),
    ([1, None, 2, None, 3],            2, "右斜鏈"),
]


def main():
    passed = 0
    for vals, want, why in CASES:
        got = Solution().diameterOfBinaryTree(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {str(vals):<42} want={want} got={got}   {why}")
    print(f"\n{passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
