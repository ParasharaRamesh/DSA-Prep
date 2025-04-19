'''
Number of Connected Components in an Undirected Graph
There is an undirected graph with n nodes. There is also an edges array, where edges[i] = [a, b] means that there is an edge between node a and node b in the graph.

The nodes are numbered from 0 to n - 1.

Return the total number of connected components in that graph.

Example 1:

Input:
n=3
edges=[[0,1], [0,2]]

Output:
1
Example 2:

Input:
n=6
edges=[[0,1], [1,2], [2,3], [4,5]]

Output:
2
Constraints:

1 <= n <= 100
0 <= edges.length <= n * (n - 1) / 2

'''
from typing import List


class DS:
    def __init__(self, n):
        self.parents = [None] * n
        self.size = [1] * n

    def union(self, x, y):
        parent1 = self.find(x)
        parent2 = self.find(y)

        if parent1 == parent2:
            #forms cycle, so they were already counted in the total count
            return False

        size1 = self.size[x]
        size2 = self.size[y]

        if size1 == size2:
            self.parents[parent2] = parent1
            self.size[parent1] += 1
        elif size1 > size2:
            self.parents[parent2] = parent1
        else:
            self.parents[parent1] = parent2

        # they are being union'd for the first time so need to consider both as part of same component and count it
        return True
    def find(self, x):
        curr = x
        while self.parents[curr] != None:
            curr = self.parents[curr]
        return curr

class Solution:
    def countComponents_union_find_approach1(self, n: int, edges: List[List[int]]) -> int:
        ds = DS(n)

        for x, y in edges:
            ds.union(x, y)

        components = set()
        for node in range(n):
            components.add(ds.find(node))

        return len(components)

    #better approach with union find, assume that there are n components i.e all are distinct and everytime they belong to same component subtract 1
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        ds = DS(n)

        count = n
        for x, y in edges:
            if ds.union(x, y):
                count -=1

        return count

if __name__ == '__main__':
    s = Solution()

    n = 5
    edges = [[0,1],[1,2],[3,4]]
    print(s.countComponents(n, edges))#2

    n = 5
    edges = [[0,1],[1,2],[2,3],[3,4]]
    print(s.countComponents(n, edges))#1