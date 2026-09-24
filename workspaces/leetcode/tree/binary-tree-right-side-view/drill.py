"""#199 Binary Tree Right Side View (兔模式,#102 換皮)

跑法:  python3 drill.py

  Given the root of a binary tree, imagine yourself standing on the right side
  of it, return the values of the nodes you can see ordered from top to bottom.
  Constraints:
    - The number of nodes in the tree is in the range [0, 100]
    - -100 <= Node.val <= 100
  例:  input [1,2,3,null,5,null,4]   output [1,3,4]

下面是 levelOrder 原封不動貼過來。只改一行。
"""
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root):
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level[-1])          # ← 改這行
        return res


# ── 以下不用改 ────────────────────────────────────────────
def build(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


CASES = [
    # (輸入 level-order,             期望答案,       這個 case 在考什麼)
    ([],                            [],             "空樹"),
    ([1],                           [1],            "單一 node"),
    ([1, 2, 3, None, 5, None, 4],   [1, 3, 4],      "題目原例"),
    ([1, None, 3],                  [1, 3],         "右斜"),
    ([1, 2, 3, 4],                  [1, 3, 4],      "★ 左邊比較深:第 3 層最右邊是左子樹的 4"),
    ([1, 2, None, 3],               [1, 2, 3],      "★ 左斜鏈:沒有右小孩,看到的全是左邊"),
]


def main():
    s = Solution()
    passed = 0
    for vals, want, why in CASES:
        got = s.rightSideView(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {str(vals):<30} want={want} got={got}   {why}")
    print(f"── rightSideView: {passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
