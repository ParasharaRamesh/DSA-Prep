'''
You are given a 2-D grid of integers matrix, where each integer is greater than or equal to 0.

Return the length of the longest strictly increasing path within matrix.

From each cell within the path, you can move either horizontally or vertically. You may not move diagonally.

Example 1:



Input: matrix = [[5,5,3],[2,3,6],[1,1,1]]

Output: 4
Explanation: The longest increasing path is [1, 2, 3, 6] or [1, 2, 3, 5].

Example 2:



Input: matrix = [[1,2,3],[2,1,4],[7,6,5]]

Output: 7
Explanation: The longest increasing path is [1, 2, 3, 4, 5, 6, 7].

Constraints:

1 <= matrix.length, matrix[i].length <= 100

'''
from typing import List
from collections import defaultdict


class Solution:
    def longestIncreasingPath_memo(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        cache = dict()

        # the fact that we dont need a visited set is because none of the older values would anyways make it in the current path because of the strict increasing check => no potential for cycles
        def dfs(i, j):
            key = (i, j)

            if key in cache:
                return cache[key]

            # just that cell alone
            res = 1
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[i][j] < matrix[ni][nj]:
                    res = max(res, 1 + dfs(ni, nj))

            cache[key] = res
            return res

        longest_path = 0
        for i in range(m):
            for j in range(n):
                longest_path = max(longest_path, dfs(i, j))

        return longest_path

    # bottom up: need to sort all cells, and process it that way because essentially that is the reverse topological order in this case!
    def longestIncreasingPath_tabulation(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        # Create a list of cells with their values
        cells = []
        for i in range(m):
            for j in range(n):
                cells.append((matrix[i][j], i, j))

        # Sort cells by value in descending order
        cells.sort(reverse=True)

        # Initialize DP table
        dp = [[1 for _ in range(n)] for _ in range(m)]

        longest_path = 1  # At minimum, path length is 1

        # Process cells in descending order of value
        for _, i, j in cells:
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[i][j] < matrix[ni][nj]:
                    dp[i][j] = max(dp[i][j], 1 + dp[ni][nj])

            longest_path = max(longest_path, dp[i][j])

        return longest_path

if __name__ == '__main__':
    s = Solution()

    matrix = [[1, 2], [4, 3]]
    expected = 4
    res = s.longestIncreasingPath(matrix)
    assert res == expected, f"{expected = } , {res = }"

    matrix = [[5, 5, 3], [2, 3, 6], [1, 1, 1]]
    expected = 4
    res = s.longestIncreasingPath(matrix)
    assert res == expected, f"{expected = } , {res = }"

    matrix = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    expected = 4
    res = s.longestIncreasingPath(matrix)
    assert res == expected, f"{expected = } , {res = }"

    matrix = [[3, 4, 5], [3, 2, 6], [2, 2, 1]]
    expected = 4
    res = s.longestIncreasingPath(matrix)
    assert res == expected, f"{expected = } , {res = }"

    matrix = [[1, 2, 3], [2, 1, 4], [7, 6, 5]]
    expected = 7
    res = s.longestIncreasingPath(matrix)
    assert res == expected, f"{expected = } , {res = }"
