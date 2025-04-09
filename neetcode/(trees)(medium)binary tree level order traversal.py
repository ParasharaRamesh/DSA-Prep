'''
Given a binary tree root, return the level order traversal of it as a nested list, where each sublist contains the values of nodes at a particular level in the tree, from left to right.

Example 1:



Input: root = [1,2,3,4,5,6,7]

Output: [[1],[2,3],[4,5,6,7]]
Example 2:

Input: root = [1]

Output: [[1]]
Example 3:

Input: root = []

Output: []
Constraints:

0 <= The number of nodes in both trees <= 1000.
-1000 <= Node.val <= 1000
'''

from collections import defaultdict, deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels = defaultdict(list)
        all_levels = []

        def helper(node, depth):
            if not node:
                return

            levels[depth].append(node.val)

            helper(node.left, depth + 1)
            helper(node.right, depth + 1)

        helper(root, 0)

        sorted_levels = sorted(levels.keys())
        for level in sorted_levels:
            all_levels.append(levels[level])

        return all_levels

    def levelOrder_bfs(self, root: Optional[TreeNode]) -> List[List[int]]:
        res = []

        q = deque()
        q.append(root)

        while q:
            qLen = len(q)
            level = []
            for i in range(qLen):
                node = q.popleft()
                if node:
                    level.append(node.val)

                    q.append(node.left)
                    q.append(node.right)
            if level:
                res.append(level)

        return res
