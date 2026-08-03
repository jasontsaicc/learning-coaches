import pytest

from solution import reverseList


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def to_pylist(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


@pytest.mark.parametrize("vals", [
    [],
    [1],
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4, 5],
    [7, 7, 7],
])
def test_reverse(vals):
    assert to_pylist(reverseList(build(vals))) == vals[::-1]


def test_in_place_no_new_nodes():
    head = build([1, 2, 3])
    original_ids = set()
    cur = head
    while cur:
        original_ids.add(id(cur))
        cur = cur.next
    cur = reverseList(head)
    reversed_ids = set()
    while cur:
        reversed_ids.add(id(cur))
        cur = cur.next
    assert reversed_ids == original_ids


@pytest.mark.timeout(2)
def test_large_n():
    # recursion blows the stack here; iterative O(1)-space passes
    n = 100_000
    vals = list(range(n))
    assert to_pylist(reverseList(build(vals))) == vals[::-1]
