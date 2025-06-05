'''
A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h))  are called minimum height trees (MHTs).

Return a list of all MHTs' root labels. You can return the answer in any order.

The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.



Example 1:


Input: n = 4, edges = [[1,0],[1,2],[1,3]]
Output: [1]
Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.
Example 2:


Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
Output: [3,4]


Constraints:

1 <= n <= 2 * 104
edges.length == n - 1
0 <= ai, bi < n
ai != bi
All the pairs (ai, bi) are distinct.
The given input is guaranteed to be a tree and there will be no repeated edges.
'''
from collections import defaultdict
from typing import List


class Solution:
    '''
    Find centroids:

    1. from 0 find the furthest node
    2. from that furthest node find the other furthest node
    3. find the path from furthest node1 -> furthest node2 to get the diameter path
    4. centroids of this path is the answer

    '''
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # adj matrix
        graph = defaultdict(list)
        for i, j in edges:
            graph[i].append(j)
            graph[j].append(i)

        def dfs(src, step, visited, end, dist_to_end):
            visited.add(src)

            for neigh in graph[src]:
                if neigh not in visited:
                    if step + 1 >= dist_to_end:
                        dist_to_end = step + 1
                        end = neigh

                    # updated
                    end, dist_to_end = dfs(neigh, step + 1, visited, end, dist_to_end)

            return end, dist_to_end

        # start dfs from 0 and go to the node furthest away
        end1, _ = dfs(0, 0, set(), 0, 0)

        # from furthest away node find other end ( keep track of that path in memory)
        end2, diameter = dfs(end1, 0, set(), end1, 0)

        def find_path(src, dest, path, visited):
            visited.add(src)

            if src == dest:
                return path, True

            for neigh in graph[src]:
                if neigh not in visited:
                    path.append(neigh)
                    path, found = find_path(neigh, dest, path, visited)

                    if found:
                        return path, True
                    else:
                        path.pop()

            return path, False

        path, _ = find_path(end1, end2, [end1], set())

        if len(path) % 2 == 1:
            return [path[len(path) // 2]]
        else:
            return [path[len(path) // 2], path[len(path) // 2 - 1]]


if __name__ == '__main__':
    s = Solution()

    n = 11
    edges = [[0, 1], [0, 2], [2, 3], [0, 4], [2, 5], [5, 6], [3, 7], [6, 8], [8, 9], [9, 10]]
    expected = [5, 6]
    ans = s.findMinHeightTrees(n, edges)
    assert set(expected) == set(ans), f"{expected = } | {ans = }"

    n = 6
    edges = [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]
    expected = [3, 4]
    ans = s.findMinHeightTrees(n, edges)
    assert set(expected) == set(ans), f"{expected = } | {ans = }"

    n = 4
    edges = [[1, 0], [1, 2], [1, 3]]
    expected = [1]
    ans = s.findMinHeightTrees(n, edges)
    assert set(expected) == set(ans), f"{expected = } | {ans = }"

    n = 10
    edges = [[0, 3], [1, 3], [2, 3], [4, 3], [5, 3], [4, 6], [4, 7], [5, 8], [5, 9]]
    expected = [3]
    ans = s.findMinHeightTrees(n, edges)
    assert set(expected) == set(ans), f"{expected = } | {ans = }"
