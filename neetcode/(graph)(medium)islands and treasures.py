'''
You are given a
m
×
n
m×n 2D grid initialized with these three possible values:

-1 - A water cell that can not be traversed.
0 - A treasure chest.
INF - A land cell that can be traversed. We use the integer 2^31 - 1 = 2147483647 to represent INF.
Fill each land cell with the distance to its nearest treasure chest. If a land cell cannot reach a treasure chest than the value should remain INF.

Assume the grid can only be traversed up, down, left, or right.

Modify the grid in-place.

Example 1:

Input: [
  [2147483647,-1,0,2147483647],
  [2147483647,2147483647,2147483647,-1],
  [2147483647,-1,2147483647,-1],
  [0,-1,2147483647,2147483647]
]

Output: [
  [3,-1,0,1],
  [2,2,1,-1],
  [1,-1,2,-1],
  [0,-1,3,4]
]
Example 2:

Input: [
  [0,-1],
  [2147483647,2147483647]
]

Output: [
  [0,-1],
  [1,2]
]
Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 100
grid[i][j] is one of {-1, 0, 2147483647}


'''
from typing import List
from collections import deque


class Solution:
    # def wallsAndGates(self, grid: List[List[int]]) -> None: # Leetcode function
    def islandsAndTreasure(self, grid: List[List[int]]) -> None: # neetcode function
        # magic constants
        empty = (1 << 31) - 1
        wall = -1
        gate = 0
        M = len(grid)
        N = len(grid[0])
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        # helper function
        is_inbounds = lambda i, j: 0 <= i < M and 0 <= j < N

        # find the indices of all the gates
        frontier = deque()
        for i in range(M):
            for j in range(N):
                if grid[i][j] == gate:
                    frontier.append((i, j, 0))

        # multisource bfs
        while frontier:
            i, j, step = frontier.popleft()

            # all base cases
            if not is_inbounds(i, j):
                continue

            if grid[i][j] == wall:
                continue

            if grid[i][j] == gate:
                for di, dj in directions:
                    ni, nj = i + di, j + dj

                    if (
                            (0 <= ni < M and 0 <= nj < N) and
                            (grid[ni][nj] != gate) and
                            (grid[ni][nj] != wall) and
                            (step + 1 <= grid[ni][nj])
                    ):
                        frontier.append((ni, nj, step + 1))

                continue

            # update only if the current step is the lowest for that cell
            if step <= grid[i][j]:
                grid[i][j] = step

                for di, dj in directions:
                    ni, nj = i + di, j + dj

                    if (
                            (0 <= ni < M and 0 <= nj < N) and
                            (grid[ni][nj] != gate) and
                            (grid[ni][nj] != wall) and
                            (step + 1 <= grid[ni][nj])
                    ):
                        frontier.append((ni, nj, step + 1))

        # return


if __name__ == '__main__':
    s = Solution()

    # 0
    rooms = [
        [2147483647, 2147483647, 2147483647],
        [2147483647, -1, 2147483647],
        [0, 2147483647, 2147483647]
    ]
    expected = [
        [2, 3, 4],
        [1, -1, 3],
        [0, 1, 2]
    ]
    s.islandsAndTreasure(rooms)
    assert rooms == expected, f"res was {rooms}, expected {expected}"

    # 1
    rooms = [[-1]]
    expected = [[-1]]
    s.islandsAndTreasure(rooms)
    assert rooms == expected, f"res was {rooms}, expected {expected}"

    # 2
    rooms = [
        [2147483647, -1, 0, 2147483647],
        [2147483647, 2147483647, 2147483647, -1],
        [2147483647, -1, 2147483647, -1],
        [0, -1, 2147483647, 2147483647]
    ]
    expected = [
        [3, -1, 0, 1],
        [2, 2, 1, -1],
        [1, -1, 2, -1],
        [0, -1, 3, 4]
    ]
    s.islandsAndTreasure(rooms)
    assert rooms == expected, f"res was {rooms}, expected {expected}"
