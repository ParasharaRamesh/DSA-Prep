'''
You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the bottom-right cell.



Example 1:



Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
Example 2:



Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
Example 3:


Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
Explanation: This route does not require any effort.


Constraints:

rows == heights.length
columns == heights[i].length
1 <= rows, columns <= 100
1 <= heights[i][j] <= 106
'''
from typing import List
from heapq import *


class Solution:
    # recursion depth exceeded :(
    def minimumEffortPath_dfs_recur_exceeded(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        min_effort = float("inf")
        visited = set()

        def dfs(i, j, effort):
            nonlocal min_effort, visited

            if not (0 <= i < m and 0 <= j < n) or (i, j) in visited:
                return float("inf")

            if i == m - 1 and j == n - 1:
                return effort

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < m and 0 <= nj < n) and (ni, nj) not in visited:
                    visited.add((i, j))

                    step_effort = abs(heights[i][j] - heights[ni][nj])
                    max_step_effort = max(effort, step_effort)

                    path_effort = dfs(ni, nj, max_step_effort)

                    min_effort = min(min_effort, path_effort)

                    visited.discard((i, j))

            return min_effort

        return dfs(0, 0, 0)

    # classic dfs (TLE) :(
    def minimumEffortPath_dfs_tle(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        min_effort = float("inf")

        frontier = [(0, 0, 0, set())]

        while frontier:
            i, j, effort, visited = frontier.pop()

            if not (0 <= i < m and 0 <= j < n) or (i, j) in visited:
                continue

            if i == m - 1 and j == n - 1:
                min_effort = min(min_effort, effort)
                continue

            visited.add((i, j))

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < m and 0 <= nj < n) and (ni, nj) not in visited:
                    step_effort = abs(heights[i][j] - heights[ni][nj])
                    max_step_effort = max(effort, step_effort)
                    frontier.append((ni, nj, max_step_effort, visited.copy()))

        return min_effort

    # dijktra (works! :))
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m = len(heights)
        n = len(heights[0])

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        visited = set()

        frontier = [(0, 0, 0)]

        while frontier:
            effort, i, j = heappop(frontier)

            if not (0 <= i < m and 0 <= j < n) or (i, j) in visited:
                continue

            visited.add((i, j))

            if i == m - 1 and j == n - 1:
                # the moment you pick this everything else is void
                return effort

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < m and 0 <= nj < n) and (ni, nj) not in visited:
                    step_effort = abs(heights[i][j] - heights[ni][nj])
                    max_step_effort = max(effort, step_effort)
                    heappush(frontier, (max_step_effort, ni, nj))

        return 0


if __name__ == '__main__':
    s = Solution()

    heights = [
        [1, 2],
        [3, 1]
    ]
    expected = 1
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [3]
    ]
    expected = 0
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [1, 1, 1],
        [3, 2, 4],
        [2, 5, 4]
    ]
    expected = 2
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [1, 1, 1],
        [1, 1, 2],
        [6, 5, 2]
    ]
    expected = 1
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [1, 2, 2],
        [3, 8, 2],
        [5, 3, 5]
    ]
    expected = 2
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [1, 2, 3],
        [3, 8, 4],
        [5, 3, 5]
    ]
    expected = 1
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"

    heights = [
        [1, 2, 1, 1, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 1, 1, 2, 1]
    ]
    expected = 0
    actual = s.minimumEffortPath(heights)
    assert expected == actual, f"{expected = }, {actual = }"
