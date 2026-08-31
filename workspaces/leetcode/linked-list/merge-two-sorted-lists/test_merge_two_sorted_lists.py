import random
import pytest

from solution import Solution, ListNode


def build(vals):
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


@pytest.mark.parametrize("a,b,expected", [
    ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
    ([], [], []),
    ([], [0], [0]),
    ([0], [], [0]),
    ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([4, 5, 6], [1, 2, 3], [1, 2, 3, 4, 5, 6]),
    ([2, 2, 2], [2, 2], [2, 2, 2, 2, 2]),
    ([-9, -3, 0], [-7, 5], [-9, -7, -3, 0, 5]),
])
def test_merge(a, b, expected):
    got = Solution().mergeTwoLists(build(a), build(b))
    assert to_list(got) == expected


def test_reuses_nodes_no_extra_space():
    """O(1) space: nodes get re-linked, not rebuilt."""
    a, b = build([1, 3]), build([2, 4])
    originals = {id(a), id(a.next), id(b), id(b.next)}
    merged = Solution().mergeTwoLists(a, b)
    assert {id(n) for n in _walk(merged)} == originals


def _walk(node):
    while node:
        yield node
        node = node.next


@pytest.mark.timeout(5)
def test_large_n():
    n = 100_000
    a = sorted(random.randint(-10**6, 10**6) for _ in range(n))
    b = sorted(random.randint(-10**6, 10**6) for _ in range(n))
    got = Solution().mergeTwoLists(build(a), build(b))
    assert to_list(got) == sorted(a + b)
