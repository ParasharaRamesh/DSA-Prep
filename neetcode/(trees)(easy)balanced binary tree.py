'''
Given a binary tree, return true if it is height-balanced and false otherwise.

A height-balanced binary tree is defined as a binary tree in which the left and right subtrees of every node differ in height by no more than 1.

Example 1:



Input: root = [1,2,3,null,null,4]

Output: true
Example 2:



Input: root = [1,2,3,null,null,4,null,5]

Output: false
Example 3:

Input: root = []

Output: true
Constraints:

The number of nodes in the tree is in the range [0, 1000].
-1000 <= Node.val <= 1000
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

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root == None:
            return True

        left = 0
        if root.left:
            left = self.height(root.left)

        right = 0
        if root.right:
            right = self.height(root.right)

        return (abs(left - right) <= 1) and (self.isBalanced(root.left)) and (self.isBalanced(root.right))