'''

Refer to -> https://leetcode.com/problems/construct-quad-tree/description/

Given a n * n matrix grid of 0's and 1's only. We want to represent grid with a Quad-Tree.

Return the root of the Quad-Tree representing grid.

A Quad-Tree is a tree data structure in which each internal node has exactly four children. Besides, each node has two attributes:

val: True if the node represents a grid of 1's or False if the node represents a grid of 0's. Notice that you can assign the val to True or False when isLeaf is False, and both are accepted in the answer.
isLeaf: True if the node is a leaf node on the tree or False if the node has four children.
class Node {
    public boolean val;
    public boolean isLeaf;
    public Node topLeft;
    public Node topRight;
    public Node bottomLeft;
    public Node bottomRight;
}
We can construct a Quad-Tree from a two-dimensional area using the following steps:

If the current grid has the same value (i.e all 1's or all 0's) set isLeaf True and set val to the value of the grid and set the four children to Null and stop.
If the current grid has different values, set isLeaf to False and set val to any value and divide the current grid into four sub-grids as shown in the photo.
Recurse for each of the children with the proper sub-grid.
'''
from typing import List


# Definition for a QuadTree node.
class Node:
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class Solution:
    def get_unique_val_in_node(self, grid: List[List[int]]) -> set:
        unique = set()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                unique.add(grid[i][j])

        return unique

    def construct(self, grid: List[List[int]]) -> 'Node':
        n = len(grid)

        # unlikely base case
        if n == 0:
            return None

        # actual base case
        if n == 1:
            return Node(
                val=(grid[0][0] == 1),
                isLeaf=True,
                topLeft=None,
                topRight=None,
                bottomLeft=None,
                bottomRight=None
            )

        vals = self.get_unique_val_in_node(grid)

        # leaf node
        if len(vals) == 1:
            return Node(
                val=(grid[0][0] == 1),
                isLeaf=True,
                topLeft=None,
                topRight=None,
                bottomLeft=None,
                bottomRight=None
            )

        # not a leaf node
        val = False
        root = Node(
            val,
            False,
            None,
            None,
            None,
            None
        )

        # get the grids
        mid = n//2

        top_left_grid = [row[:mid] for row in grid[:mid]]
        top_right_grid = [row[mid:] for row in grid[:mid]]

        bottom_left_grid = [row[:mid] for row in grid[mid:]]
        bottom_right_grid = [row[mid:] for row in grid[mid:]]

        #connect it
        root.topLeft = self.construct(top_left_grid)
        root.topRight = self.construct(top_right_grid)
        root.bottomLeft = self.construct(bottom_left_grid)
        root.bottomRight = self.construct(bottom_right_grid)

        return root
