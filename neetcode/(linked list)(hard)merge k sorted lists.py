'''
You are given an array of k linked lists lists, where each list is sorted in ascending order.

Return the sorted linked list that is the result of merging all of the individual linked lists.

Example 1:

Input: lists = [[1,2,4],[1,3,5],[3,6]]

Output: [1,1,2,3,3,4,5,6]
Example 2:

Input: lists = []

Output: []
Example 3:

Input: lists = [[]]

Output: []
Constraints:

0 <= lists.length <= 1000
0 <= lists[i].length <= 100
-1000 <= lists[i][j] <= 1000

'''
from typing import List, Optional
from heapq import *

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        merged, curr = None, None

        # init heap
        heap = []
        pointers = [None] * len(lists)
        for i, listNode in enumerate(lists):
            pointers[i] = listNode
            if listNode:
                heappush(heap, (listNode.val, i))

        while heap:
            smallest_val, i = heappop(heap)
            newNode = ListNode(smallest_val)

            if not merged:
                merged = newNode
                curr = merged
            else:
                curr.next = newNode
                curr = curr.next

            if pointers[i]:
                pointers[i] = pointers[i].next

                if pointers[i]:
                    heappush(heap, (pointers[i].val, i))

        return merged

if __name__ == '__main__':
    lists = []

    #1
    one_0 = ListNode(1)
    one_1 = ListNode(4)
    one_2 = ListNode(5)

    one_0.next = one_1
    one_1.next = one_2

    #2
    two_0 = ListNode(1)
    two_1 = ListNode(3)
    two_2 = ListNode(4)

    two_0.next = two_1
    two_1.next = two_2

    #3
    three_0 = ListNode(2)
    three_1 = ListNode(6)

    three_0.next = three_1

    lists.append(one_0)
    lists.append(two_0)
    lists.append(three_0)

    merged = Solution().mergeKLists(lists)
    print(merged)