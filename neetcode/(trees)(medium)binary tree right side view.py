'''
You are given the root of a binary tree. Return only the values of the nodes that are visible from the right side of the tree, ordered from top to bottom.

Example 1:



Input: root = [1,2,3]

Output: [1,3]
Example 2:

Input: root = [1,2,3,4,5,6,7]

Output: [1,3,7]
Constraints:

0 <= number of nodes in the tree <= 100
-100 <= Node.val <= 100
'''
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, node):
        levels = dict()

        def helper(node, depth):
            if node:
                if depth not in levels:
                    levels[depth] = [node.val]
                else:
                    levels[depth].append(node.val)

                helper(node.left, depth + 1)
                helper(node.right, depth + 1)

        helper(node, 1)
        return levels

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        levels = self.levelOrder(root)
        # print(f"levels are {levels}")

        right = []
        for level in sorted(levels.keys()):
            right.append(levels[level][-1])

        return right

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        res = []

        def dfs(node, depth):
            if not node:
                return None
            
            # effectively the same as level order without the extra space
            if depth == len(res):
                res.append(node.val)

            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return res
