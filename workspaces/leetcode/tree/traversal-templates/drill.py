"""Tree 走訪模板複習 - DFS 前序 / 中序 / 後序 + BFS level order

跑法:  python3 drill.py

#144 Binary Tree Preorder Traversal
#94  Binary Tree Inorder Traversal
#145 Binary Tree Postorder Traversal
  Given the root of a binary tree, return the preorder / inorder / postorder
  traversal of its nodes' values.
  Constraints:
    - The number of nodes in the tree is in the range [0, 100]
    - -100 <= Node.val <= 100
  例:  input [1,null,2,3]   preorder [1,2,3]   inorder [1,3,2]   postorder [3,2,1]

#102 Binary Tree Level Order Traversal
  Given the root of a binary tree, return the level order traversal of its
  nodes' values. (i.e., from left to right, level by level).
  Constraints:
    - The number of nodes in the tree is in the range [0, 2000]
    - -1000 <= Node.val <= 1000
  例:  input [3,9,20,null,null,15,7]   output [[3],[9,20],[15,7]]

順序:  先做三個 DFS。BFS 等對話第二層再動。
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root):
        # ── 冷寫區 ────────────────────────────────────────
        # 0. 收集答案的 list 放哪?
        res = [] 
        # 1. 煞車   -> 空 node 做什麼?
        def deepth(node):
            if not node:
                return
        # 2. 做事   -> 把 node.val 收進 list。放在時刻 A / B / C 哪一格?
            res.append(node.val)

        # 3. 委派   -> 左右各叫一次 (注意 node.)
            deepth(node.left)
            deepth(node.right)
        # 4. 啟動 + 交答案
            return None
        deepth(root)
        return res
        # ────────────────────────────────────────────────

    def inorderTraversal(self, root):
        # ── 冷寫區 ── 跟 preorder 只差一行的位置
        res = []
        def deepth(node):
            if not node:
                return
            
            deepth(node.left)
            res.append(node.val)
            deepth(node.right)
        deepth(root)
        return res

    def postorderTraversal(self, root):
        # ── 冷寫區 ── 跟 preorder 只差一行的位置
        res = []
        def deepth(node):
            if not node:
                return
            deepth(node.left)
            deepth(node.right)
            res.append(node.val)
        deepth(root)
        return res

    def levelOrder(self, root):
        # ── 冷寫區 ── 第二層再做。提示: 換掉的不是「做事」的位置,是資料結構
        return None


# ── 以下不用改 ────────────────────────────────────────────
def build(vals):
    """LeetCode level-order list -> tree。None 代表沒有小孩。
    (第二層會回來看這個函式:它自己就是一個 BFS)"""
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


DFS_CASES = [
    # (輸入 level-order,          preorder,          inorder,           postorder,         這個 case 在考什麼)
    ([],                         [],                [],                [],                "空樹,煞車要頂得住"),
    ([1],                        [1],               [1],               [1],               "單一 node,三種順序一樣"),
    ([1, None, 2, 3],            [1, 2, 3],         [1, 3, 2],         [3, 2, 1],         "題目原例"),
    ([1, 2, None, 3],            [1, 2, 3],         [3, 2, 1],         [3, 2, 1],         "左斜鏈:沒有右小孩,B 跟 C 黏在一起"),
    ([1, 2, 3, 4, 5, 6, 7],      [1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7], [4, 5, 2, 6, 7, 3, 1], "滿樹"),
    ([4, 2, 6, 1, 3, 5, 7],      [4, 2, 1, 3, 6, 5, 7], [1, 2, 3, 4, 5, 6, 7], [1, 3, 2, 5, 7, 6, 4], "★ BST 的 inorder 是排好的"),
    ([1, 2, 3, None, None, 4, None, 5], [1, 2, 3, 4, 5], [2, 1, 5, 4, 3], [2, 5, 4, 3, 1], "★ 最左不等於最深 (#543 那棵)"),
]

BFS_CASES = [
    # (輸入 level-order,                 期望答案,                     這個 case 在考什麼)
    ([],                                [],                           "空樹回 [],不是 [[]]"),
    ([1],                               [[1]],                        "單一 node"),
    ([3, 9, 20, None, None, 15, 7],     [[3], [9, 20], [15, 7]],      "題目原例"),
    ([1, 2, None, 3],                   [[1], [2], [3]],              "左斜鏈,每層一個"),
    ([1, 2, 3, 4, 5, 6, 7],             [[1], [2, 3], [4, 5, 6, 7]],  "滿樹"),
    ([1, 2, 3, None, 4, 5],             [[1], [2, 3], [4, 5]],        "★ 同一層來自不同 parent,要併在同一格"),
    ([1, 2, 3, None, None, 4, None, 5], [[1], [2, 3], [4], [5]],      "★ 最左不等於最深"),
]


def run(name, fn, cases):
    passed = 0
    for vals, want, why in cases:
        got = fn(build(vals))
        ok = got == want
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {str(vals):<36} want={want} got={got}   {why}")
    print(f"── {name}: {passed}/{len(cases)} passed\n")
    return passed


def main():
    s = Solution()
    total = 0
    for idx, name in enumerate(["preorder", "inorder", "postorder"], start=1):
        fn = getattr(s, f"{name}Traversal")
        total += run(name, fn, [(c[0], c[idx], c[4]) for c in DFS_CASES])
    total += run("levelOrder", s.levelOrder, BFS_CASES)
    print(f"total {total}/{len(DFS_CASES) * 3 + len(BFS_CASES)}")


if __name__ == "__main__":
    main()
