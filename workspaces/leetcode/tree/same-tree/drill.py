"""#100 Same Tree - 換皮題(母題 #104,回傳值從 int 換成 bool)

跑法:  python3 drill.py

Given the roots of two binary trees p and q, return True if they are the same.
Same means: same structure, and every matching node has the same value.

Constraints:
  - The number of nodes in both trees is in the range [0, 100]
  - -10^4 <= Node.val <= 10^4

例:  p [1,2,3]  q [1,2,3]     -> True
     p [1,2]    q [1,None,2]  -> False
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p, q):
        # ── 冷寫區 ────────────────────────────────────────
        # 1. 煞車  -> 兩邊都空?一邊空?
        if p is None and q is None:
            return True
        if p is None or q is  None:
            return False
        

        # 2. 本層  -> 這一格的值一樣嗎?
        if p.val != q.val:
            return False

        # 3. 委派  -> 左跟左比、右跟右比,怎麼把兩個 bool 合起來?
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        
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
    ([1, 2, 3], [1, 2, 3], True, "題目範例"),
    ([1, 2], [1, None, 2], False, "值一樣,結構不同"),
    ([1, 2, 1], [1, 1, 2], False, "結構一樣,值不同"),
    ([], [], True, "兩邊都空"),
    ([1], [], False, "一邊空 (p 有 q 沒有)"),
    ([], [1], False, "一邊空 (q 有 p 沒有)"),
    ([0], [0], True, "val=0 是 falsy,不能用 if not p.val"),
    ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 8], False, "只差在最右下的 leaf"),
    ([1, 2, None, 3], [1, 2, None, 3], True, "左斜三層"),
]

if __name__ == "__main__":
    fails = []
    for pv, qv, want, why in CASES:
        try:
            got = Solution().isSameTree(build(pv), build(qv))
        except Exception as e:
            fails.append(f"  ✗ {pv} vs {qv} -> {type(e).__name__}: {e}   ({why})")
            continue
        if got is not want:
            fails.append(f"  ✗ {pv} vs {qv} -> got {got}, want {want}   ({why})")
    if fails:
        print(f"{len(fails)}/{len(CASES)} FAIL")
        print("\n".join(fails))
    else:
        print(f"{len(CASES)}/{len(CASES)} PASS ✅")
