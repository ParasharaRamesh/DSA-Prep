'''
You are given the head of a linked list of length n. Unlike a singly linked list, each node contains an additional pointer random, which may point to any node in the list, or null.

Create a deep copy of the list.

The deep copy should consist of exactly n new nodes, each including:

The original value val of the copied node
A next pointer to the new node corresponding to the next pointer of the original node
A random pointer to the new node corresponding to the random pointer of the original node
Note: None of the pointers in the new list should point to nodes in the original list.

Return the head of the copied linked list.

In the examples, the linked list is represented as a list of n nodes. Each node is represented as a pair of [val, random_index] where random_index is the index of the node (0-indexed) that the random pointer points to, or null if it does not point to any node.

Example 1:



Input: head = [[3,null],[7,3],[4,0],[5,1]]

Output: [[3,null],[7,3],[4,0],[5,1]]
Example 2:



Input: head = [[1,null],[2,2],[3,2]]

Output: [[1,null],[2,2],[3,2]]
Constraints:

0 <= n <= 100
-100 <= Node.val <= 100
random is null or is pointing to some node in the linked list.
'''
from typing import Optional


class Node:
    def __init__(self, x, next = None, random = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        curr = head
        copy_head, copy_curr = None, None

        # make copy and get intertwined
        while curr:
            if not copy_head:
                copy_head = Node(curr.val)
                copy_curr = copy_head

                copy_curr.next = curr.next
                curr.next = copy_curr
            else:
                copy_curr = Node(curr.val)

                copy_curr.next = curr.next
                curr.next = copy_curr

            curr = copy_curr.next

        #  start from head assign its random to its next's random .next
        curr = head
        while curr and curr.next:
            if curr.random:
                curr.next.random = curr.random.next
            else:
                curr.next.random = curr.random # both point to null/None

            curr = curr.next.next

        # change only the next pointers from the new list
        copy_curr = copy_head

        while copy_curr and copy_curr.next:
            copy_curr.next = copy_curr.next.next
            copy_curr = copy_curr.next


        # return the new list
        return copy_head

if __name__ == '__main__':
    three = Node(3)
    seven = Node(7)
    four = Node(4)
    five = Node(5)

    three.next = seven
    three.random = None

    seven.next = four
    seven.random = five

    four.next = five
    four.random = three

    five.random = seven


    ans = Solution().copyRandomList(three)
    print(ans)