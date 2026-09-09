"""#141 Linked List Cycle - 開場默寫 (2 分鐘,不看任何東西)

跑法:  python3 drill.py

Given head, the head of a linked list, determine if the linked list has a
cycle in it. There is a cycle if some node can be reached again by
continuously following the next pointer. Return True if there is a cycle,
otherwise False.

Constraints:
  - number of nodes in [0, 10^4]
  - -10^5 <= Node.val <= 10^5
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def hasCycle(self, head) -> bool:
        # ── 冷寫區:從這行往下寫,3 行左右就夠 ──────────────
        # 1. 兩個指標的起手式
        
        slow = head
        fast = head

        # 2. while 條件 (這題唯一會爆 AttributeError 的地方)
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
        # 3. 迴圈裡誰走幾步
        # 4. 比較兩個指標用什麼運算子
        
        # ────────────────────────────────────────────────


# ── 以下不用改 ────────────────────────────────────────────
def build(vals, pos=-1):
    """pos = 尾巴接回第幾個 index;-1 表示無環。"""
    if not vals:
        return None
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


CASES = [
    ([3, 2, 0, -4], 1, True),    # 標準有環
    ([1, 2], 0, True),           # 兩顆成環
    ([1], 0, True),              # 自己指自己
    ([1], -1, False),            # 單顆無環
    ([], -1, False),             # 空 list
    ([1, 2, 3, 4, 5], -1, False),  # 直線無環
    (list(range(10000)), 5000, True),  # 大測資有環
]

if __name__ == "__main__":
    fails = []
    for vals, pos, want in CASES:
        label = f"vals={vals[:6]}{'...' if len(vals) > 6 else ''} pos={pos}"
        try:
            got = Solution().hasCycle(build(vals, pos))
        except Exception as e:
            fails.append(f"  ✗ {label} -> {type(e).__name__}: {e}")
            continue
        if got != want:
            fails.append(f"  ✗ {label} -> got {got!r}, want {want!r}")
    if fails:
        print(f"{len(fails)}/{len(CASES)} FAIL")
        print("\n".join(fails))
    else:
        print(f"{len(CASES)}/{len(CASES)} PASS ✅")
