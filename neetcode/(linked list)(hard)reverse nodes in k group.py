'''
Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.



Example 1:


Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
Example 2:


Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]


Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000


Follow-up: Can you solve the problem in O(1) extra memory space?
'''
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverse(self, node1, node2):
        before = None
        curr = node1

        while curr != node2:
            after = curr.next
            curr.next = before
            before = curr
            curr = after

        curr.next = before

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return None

        curr = head
        group_tail = None
        i = 0

        while curr and i < k:
            group_tail = curr
            curr = curr.next
            i += 1

        #in case we go to the end before counting k
        if not curr and i < k:
            return head
        else:
            next_group_head = self.reverseKGroup(curr, k)

            #reverse till k
            self.reverse(head, group_tail)

            # connect head to next group head
            head.next = next_group_head
            return group_tail