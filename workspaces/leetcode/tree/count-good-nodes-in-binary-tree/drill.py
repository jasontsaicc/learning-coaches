"""#1448 Count Good Nodes in Binary Tree (龜模式,前序 + 往下傳值 首刷)

跑法:  python3 drill.py

  Given a binary tree root, a node X in the tree is named good if in the path
  from root to X there are no nodes with a value greater than X.
  Return the number of good nodes in the binary tree.
  例:  root = [3,1,4,3,null,1,5]   output 4

一句話:
  從 root 走到我這站,路上沒有人比我大 -> 我是 good
  往下走時,把「這條路目前最大值」交給小孩
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root):
        # ── 打在這裡 ──────────────────────────────────────
        # (1) 裝 good node 的 list
        res = []

        # (2) def dfs(node, 紙條): 走到 None 就停
        def dfs(node, max_so_far):
            if not node:
                return
            # (3)     我 >= 紙條 -> 記一筆
            if node.val >= max_so_far:
                res.append(node.val)
            # (4)     算要交給小孩的新紙條
            new_max = max(node.val, max_so_far)
            # (5)     左、右小孩都拿新紙條
            dfs(node.left, new_max)
            dfs(node.right, new_max)

        # 最後:從 root 開始走(第一張紙條寫什麼?),交回數量
        dfs(root, root.val)
        return len(res)

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
    # (樹,  期望,  這個 case 在考什麼)
    ([3, 1, 4, 3, None, 1, 5], 4, "題目原例"),
    ([3, 3, None, 4, 2], 3, "相等也算 good(3 >= 3)"),
    ([1], 1, "只有 root,root 一定 good"),
    ([3, 9, 4], 3, "左邊的 9 不能影響右邊的 4(每條路自己的 max)"),
    ([2, None, 4, 10, 8, None, None, 4], 4, "max 變大後,路上小的 4 不 good"),
    ([9, 1, 3, None, None, 6, 5], 1, "root 最大,其他全不 good"),
    ([-1, 5, -2, 4, 4, 2, -2], 3, "負數也要對"),
]

if __name__ == "__main__":
    passed = 0
    for vals, want, why in CASES:
        got = Solution().goodNodes(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {vals}  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
