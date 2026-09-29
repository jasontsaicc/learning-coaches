"""#637 Average of Levels in Binary Tree (兔模式,#102 換皮)

跑法:  python3 drill.py

  Given the root of a binary tree, return the average value of the nodes
  on each level in the form of an array.
  Constraints:
    - The number of nodes in the tree is in the range [1, 10^4]
    - -2^31 <= Node.val <= 2^31 - 1
  例:  input [3,9,20,null,null,15,7]   output [3.0, 14.5, 11.0]

從頭寫。卡住就翻 ../binary-tree-level-order-traversal/bfs-queue-model.md。
"""
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfLevels(self, root):
        pass


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
    # (輸入 level-order,               期望答案,           這個 case 在考什麼)
    ([1, 2, 3, 4, 5],                 [1, 2.5, 4.5],      "我們那棵樹"),
    ([3, 9, 20, None, None, 15, 7],   [3, 14.5, 11],      "題目原例"),
    ([5],                             [5],                "單一 node"),
    ([1, -1, -2],                     [1, -1.5],          "負數"),
    ([2147483647, 2147483647, 2147483647], [2147483647, 2147483647], "★ 最大值相加(Python int 不會 overflow)"),
]


def main():
    s = Solution()
    passed = 0
    for vals, want, why in CASES:
        got = s.averageOfLevels(build(vals))
        ok = (isinstance(got, list) and len(got) == len(want)
              and all(isinstance(g, (int, float)) and abs(g - w) < 1e-5 for g, w in zip(got, want)))
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {str(vals):<32} want={want} got={got}   {why}")
    print(f"── averageOfLevels: {passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
