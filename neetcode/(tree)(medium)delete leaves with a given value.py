'''
You are given a binary tree root and an integer target, delete all the leaf nodes with value target.

Note that once you delete a leaf node with value target, if its parent node becomes a leaf node and has the value target, it should also be deleted (you need to continue doing that until you cannot).

Example 1:





Input: root = [1,2,3,5,2,2,5], target = 2

Output: [1,2,3,5,null,null,5]
Example 2:



Input: root = [3,null,3,3], target = 3

Output: []
Explanation: The output is an empty tree after removing all the nodes with value 3.

Constraints:

1 <= number of nodes in the tree <= 3000
1 <= Node.val, target <= 1000

'''

# Definition for a binary tree node.
from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    '''
    . Use a helper function to find the leaves to remove -> do it in a loop until no more leaves 
    '''
    def removeLeafNodes_mysoln(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        def find(node, parent, target_leaves):
            if not node:
                return

            if not node.left and not node.right and node.val == target:
                target_leaves.append((node, parent))
                return

            find(node.left, node, target_leaves)
            find(node.right, node, target_leaves)

        while True:
            leaves_to_remove = []
            find(root, None, leaves_to_remove)

            # no more to remove
            if not leaves_to_remove:
                return root

            for leaf, parent in leaves_to_remove:
                if not parent:
                    return None
                    
                if id(parent.left) == id(leaf):
                    parent.left = None
                else:
                    parent.right = None

        return None

    '''
    . Do a post order traversal and remove the leaves when you find them
    . after removing, check if the parent is now a leaf and if so, remove it too
    '''
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        if not root:
            return None

        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        if not root.left and not root.right and root.val == target:
            return None

        return root