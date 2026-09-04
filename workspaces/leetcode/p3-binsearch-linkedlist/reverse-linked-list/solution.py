def reverseList(head):
    # 清空重打 — 學員 2026-09-04
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
