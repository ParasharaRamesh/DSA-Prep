from collections import deque, defaultdict
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # process graph
        m = len(grid)
        n = len(grid[0])

        frontier = deque([])
        fresh = set()

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh.add((i, j))
                elif grid[i][j] == 2:
                    frontier.append((i, j, 0))

        #print(f"fresh : {fresh}")
        #print(f"frontier init: {frontier}")
        #print("-" * 40)
        #print()

        # start from rotten in the frontier
        total = 0
        visited = dict()

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # do bfs, and visit all oranges
        while frontier:
            #print(f"frontier is : {frontier}")
            i, j, time = frontier.popleft()

            #print(f"({i}, {j}) @ time {time}, total was {total}, fresh: {fresh}, visited: {visited}")

            if (i, j) in visited:
                visited[(i, j)] = min(visited[(i, j)], time)
            else:
                visited[(i, j)] = time

            fresh.discard((i, j))  # remove it if it was there and was fresh
            #print(f"TOTAL: {total}, visited: {visited}, fresh: {fresh}")

            for direction in directions:
                dx, dy = direction
                ni, nj = i + dx, j + dy

                if (0 <= ni < m) and (0 <= nj <= n) and (ni, nj) in fresh:
                    if (ni, nj) not in visited:
                        #print(f"added {(ni, nj)} @ time {time + 1} to frontier")
                        frontier.append((ni, nj, time + 1))
                    elif visited[(ni, nj)] > time + 1:
                        frontier.append((ni, nj, time + 1))

            #print("-" * 40)
            #print()

        if len(fresh) > 0:
            #print(f"fresh fruit was remaining")
            return -1

        return max(visited.values()) if len(visited) > 0 else 0


if __name__ == '__main__':
    # grid = [[2,1,1],[1,1,0],[0,1,1]] #4
    grid = [[2,1,1],[0,1,1],[1,0,1]] #-1
    # grid = [[0,2]] #0
    sol = Solution()
    print(sol.orangesRotting(grid))
