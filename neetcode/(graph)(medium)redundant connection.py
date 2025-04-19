'''
You are given a connected undirected graph with n nodes labeled from 1 to n. Initially, it contained no cycles and consisted of n-1 edges.

We have now added one additional edge to the graph. The edge has two different vertices chosen from 1 to n, and was not an edge that previously existed in the graph.

The graph is represented as an array edges of length n where edges[i] = [ai, bi] represents an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the graph is still a connected non-cyclical graph. If there are multiple answers, return the edge that appears last in the input edges.

Example 1:



Input: edges = [[1,2],[1,3],[3,4],[2,4]]

Output: [2,4]
Example 2:



Input: edges = [[1,2],[1,3],[1,4],[3,4],[4,5]]

Output: [3,4]
Constraints:

n == edges.length
3 <= n <= 100
1 <= edges[i][0] < edges[i][1] <= edges.length
There are no repeated edges and no self-loops in the input.

'''
from typing import List


class Solution:
    def union(self, i, j):
        # 1 indexed -> 0 indexed
        i -= 1
        j -= 1

        parent_i = self.find(i)
        parent_j = self.find(j)

        if parent_i == parent_j:
            # part of same connected component
            return False

        self.parent[parent_j] = parent_i
        return True

    def find(self, k):
        curr = k

        while self.parent[curr] != curr:
            curr = self.parent[curr]

        return curr

    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        self.parent = list(range(len(edges)))  # 0 indexed

        for edge in edges:
            i, j = edge

            if not self.union(i, j):
                return edge

