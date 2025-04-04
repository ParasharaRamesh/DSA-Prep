'''
You are given the beginning of a linked list head, and an integer n.

Remove the nth node from the end of the list and return the beginning of the list.

Example 1:

Input: head = [1,2,3,4], n = 2

Output: [1,2,4]
Example 2:

Input: head = [5], n = 1

Output: []
Example 3:

Input: head = [1,2], n = 2

Output: [2]
Constraints:

The number of nodes in the list is sz.
1 <= sz <= 30
0 <= Node.val <= 100
1 <= n <= sz
'''
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd_sentinel_two_pointers(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        sent = ListNode(0, head)
        left = sent
        right = head

        while n > 0:
            right = right.next
            n -= 1

        while right:
            left = left.next
            right = right.next

        left.next = left.next.next
        return sent.next

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        N = 0
        curr = head
        while curr:
            curr = curr.next
            N += 1

        j = N - n  # 0 index

        i = 0
        curr = head
        prev = None

        while curr and i < j:
            prev = curr
            curr = curr.next
            i += 1

        if prev:
            prev.next = curr.next
            curr.next = None
            return head
        else:
            new_head = curr.next
            curr.next = None
            return new_head
