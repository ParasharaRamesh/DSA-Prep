'''
You are given two integer arrays preorder and inorder.

preorder is the preorder traversal of a binary tree
inorder is the inorder traversal of the same tree
Both arrays are of the same size and consist of unique values.
Rebuild the binary tree from the preorder and inorder traversals and return its root.

Example 1:



Input: preorder = [1,2,3,4], inorder = [2,1,3,4]

Output: [1,2,3,null,null,null,4]
Example 2:

Input: preorder = [1], inorder = [1]

Output: [1]
Constraints:

1 <= inorder.length <= 1000.
inorder.length == preorder.length
-1000 <= preorder[i], inorder[i] <= 1000
unique values

'''
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # inorder = LTR, preorder = TLR
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # base case
        if len(preorder) == 0:
            return None

        # find out where the root node exists in the inorder
        try:
            root = TreeNode(preorder[0])

            root_index = inorder.index(preorder[0])

            left_size = root_index # number of elements in the left subtree

            # build left
            left = self.buildTree(preorder[1: left_size + 1], inorder[:root_index]) # for preorder you know it starts from 1 since the root is the 0th index

            # build right
            right = self.buildTree(preorder[left_size + 1:], inorder[root_index + 1:])

            root.left = left
            root.right = right

            return root
        except ValueError:
            print(f"problem with index {preorder[0]}")
            exit(0)
