'''
Leetcode 314: https://leetcode.com/problems/binary-tree-vertical-order-traversal/

Given the root of a binary tree, return the vertical order traversal of its nodes' values. (i.e., from top to bottom, column by column).

If two nodes are in the same row and column, the order should be from left to right.

Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]


Input: root = [3,9,8,4,0,1,7]
Output: [[4],[9],[3,0,1],[8],[7]]


Input: root = [1,2,3,4,10,9,11,null,5,null,null,null,null,null,null,null,6]
Output: [[4],[2,5],[1,10,9,6],[3],[11]]

Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100

Insights:

* do dfs, and keep track of vertical and horizontal depths as we go

'''
from typing import Optional, List
from collections import defaultdict

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        order = defaultdict(list)

        def helper(node, level, depth):
            if not node:
                return

            # add the levels
            order[level].append((node.val, depth))

            helper(node.left, level - 1, depth + 1)
            helper(node.right, level + 1, depth + 1)

        helper(root, 0, 0)
        verticalOrder = []

        for level in sorted(order.keys()):
            items = order[level]
            items.sort(key=lambda item: item[1])

            nodes = list(map(lambda item: item[0], items))
            verticalOrder.append(nodes)

        return verticalOrder
