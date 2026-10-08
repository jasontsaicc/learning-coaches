"""開場對照打:前序模板

跑法:  python3 drill-preorder.py
看不懂就打開 warmup-preorder.py 對照抄。
"""

from types import resolve_bases


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root):
        # ── 打在這裡 ──────────────────────────────────────
        # (1) 裝結果的 list
        # (2) def dfs(node): 走到 None 就停
        # (3)               先記下自己
        # (4)               再往左、再往右
        # 最後:從 root 開始走,交回結果
        res = []

        def dfs(node):
            if not node:
                return
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return res

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


CASES = [
    ([], []),
    ([1], [1]),
    ([1, None, 2, 3], [1, 2, 3]),
    ([1, 2, 3, 4, 5, 6, 7], [1, 2, 4, 5, 3, 6, 7]),
]

if __name__ == "__main__":
    passed = 0
    for vals, want in CASES:
        got = Solution().preorderTraversal(build(vals))
        ok = got == want
        passed += ok
        print(("PASS" if ok else "FAIL"), vals, "want", want, "got", got)
    print(f"{passed}/{len(CASES)}")
