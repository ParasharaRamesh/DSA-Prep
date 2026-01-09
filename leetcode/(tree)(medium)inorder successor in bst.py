'''
Given the root of a binary search tree and a node p in it, return the in-order successor of that node in the BST. If the given node has no in-order successor in the tree, return null.

The successor of a node p is the node with the smallest key greater than p.val.

 

Example 1:


Input: root = [2,1,3], p = 1
Output: 2
Explanation: 1's in-order successor node is 2. Note that both p and the return value is of TreeNode type.
Example 2:


Input: root = [5,3,6,2,4,null,null,1], p = 6
Output: null
Explanation: There is no in-order successor of the current node, so the answer is null.
 

Constraints:

The number of nodes in the tree is in the range [1, 104].
-105 <= Node.val <= 105
All Nodes will have unique values.
'''

# Definition for a binary tree node.
from typing import Optional

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        successor = None

        curr = root
        while curr:
            # go to the right as it is somewhere there and its successor can never be something previous
            if p.val >= curr.val:
                curr = curr.right
            else:
                # go to the left but bookmark the successor 
                successor = curr
                curr = curr.left

        return successor

    def inorderSuccessor_mysoln(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        # guard
        if not root:
            return None

        # if p is the root, then obviously its in the right subtree's left most
        if p.val == root.val:
            return self.get_leftmost(root.right)

        # the node p itself is in the right subtree so its inorder successor also would be somewhere in the right subtree only 
        if root.val < p.val:
            # get it from the right subtree
            return self.inorderSuccessor(root.right, p)

        # try to find p and keep track of the potential successor along the way
        successor = None
        curr = root
        while curr:
            if curr.val == p.val:
                break
            elif p.val < curr.val:
                # only when taking a left turn do you keep track of the successor 
                successor = curr
                curr = curr.left
            else:
                curr = curr.right

        # if you have found it , get the left most element of its right subtree
        if not curr.right:
            return successor

        return self.get_leftmost(curr.right)

    def get_leftmost(self, node):
        curr = node
        while curr and curr.left:
            curr = curr.left
        return curr