"""#105 Construct Binary Tree from Preorder and Inorder Traversal(速刷)

跑法:  python3 drill.py

  給一棵樹的前序和中序(值都不重複),把樹蓋回來,交回 root。
  例:  preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]

一句話:
  前序第一個是 root;它在中序的位置 mid,就是左子樹有幾個 node
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder, inorder):
        # ── 打在這裡 ──
        if not preorder:
            return None
        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])
        return root


# ── 以下不用改 ────────────────────────────────────────────
def to_list(root):
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


CASES = [
    # (preorder, inorder, 期望(一層一層列), 這個 case 在考什麼)
    ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7], "題目原例"),
    ([-1], [-1], [-1], "只有 root"),
    ([1, 2], [2, 1], [1, 2], "mid=1:只有左小孩"),
    ([1, 2], [1, 2], [1, None, 2], "mid=0:沒有左子樹"),
    ([3, 2, 1], [1, 2, 3], [3, 2, None, 1], "全部往左一條線"),
    ([1, 2, 3], [1, 2, 3], [1, None, 2, None, 3], "全部往右一條線"),
    ([1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7], [1, 2, 3, 4, 5, 6, 7], "滿的三層"),
]

if __name__ == "__main__":
    passed = 0
    for pre, ino, want, why in CASES:
        got = to_list(Solution().buildTree(list(pre), list(ino)))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  pre={pre}  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
