'''
Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes), write a function to check whether these edges make up a valid tree.

Example 1:

Input:
n = 5
edges = [[0, 1], [0, 2], [0, 3], [1, 4]]

Output:
true
Example 2:

Input:
n = 5
edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]

Output:
false
Note:

You can assume that no duplicate edges will appear in edges. Since all edges are undirected, [0, 1] is the same as [1, 0] and thus will not appear together in edges.
Constraints:

1 <= n <= 100
0 <= edges.length <= n * (n - 1) / 2

'''
from typing import List
from collections import defaultdict


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # basic check for a tree
        if len(edges) != n - 1:
            return False

        # trivial case with one node
        if len(edges) == 0 and n == 1:
            return True

        # check if there is a cycle, if not then it is a valid tree
        def dfs(node, parent, visited):
            if node in visited:
                return True

            visited.add(node)
            for neighbor in graph[node]:
                if neighbor in visited and neighbor != parent:
                    return False

                if neighbor not in visited:
                    res = dfs(neighbor, node, visited)
                    if not res:
                        return False

            return True

        # construct adjacency graph
        graph = defaultdict(list)
        for i, j in edges:
            graph[i].append(j)
            graph[j].append(i)

        # do dfs from somewhere
        visited = set()
        for i in range(n):
            if not dfs(i, None, visited):
                return False
        return True

