'''
The diameter of a binary tree is defined as the length of the longest path between any two nodes within the tree. The path does not necessarily have to pass through the root.

The length of a path between two nodes in a binary tree is the number of edges between the nodes.

Given the root of a binary tree root, return the diameter of the tree.

Example 1:



Input: root = [1,null,2,3,4,5]

Output: 3
Explanation: 3 is the length of the path [1,2,3,5] or [5,3,2,4].

Example 2:

Input: root = [1,2,3]

Output: 2
Constraints:

1 <= number of nodes in the tree <= 100
-100 <= Node.val <= 100

'''
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def height(self, node):
        if node == None:
            return 0

        return 1 + max(self.height(node.left), self.height(node.right))

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        diameter_through_root = 0
        if root.left:
            left_height = self.height(root.left)
            diameter_through_root += left_height
            # print(f"Left height at {root.val} is {left_height} and total left path is {diameter_through_root}")

        if root.right:
            right_height = self.height(root.right)
            diameter_through_root += right_height
        #    print(f"Right height at {root.val} is {right_height} and total right path is {diameter_through_root}")

        return max(
            diameter_through_root,
            self.diameterOfBinaryTree(root.left),
            self.diameterOfBinaryTree(root.right)
        )