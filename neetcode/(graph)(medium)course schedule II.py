'''
You are given an array prerequisites where prerequisites[i] = [a, b] indicates that you must take course b first if you want to take course a.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
There are a total of numCourses courses you are required to take, labeled from 0 to numCourses - 1.

Return a valid ordering of courses you can take to finish all courses. If there are many valid answers, return any of them. If it's not possible to finish all courses, return an empty array.

Example 1:

Input: numCourses = 3, prerequisites = [[1,0]]

Output: [0,1,2]
Explanation: We must ensure that course 0 is taken before course 1.

Example 2:

Input: numCourses = 3, prerequisites = [[0,1],[1,2],[2,0]]

Output: []
Explanation: It's impossible to finish all courses.

Constraints:

1 <= numCourses <= 1000
0 <= prerequisites.length <= 1000
All prerequisite pairs are unique.

'''
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = {i: set() for i in range(numCourses)}
        for j, i in prerequisites:
            graph[i].add(j)

        topo_order = []

        # do topological sorting
        while len(topo_order) < numCourses:
            # find nodes with zero indegree
            reverse_graph = {}

            for i in graph:
                if i not in reverse_graph:
                    reverse_graph[i] = set()

                neighbours = graph[i]
                for neighbour in neighbours:
                    if neighbour not in reverse_graph:
                        reverse_graph[neighbour] = {i}
                    else:
                        reverse_graph[neighbour].add(i)

            zero_node = None
            for i in reverse_graph:
                if len(reverse_graph[i]) == 0:
                    zero_node = i
                    break

            if zero_node == None:
                return []

            # remove that node from the graph
            for node in graph:
                if zero_node in graph[node]:
                    graph[node].remove(zero_node)
            del graph[zero_node]

            # add to topo_order
            topo_order.append(zero_node)

        return topo_order
