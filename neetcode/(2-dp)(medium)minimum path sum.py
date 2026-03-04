'''
Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

 

Example 1:


Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.
Example 2:

Input: grid = [[1,2,3],[4,5,6]]
Output: 12
 

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 200
0 <= grid[i][j] <= 200
'''
from functools import cache

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        is_valid = lambda i, j : 0 <= i < m  and 0 <= j < n

        @cache
        def f(i, j):
            if not is_valid(i, j):
                return float("inf")

            if i == m - 1 and j == n - 1:
                return grid[i][j]

            right = grid[i][j] + f(i, j+1)
            down = grid[i][j] + f(i+1, j)
            return min(right, down)

        return f(0, 0)
