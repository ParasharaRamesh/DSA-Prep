'''
You are given a 2-D integer array points, where points[i] = [xi, yi]. Each points[i] represents a distinct point on a 2-D plane.

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between the two points, i.e. |xi - xj| + |yi - yj|.

Return the minimum cost to connect all points together, such that there exists exactly one path between each pair of points.

Example 1:



Input: points = [[0,0],[2,2],[3,3],[2,4],[4,2]]

Output: 10
Constraints:

1 <= points.length <= 1000
-1000 <= xi, yi <= 1000
'''
from typing import List
from collections import defaultdict
from heapq import *

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # construct graph
        graph = defaultdict(list)
        manhattan_distance = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                point1 = points[i]
                point2 = points[j]
                distance = manhattan_distance(point1, point2)
                graph[tuple(point1)].append((tuple(point2), distance))
                graph[tuple(point2)].append((tuple(point1), distance))

        # construct min spanning tree and calculate cost
        src = tuple(points[0])
        visited = {src}
        frontier = [(d, src, j) for j, d in graph[src]]
        heapify(frontier)

        cost = 0
        # mst = []
        while frontier:
            d_ij, i, j = heappop(frontier)

            if j not in visited:
                visited.add(j)
                # mst.append((d_ij, i, j))
                cost += d_ij

                for k, d_kj in graph[j]:
                    if k not in visited:
                        heappush(frontier, (d_kj, j, k))

        return cost

if __name__ == '__main__':
    s = Solution()
    points = [[0, 0], [2, 2], [3, 3], [2, 4], [4, 2]]
    print(s.minCostConnectPoints(points))#10
