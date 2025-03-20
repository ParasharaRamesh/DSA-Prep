'''
Leetcode 3108:

There is an undirected weighted graph with n vertices labeled from 0 to n - 1.

You are given the integer n and an array edges, where edges[i] = [ui, vi, wi] indicates that there is an edge between vertices ui and vi with a weight of wi.

A walk on a graph is a sequence of vertices and edges. The walk starts and ends with a vertex, and each edge connects the vertex that comes before it and the vertex that comes after it. It's important to note that a walk may visit the same edge or vertex more than once.

The cost of a walk starting at node u and ending at node v is defined as the bitwise AND of the weights of the edges traversed during the walk. In other words, if the sequence of edge weights encountered during the walk is w0, w1, w2, ..., wk, then the cost is calculated as w0 & w1 & w2 & ... & wk, where & denotes the bitwise AND operator.

You are also given a 2D array query, where query[i] = [si, ti]. For each query, you need to find the minimum cost of the walk starting at vertex si and ending at vertex ti. If there exists no such walk, the answer is -1.

Return the array answer, where answer[i] denotes the minimum cost of a walk for query i.


Insight:
> do union find and keep track of components ( do union find by rank for making it faster)
> for each component find all the edges and take the bitwise and of everything and cache the cost
> return the cost for that component

'''
from collections import defaultdict
from typing import List


class Solution:
    def find(self, node):
        curr = node
        while self.parents[curr] != curr:
            curr = self.parents[curr]
        return curr

    def union(self, node1, node2):
        parent1 = self.find(node1)
        parent2 = self.find(node2)
        rank1 = self.rank[parent1]
        rank2 = self.rank[parent2]

        if parent1 != parent2:
            if rank1 == rank2:
                # if ranks are equal then anyone can become child and the parent's rank is increased by one
                self.parents[parent2] = parent1
                self.rank[parent1] += 1
            elif rank1 > rank2:
                # whichever rank is lower that becomes the child and rank doesnt change
                self.parents[parent2] = parent1
            else:
                # whichever rank is lower that becomes the child and rank doesnt change
                self.parents[parent1] = parent2

    def create_graph_with_connected_components(self, n, edges):
        self.graph = {i: [] for i in range(n)}
        self.components = defaultdict(list)

        for edge in edges:
            u, v, w = edge
            self.union(u, v)
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))

        for node in range(n):
            parent = self.find(node)
            self.components[parent].append(node)

    def find_component_cost(self, root):
        if root in self.cost_cache:
            return self.cost_cache[root]

        cost = None
        for node in self.components[root]:
            edges = self.graph[node]
            weights = list(map(lambda item: item[1], edges))

            if weights:
                weights = list(set(weights))
                if cost == None:
                    cost = weights[0]
                    weights = weights[1:]

                for weight in weights:
                    cost &= weight

        self.cost_cache[root] = cost
        return cost

    def minimumCost(self, n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
        self.parents = [i for i in range(n)]  # for union find
        self.rank = [0] * n
        self.cost_cache = dict()

        self.create_graph_with_connected_components(n, edges)

        res = []
        for u, v in query:
            parent_u = self.find(u)
            parent_v = self.find(v)
            if parent_u != parent_v:
                res.append(-1)
            else:
                res.append(self.find_component_cost(parent_u))

        return res


if __name__ == '__main__':
    s = Solution()

    n = 5
    edges = [[0, 1, 7], [1, 3, 7], [1, 2, 1]]
    query = [[0, 3], [3, 4]]

    assert (s.minimumCost(n, edges, query) == [1, -1])

    n = 4
    edges = [[3,2,3],[1,2,3],[3,1,5],[1,2,5],[0,1,2],[1,0,4],[3,2,4]]
    query = [[0,3],[3,0],[1,3],[0,3],[3,2],[3,1],[1,0]]

    assert (s.minimumCost(n, edges, query) == [0, 0, 0, 0, 0, 0, 0])


    n = 5
    edges = [[3, 1, 8], [4, 3, 7], [3, 2, 14], [1, 2, 13], [3, 2, 6], [3, 2, 4], [3, 0, 1], [3, 1, 12]]
    query = [[0, 4], [2, 1], [0, 3], [3, 2], [2, 4], [4, 1], [3, 2]]

    assert (s.minimumCost(n, edges, query) == [0, 0, 0, 0, 0, 0, 0])

    n = 3
    edges = [[0, 2, 7], [0, 1, 15], [1, 2, 6], [1, 2, 1]]
    query = [[1, 2]]

    assert (s.minimumCost(n, edges, query) == [0])
