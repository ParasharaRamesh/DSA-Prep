from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addValToTail(self, head, tail, val):
        if tail:
            tail.next = ListNode(val)
            tail = tail.next
        else:
            tail = ListNode(val)
            head = tail

        return head, tail

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        h1 = list1
        h2 = list2

        head, tail = None, None

        while h1 and h2:
            if h1.val <= h2.val:
                head, tail = self.addValToTail(head, tail, h1.val)
                h1 = h1.next
            else:
                head, tail = self.addValToTail(head, tail, h2.val)
                h2 = h2.next

        if tail and not h1:
            tail.next = h2
            return head
        elif tail and not h2:
            tail.next = h1
            return head
        elif not tail and not h2:
            return h1
        elif not tail and not h1:
            return h2
        else:
            return None