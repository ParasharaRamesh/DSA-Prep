# Definition for singly-linked list.
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if left == right:
            return head
        
        left -= 1
        right -= 1

        prev, after = None, None
        i = 0
        curr = head
        
        l = None
        r = None

        while i <= right:
            if i == left:
                l = curr
            
            if i == right:
                r = curr
                after = r.next

            i += 1

            if not l:
                prev = curr

            curr = curr.next 

        self.reverse(l, r)

        if prev:
            prev.next = r

        l.next = after

        return head if left > 0 else r

    # both are nodes
    def reverse(self, l, r):
        if l == r:
            return l

        self.reverse(l.next, r)

        l.next.next = l
        l.next = None

