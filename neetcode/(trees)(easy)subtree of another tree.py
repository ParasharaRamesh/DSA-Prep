'''
Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's descendants. The tree tree could also be considered as a subtree of itself.

Example 1:



Input: root = [1,2,3,4,5], subRoot = [2,4,5]

Output: true
Example 2:



Input: root = [1,2,3,4,5,null,null,6], subRoot = [2,4,5]

Output: false
Constraints:

0 <= The number of nodes in both trees <= 100.
-100 <= root.val, subRoot.val <= 100
'''

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isExactlySame(self, root1, root2):
        if root1 == None and root2 == None:
            return True
        elif root1 == None and root2 != None:
            return False
        elif root1 != None and root2 == None:
            return False
        elif root1.val == root2.val:
            return self.isExactlySame(root1.left, root2.left) and self.isExactlySame(root1.right, root2.right)

        return False

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if self.isExactlySame(root, subRoot):
            return True

        return (root.left != None and self.isSubtree(root.left, subRoot)) or (
                root.right != None and self.isSubtree(root.right, subRoot))
