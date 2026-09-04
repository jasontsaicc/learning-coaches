class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1, list2):
        # 冷寫區 — 學員 2026-09-04 速刷
        dummy = ListNode(0)
        tail = dummy

        while list1 and list2:
            if list1.val > list2.val:
                tail.next = list2
                list2 = list2.next
            else:
                tail.next = list1
                list1 = list1.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next
