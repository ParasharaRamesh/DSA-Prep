'''
You are given a square 2-D matrix of distinct integers grid where each integer grid[i][j] represents the elevation at position (i, j).

Rain starts to fall at time = 0, which causes the water level to rise. At time t, the water level across the entire grid is t.

You may swim either horizontally or vertically in the grid between two adjacent squares if the original elevation of both squares is less than or equal to the water level at time t.

Starting from the top left square (0, 0), return the minimum amount of time it will take until it is possible to reach the bottom right square (n - 1, n - 1).

Example 1:



Input: grid = [[0,1],[2,3]]

Output: 3
Explanation: For a path to exist to the bottom right square grid[1][1] the water elevation must be at least 3. At time t = 3, the water level is 3.

Example 2:



Input: grid = [
  [0,1,2,10],
  [9,14,4,13],
  [12,3,8,15],
  [11,5,7,6]]
]

Output: 8
Explanation: The water level must be at least 8 to reach the bottom right square. The path is [0, 1, 2, 4, 8, 7, 6].

Constraints:

grid.length == grid[i].length
1 <= grid.length <= 50
0 <= grid[i][j] < n^2

'''
from typing import List
from heapq import *


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        n = len(grid)

        # since we know that these two spots are there for sure
        height = max(grid[0][0], grid[n - 1][n - 1])

        frontier = [(grid[0][0], (0, 0))]
        visited = set()

        while frontier:
            curr_height, coords = heappop(frontier)
            i, j = coords

            if coords in visited:
                continue

            height = max(height, curr_height)
            visited.add(coords)

            if coords == (n - 1, n - 1):
                break

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and (ni, nj) not in visited:
                    heappush(frontier, (grid[ni][nj], (ni, nj)))

        return height

if __name__ == '__main__':
    s = Solution()

    grid = [
        [0,2],
        [1,3]
    ]
    expected = 3
    res = s.swimInWater(grid)
    assert res == expected, f"expected: {expected}, res: {res}"

    grid = [
        [0,1,2,3,4],
        [24,23,22,21,5],
        [12,13,14,15,16],
        [11,17,18,19,20],
        [10,9,8,7,6]
    ]
    expected = 16
    res = s.swimInWater(grid)
    assert res == expected, f"expected: {expected}, res: {res}"