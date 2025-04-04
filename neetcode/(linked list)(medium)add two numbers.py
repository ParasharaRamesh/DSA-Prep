'''
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.



Example 1:


Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]
Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]


Constraints:

The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.
'''
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        curr1 = l1
        curr2 = l2

        res = None
        curr3 = None

        carry = 0

        while curr1 and curr2:
            carry, val = divmod(carry + curr1.val + curr2.val, 10)
            node = ListNode(val)

            # first time
            if not res:
                res = node
                curr3 = res
            else:
                curr3.next = node
                curr3 = curr3.next

            curr1 = curr1.next
            curr2 = curr2.next

        if not curr1 and curr2:
            while curr2:
                carry, val = divmod(carry + curr2.val, 10)
                node = ListNode(val)
                curr3.next = node
                curr3 = curr3.next
                curr2 = curr2.next
        elif not curr2 and curr1:
            while curr1:
                carry, val = divmod(carry + curr1.val, 10)
                node = ListNode(val)
                curr3.next = node
                curr3 = curr3.next
                curr1 = curr1.next

        if carry > 0:
            node = ListNode(carry)
            curr3.next = node
            curr3 = curr3.next

        return res