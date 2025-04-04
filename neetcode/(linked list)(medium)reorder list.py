'''
You are given the head of a singly linked-list.

The positions of a linked list of length = 7 for example, can intially be represented as:

[0, 1, 2, 3, 4, 5, 6]

Reorder the nodes of the linked list to be in the following order:

[0, 6, 1, 5, 2, 4, 3]

Notice that in the general case for a list of length = n the nodes are reordered to be in the following order:

[0, n-1, 1, n-2, 2, n-3, ...]

You may not modify the values in the list's nodes, but instead you must reorder the nodes themselves.

Example 1:

Input: head = [2,4,6,8]

Output: [2,8,4,6]
Example 2:

Input: head = [2,4,6,8,10]

Output: [2,10,4,8,6]
Constraints:

1 <= Length of the list <= 1000.
1 <= Node.val <= 1000


'''

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        order = []

        curr = head
        while curr:
            after = curr.next

            curr.next = None
            order.append(curr)

            curr = after

        l = 0
        r = len(order) - 1

        if l == r:
            return

        # print(f"l : {l}, r: {r}")

        connect = None

        while l < r:
            a = order[l]
            b = order[r]

            # print(f"@{l}: {a.val}, @{r}: {b.val}, connect: {connect.val if connect else None}")

            if connect:
                connect.next = a
                # print(f"{connect.val}->{a.val}")

            a.next = b
            # print(f"{a.val}->{b.val}")

            connect = b

            l += 1
            r -= 1

        # add middle element to end
        if l == r:
            order[l + 1].next = order[l]
            # print(f"{order[l+1].val}->{order[l].val}")
