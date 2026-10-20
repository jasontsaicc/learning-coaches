"""#230 Kth Smallest Element in a BST (龜模式,中序走訪 首刷)

跑法:  python3 drill.py

  Given the root of a binary search tree, and an integer k, return the kth
  smallest value (1-indexed) of all the values of the nodes in the tree.
  Constraints:
    - The number of nodes in the tree is n.
    - 1 <= k <= n <= 10^4
    - 0 <= Node.val <= 10^4
  例:  root = [3,1,4,null,2], k = 1  -> 1
       root = [5,3,6,2,4,null,null,1], k = 3  -> 3

一句話:
  BST 中序(左、我、右)收出來就是由小到大,第 k 個是 res[k - 1]
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root, k):
        # ── 打在這裡 ──────────────────────────────────────
        # (1) 收值的 list 放外層;def dfs(node): 走到 None -> return
        #     先往左、收我、再往右(append 夾在兩個呼叫中間)

        # (2) 從 root 啟動

        # (3) 交回第 k 個(k 從 1 數,index 從 0 數)

        # ────────────────────────────────────────────────
        pass


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
    # (樹,  k,  期望,  這個 case 在考什麼)
    ([5, 3, 6, 2, 4, None, None, 1], 3, 3, "圖解頁的例子"),
    ([3, 1, 4, None, 2], 1, 1, "題目原例 1"),
    ([5, 3, 6, 2, 4, None, None, 1], 1, 1, "k=1:最左邊那個,寫成 res[k] 會拿到 2"),
    ([5, 3, 6, 2, 4, None, None, 1], 6, 6, "k=n:最右邊那個,寫成 res[k] 會 IndexError"),
    ([1], 1, 1, "只有 root"),
    ([4, 3, None, 2, None, 1], 2, 2, "全部往左一條線"),
    ([1, None, 2, None, 3, None, 4], 3, 3, "全部往右一條線"),
]

if __name__ == "__main__":
    passed = 0
    for vals, k, want, why in CASES:
        got = Solution().kthSmallest(build(vals), k)
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {vals} k={k}  want={want} got={got}   {why}")
    print(f"{passed}/{len(CASES)}")
