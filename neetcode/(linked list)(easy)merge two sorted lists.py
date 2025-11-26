from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    # old solution - iterative
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

    # recursive solution
    def mergeTwoLists_recursive(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if list1 is None:
            return list2
        if list2 is None:
            return list1
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2

    # better iterative solution in place
    def mergeTwoLists_iterative(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        res_curr = ListNode()
        res_head = res_curr

        curr1 = list1
        curr2 = list2

        while curr1 and curr2:
            after1 = curr1.next
            after2 = curr2.next

            if curr1.val <= curr2.val:
                res_curr.next = curr1
                curr1.next = None #disconnect
                curr1 = after1
            else:
                res_curr.next = curr2
                curr2.next = None
                curr2 = after2

            res_curr = res_curr.next

        if curr1: 
            res_curr.next = curr1
        elif curr2: 
            res_curr.next = curr2

        return res_head.next