# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional
from bisect import *

class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        vals = []

        def inorder(node):
            nonlocal vals 

            if not node:
                return
            
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)

        inorder(root)
        insort(vals, val)

        # now to construct it 
        def construct(l, r):
            if l > r:
                return None

            if l == r:
                return TreeNode(vals[l])

            m = (l + r)//2

            root = TreeNode(vals[m])

            root.left = construct(l, m-1)
            root.right = construct(m+1, r)
            
            return root

        return construct(0, len(vals) - 1)

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        vals = []

        def inorder(node):
            nonlocal vals 

            if not node:
                return
            
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)

        inorder(root)
        i = bisect_left(vals, key)

        if i == len(vals) or vals[i] != key:
            # no need to delete
            return root

        # remove ith index
        vals.pop(i)

        # now to construct it 
        def construct(l, r):
            if l > r:
                return None

            if l == r:
                return TreeNode(vals[l])

            m = (l + r)//2

            root = TreeNode(vals[m])

            root.left = construct(l, m-1)
            root.right = construct(m+1, r)
            
            return root

        return construct(0, len(vals) - 1)
