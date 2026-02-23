'''
You are given the head of a linked list head, in which each node contains an integer value.

Between every pair of adjacent nodes, insert a new node with a value equal to the greatest common divisor of them.

Return the head of the linked list after insertion.

The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.

Example 1:

Input: head = [12,3,4,6]

Output: [12,3,3,1,4,2,6]
Example 2:

Input: head = [2,1]

Output: [2,1,1]
Constraints:

1 <= The length of the list <= 5000.
1 <= Node.val <= 1000
'''

from typing import Optional
from math import gcd

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head

        while curr.next:
            after = curr.next

            hcf = gcd(curr.val, after.val)
            node_to_insert = ListNode(hcf)
            
            curr.next = node_to_insert
            node_to_insert.next = after

            curr = after

        return head
        