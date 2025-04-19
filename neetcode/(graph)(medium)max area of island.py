'''
You are given a matrix grid where grid[i] is either a 0 (representing water) or 1 (representing land).

An island is defined as a group of 1's connected horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

The area of an island is defined as the number of cells within the island.

Return the maximum area of an island in grid. If no island exists, return 0.

Example 1:



Input: grid = [
  [0,1,1,0,1],
  [1,0,1,0,1],
  [0,1,1,0,1],
  [0,1,0,0,1]
]

Output: 6
Explanation: 1's cannot be connected diagonally, so the maximum area of the island is 6.

Constraints:

1 <= grid.length, grid[i].length <= 50

'''
from typing import List


class Solution:
    def maxAreaOfIsland_nc(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        visit = set()

        def dfs(r, c):
            if (r < 0 or r == ROWS or c < 0 or
                c == COLS or grid[r][c] == 0 or
                (r, c) in visit
            ):
                return 0
            visit.add((r, c))
            return (1 + dfs(r + 1, c) +
                        dfs(r - 1, c) +
                        dfs(r, c + 1) +
                        dfs(r, c - 1))

        area = 0
        for r in range(ROWS):
            for c in range(COLS):
                area = max(area, dfs(r, c))
        return area

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        all_land = set()
        ROWS = len(grid)
        COLS = len(grid[0])

        isValid = lambda i, j: 0 <= i < ROWS and 0 <= j < COLS

        # keep track of all land
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == 1:
                    all_land.add((i, j))

        # all directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # now do dfs and keep removing from this
        max_area = 0

        while all_land:
            area = 0
            frontier = [list(all_land)[0]]  # start somewhere

            while frontier:
                curr_i, curr_j = frontier.pop()

                if (curr_i, curr_j) in all_land:
                    area += 1
                    all_land.remove((curr_i, curr_j))

                for direction in directions:
                    del_x, del_y = direction
                    new_i, new_j = curr_i + del_x, curr_j + del_y

                    if isValid(new_i, new_j) and (new_i, new_j) in all_land:  # since we would have already seen it
                        frontier.append((new_i, new_j))

            max_area = max(max_area, area)

        return max_area

