'''
Within a binary tree, a node x is considered good if the path from the root of the tree to the node x contains no nodes with a value greater than the value of node x

Given the root of a binary tree root, return the number of good nodes within the tree.

Example 1:



Input: root = [2,1,1,3,null,1,5]

Output: 3


Example 2:

Input: root = [1,2,-1,3,4]

Output: 4
Constraints:

1 <= number of nodes in the tree <= 100
-100 <= Node.val <= 100
'''


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


'''
for a node x the path from root -> x should not have anything greater than x
'''
class Solution:
    def dfs(self, curr, maxInPathSoFar):
        if not curr:
            return 0

        if curr.val < maxInPathSoFar:
            # Bad case
            return self.dfs(curr.left, maxInPathSoFar) + self.dfs(curr.right, maxInPathSoFar)
        else:
            maxInPathSoFar = curr.val
            return 1 + self.dfs(curr.left, maxInPathSoFar) + self.dfs(curr.right, maxInPathSoFar)

    def goodNodes(self, root: TreeNode) -> int:
        if not root:
            return 0

        return self.dfs(root, root.val)


