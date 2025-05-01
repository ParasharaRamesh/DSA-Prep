'''
There is an m x n grid where you are allowed to move either down or to the right at any point in time.

Given the two integers m and n, return the number of possible unique paths that can be taken from the top-left corner of the grid (grid[0][0]) to the bottom-right corner (grid[m - 1][n - 1]).

You may assume the output will fit in a 32-bit integer.

Example 1:



Input: m = 3, n = 6

Output: 21
Example 2:

Input: m = 3, n = 3

Output: 6
Constraints:

1 <= m, n <= 100

'''

from math import factorial


class Solution:
    # math approach, combinatorics
    def uniquePaths_math(self, m: int, n: int) -> int:
        num_right = n - 1
        num_left = m - 1
        return factorial(num_right + num_left) // (factorial(num_right) * factorial(num_left))

    # dynamic programming - top down
    def uniquePaths_memo(self, m: int, n: int) -> int:
        cache = dict()
        def helper(i, j):
            key = (i, j)

            if key in cache:
                return cache[key]

            if i >= m or j >= n:
                cache[key] = 0
                return 0

            if i == m - 1 and j == n - 1:
                cache[key] = 1
                return 1

            # num right + num down
            cache[key] = helper(i, j + 1) + helper(i + 1, j)
            return cache[key]

        return helper(0, 0)

    # dynamic programming - bottom up
    def uniquePaths(self, m: int, n: int) -> int:
        cache = dict()

        # base cases
        cache[(m - 1, n - 1)] = 1

        for j in range(n):
            cache[(m, j)] = 0

        for i in range(m):
            cache[(i, n)] = 0

        cache[(m, n)] = 0

        # all states
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if i == m - 1 and j == n - 1:
                    # already computed!
                    continue

                key = (i, j)

                # num right + num down
                cache[key] = cache[(i, j + 1)] + cache[(i + 1, j)]

        return cache[(0, 0)]

