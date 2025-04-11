'''
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/description/

Given two nodes of a binary tree p and q, return their lowest common ancestor (LCA).

Each node will have a reference to its parent node. The definition for Node is below:

class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
}
According to the definition of LCA on Wikipedia: "The lowest common ancestor of two nodes p and q in a tree T is the lowest node that has both p and q as descendants (where we allow a node to be a descendant of itself)."



Example 1:


Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.
Example 2:


Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5 since a node can be a descendant of itself according to the LCA definition.
Example 3:

Input: root = [1,2], p = 1, q = 2
Output: 1


Constraints:

The number of nodes in the tree is in the range [2, 105].
-109 <= Node.val <= 109
All Node.val are unique.
p != q
p and q exist in the tree.

Insights:
* can do with O(n) space
* can also do with O(1) space with a teleport trick because:
- traversing from p -> root might be < = > then q-> root
- if they are of same length then easy, just move both one by one together
- if they are of different lengths then we can use the algebraic property:
    - distance(p -> root =(teleport)=> q -> lca) = distance(q -> root =(teleport)=> p -> lca)

'''


# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class Solution:
    '''
    O(n) space solution:
    - traverse from one till root and keep track of all the ids in a set
    - travers from the other one till root and keep checking if that id is in the set, the first one which has will be the lca

    '''
    def lowestCommonAncestor_On_space(self, p: 'Node', q: 'Node') -> 'Node':
        # from p -> root
        curr_p = p
        p_ids = set()
        while curr_p:
            p_ids.add(id(curr_p))
            curr_p = curr_p.parent

        # now from q -> root and check the ids along the way
        curr_q = q
        while True:
            if id(curr_q) in p_ids:
                return curr_q

            curr_q = curr_q.parent

    '''
    O(1) space solution:
    - using the teleport trick
    '''
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        curr_p = p
        curr_q = q

        while True:
            if not curr_p:
                curr_p = q
                continue

            if not curr_q:
                curr_q = p
                continue

            if id(curr_p) == id(curr_q):
                return curr_p

            curr_p = curr_p.parent
            curr_q = curr_q.parent
