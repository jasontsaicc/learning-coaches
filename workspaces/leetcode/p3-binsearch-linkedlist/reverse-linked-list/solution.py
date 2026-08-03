def reverseList(head):
    # Q4: starting poins (prev = ?, curr = ?)
    prev = None
    curr = head

    # Q5: while <keep-going condition>:
    while curr:
        nxt = curr.next
        # Q2: save

        # Q1: rewirea
        curr.next = prev

        # Q3: advance, advance
        prev = curr
        curr = nxt
    # Q5: return the new head
    return prev
