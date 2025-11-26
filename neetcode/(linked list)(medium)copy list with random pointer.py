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

        '''
        PHASE 1: Create intertwined list structure
        ===========================================
        Create a copy node for each original node and interleave them:
        Original: A -> B -> C -> None
        After:    A -> A' -> B -> B' -> C -> C' -> None
        
        Where A' is copy of A, B' is copy of B, etc.
        
        Key insight: By placing each copy immediately after its original,
        we maintain a direct link: original.next = copy, copy.next = original.next
        This allows us to easily find the copy of any node in Phase 2.
        
        Example:
        Original list: [3] -> [7] -> [4]
        After Phase 1: [3] -> [3'] -> [7] -> [7'] -> [4] -> [4']
        '''
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

        '''
        PHASE 2: Set random pointers for copied nodes
        ==============================================
        Now that we have intertwined structure, we can set random pointers.
        
        For each original node:
        - curr = original node
        - curr.next = copy node (our intertwined structure)
        - curr.random = some original node (or None)
        - curr.random.next = copy of that random node (due to intertwining)
        
        Therefore: copy.random = curr.next.random = curr.random.next
        
        Example:
        If original node A has random pointer to C:
        A.random = C (original)
        A.next = A' (copy of A)
        C.next = C' (copy of C, due to intertwining)
        So: A'.random = A.random.next = C.next = C' ✓
        
        We skip by 2 (curr.next.next) to only visit original nodes.
        '''
        curr = head
        while curr and curr.next:
            if curr.random:
                curr.next.random = curr.random.next
            else:
                curr.next.random = curr.random # both point to null/None

            curr = curr.next.next

        '''
        PHASE 3: Separate the copied list from original list
        =====================================================
        Currently: A -> A' -> B -> B' -> C -> C' -> None
        Goal:      A' -> B' -> C' -> None (and restore original if needed)
        
        We traverse only the copied nodes (starting from copy_head).
        For each copy node:
        - copy_curr.next currently points to next original node
        - copy_curr.next.next points to next copy node
        - So we update: copy_curr.next = copy_curr.next.next
        
        Example:
        Before: A' -> B -> B' -> C -> C' -> None
        A'.next = B, B.next = B'
        After:  A' -> B' -> C' -> None
        A'.next = A'.next.next = B.next = B' ✓
        
        Note: This only fixes the copy list. Original list is modified but
        we don't restore it (problem doesn't require it).
        '''
        copy_curr = copy_head

        while copy_curr and copy_curr.next:
            copy_curr.next = copy_curr.next.next
            copy_curr = copy_curr.next


        # return the new list
        return copy_head

    def copyRandomList_hashmap(self, head: Optional[Node]) -> Optional[Node]:
        old_2_new = dict()

        # make new nodes
        curr = head
        while curr:
            old_2_new[curr] = Node(curr.val)
            curr = curr.next

        # make the deepcopy
        curr = head
        while curr:
            new_curr = old_2_new[curr]

            if curr.next:
                new_curr.next = old_2_new[curr.next]
            
            if curr.random:
                new_curr.random = old_2_new[curr.random]

            curr = curr.next

        return old_2_new[head] if head else None

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