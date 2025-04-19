'''
Given a 2D grid grid where '1' represents land and '0' represents water, count and return the number of islands.

An island is formed by connecting adjacent lands horizontally or vertically and is surrounded by water. You may assume water is surrounding the grid (i.e., all the edges are water).

Example 1:

Input: grid = [
    ["0","1","1","1","0"],
    ["0","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
  ]
Output: 1
Example 2:

Input: grid = [
    ["1","1","0","0","1"],
    ["1","1","0","0","1"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
Output: 4
Constraints:

1 <= grid.length, grid[i].length <= 100
grid[i][j] is '0' or '1'.
'''


class Solution:
    def isValid(self, i, j, ROWS, COLS):
        valid_i = (i >= 0) and (i < ROWS)
        valid_j = (j >= 0) and (j < COLS)
        return valid_i and valid_j

    def numIslands(self, grid: List[List[str]]) -> int:
        all_land = set()
        ROWS = len(grid)
        COLS = len(grid[0])

        # keep track of all land
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == "1":
                    all_land.add((i, j))

        print(f"land is present at indices {all_land}, number is {len(all_land)}")

        # all directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # now do dfs and keep removing from this
        count = 0
        while all_land:
            print(f"count is currently {count} and remaining all_land is {all_land} with number {len(all_land)}")
            frontier = [list(all_land)[0]]  # start somewhere
            while frontier:
                curr_i, curr_j = frontier.pop()
                print(f"curr_i, curr_j is ({curr_i}, {curr_j}) and inside all_land? : {(curr_i, curr_j) in all_land}")
                if (curr_i, curr_j) in all_land:
                    all_land.remove((curr_i, curr_j))

                for direction in directions:
                    del_x, del_y = direction
                    new_i, new_j = curr_i + del_x, curr_j + del_y
                    if self.isValid(new_i, new_j, ROWS, COLS) and (
                            (new_i, new_j) in all_land):  # since we would have already seen it
                        frontier.append((new_i, new_j))
            count += 1

        return count

