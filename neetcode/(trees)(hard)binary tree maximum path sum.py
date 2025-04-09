'''
Given the root of a non-empty binary tree, return the maximum path sum of any non-empty path.

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can not appear in the sequence more than once. The path does not necessarily need to include the root.

The path sum of a path is the sum of the node's values in the path.

Example 1:



Input: root = [1,2,3]

Output: 6
Explanation: The path is 2 -> 1 -> 3 with a sum of 2 + 1 + 3 = 6.

Example 2:



Input: root = [-15,10,20,null,null,15,5,-5]

Output: 40
Explanation: The path is 15 -> 20 -> 5 with a sum of 15 + 20 + 5 = 40.

Constraints:

1 <= The number of nodes in the tree <= 1000.
-1000 <= Node.val <= 1000

'''
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def get_max_path_sum(self, node):
        paths = []

        def helper(node, curr_path):
            if not node:
                return

            paths.append(sum(curr_path + [node.val]))

            if node.left:
                helper(node.left, curr_path + [node.val])

            if node.right:
                helper(node.right, curr_path + [node.val])

        helper(node, [])
        return max(paths)

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return float("-inf")

        if not root.left and not root.right:
            return root.val

        left_max_path_sum = float("-inf")
        right_max_path_sum = float("-inf")

        if root.left:
            left_max_path_sum = self.get_max_path_sum(root.left)

        if root.right:
            right_max_path_sum = self.get_max_path_sum(root.right)

        max_sum_with_root = max(
            root.val,
            left_max_path_sum + root.val,
            root.val + right_max_path_sum,
            left_max_path_sum + root.val + right_max_path_sum
        )
        return max(max_sum_with_root, self.maxPathSum(root.left), self.maxPathSum(root.right))