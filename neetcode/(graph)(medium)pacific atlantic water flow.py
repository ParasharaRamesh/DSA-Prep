'''
You are given a rectangular island heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).

The islands borders the Pacific Ocean from the top and left sides, and borders the Atlantic Ocean from the bottom and right sides.

Water can flow in four directions (up, down, left, or right) from a cell to a neighboring cell with height equal or lower. Water can also flow into the ocean from cells adjacent to the ocean.

Find all cells where water can flow from that cell to both the Pacific and Atlantic oceans. Return it as a 2D list where each element is a list [r, c] representing the row and column of the cell. You may return the answer in any order.

Example 1:



Input: heights = [
  [4,2,7,3,4],
  [7,4,6,4,7],
  [6,3,5,3,6]
]

Output: [[0,2],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0]]
Example 2:

Input: heights = [[1],[1]]

Output: [[0,0],[0,1]]
Constraints:

1 <= heights.length, heights[r].length <= 100
0 <= heights[r][c] <= 1000

'''
from typing import List
from collections import deque


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        M = len(heights)
        N = len(heights[0])

        # get all pacific cells
        pacific = []
        for i in range(M):
            for j in range(N):
                if i == 0 or j == 0:
                    pacific.append((i, j))

        # get all atlantic cells
        atlantic = []
        for i in range(M):
            for j in range(N):
                if i == M - 1 or j == N - 1:
                    atlantic.append((i, j))

        # do dfs from atlantic and pacific side and take intersection
        to_pacific = self.multisouce_bfs(heights, pacific)
        to_atlantic = self.multisouce_bfs(heights, atlantic)
        common = list(to_pacific.intersection(to_atlantic))
        common = [list(index) for index in common]
        return common

    def multisouce_bfs(self, heights, frontier) -> set:
        M = len(heights)
        N = len(heights[0])

        visited = set()
        frontier = deque(frontier)

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        while frontier:
            i, j = frontier.popleft()

            if (i, j) not in visited:
                visited.add((i, j))

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < M and 0 <= nj < N and (ni, nj) not in visited and heights[i][j] <= heights[ni][nj]:
                    frontier.append((ni, nj))

        return visited


if __name__ == '__main__':
    s = Solution()

    heights = [
        [4, 2, 7, 3, 4],
        [7, 4, 6, 4, 7],
        [6, 3, 5, 3, 6]
    ]
    expected = [[0,2],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0]]
    res = s.pacificAtlantic(heights)
    assert expected == res, f"expected: {expected} but was res: {res}"


    heights = [[1],[1]]
    expected = [[0,0],[0,1]]
    res = s.pacificAtlantic(heights)
    assert expected == res, f"expected: {expected} but was res: {res}"
