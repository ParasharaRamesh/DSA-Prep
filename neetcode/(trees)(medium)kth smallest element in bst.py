'''
Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) in the tree.

A binary search tree satisfies the following constraints:

The left subtree of every node contains only nodes with keys less than the node's key.
The right subtree of every node contains only nodes with keys greater than the node's key.
Both the left and right subtrees are also binary search trees.
Example 1:



Input: root = [2,1,3], k = 1

Output: 1
Example 2:



Input: root = [4,3,5,2,null], k = 4

Output: 5
Constraints:

1 <= k <= The number of nodes in the tree <= 1000.
0 <= Node.val <= 1000

'''

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def __init__(self):
        self.id_to_num = dict()

    def numNodes(self, root):
        if not root:
            return 0

        if id(root) in self.id_to_num:
            return self.id_to_num[id(root)]

        self.id_to_num[id(root)] = 1 + self.numNodes(root.left) + self.numNodes(root.right)
        return self.id_to_num[id(root)]

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        if not root:
            return 0

        num_left, num_right = 0, 0

        if root.left:
            num_left = self.numNodes(root.left)

        if root.right:
            num_right = self.numNodes(root.right)

        if k == num_left + 1:
            return root.val
        elif k <= num_left:
            return self.kthSmallest(root.left, k)
        else:
            return self.kthSmallest(root.right, k - (num_left + 1))
