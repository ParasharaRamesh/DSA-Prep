'''
You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * (10^9).

Example 1:

Input: obstacleGrid = [[0,0,0],[0,0,0],[0,1,0]]

Output: 3
Explanation: There are three ways to reach the bottom-right corner:

Right -> Right -> Down -> Down
Right -> Down -> Right -> Down
Down -> Right -> Right -> Down
Example 2:

Input: obstacleGrid = [[0,0,0],[0,0,1],[0,1,0]]

Output: 0
Constraints:

m == obstacleGrid.length
n == obstacleGrid[i].length
1 <= m, n <= 100
obstacleGrid[i][j] is 0 or 1.

'''

from typing import List
from functools import cache

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        # edge case where you cannot even start
        if obstacleGrid[0][0] == 1:
            return 0

        is_valid = lambda i, j: (0 <= i < m) and (0 <= j < n)

        # No need to use a visited set because the same cell can be visited from top and from left also and we need to count it in both cases. If we used visited we will not able to count both paths

        @cache
        def dfs(i, j):
            if i == m - 1 and j == n - 1:
                return 1

            total = 0
            dir = [(0, 1), (1, 0)]
            for di, dj in dir:
                ni = i + di
                nj = j + dj

                if is_valid(ni, nj) and obstacleGrid[ni][nj] == 0:
                    total += dfs(ni, nj)

            return total

        return dfs(0, 0)