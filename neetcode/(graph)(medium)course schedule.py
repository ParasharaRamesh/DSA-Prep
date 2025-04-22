'''
You are given an array prerequisites where prerequisites[i] = [a, b] indicates that you must take course b first if you want to take course a.

The pair [0, 1], indicates that must take course 1 before taking course 0.

There are a total of numCourses courses you are required to take, labeled from 0 to numCourses - 1.

Return true if it is possible to finish all courses, otherwise return false.

Example 1:

Input: numCourses = 2, prerequisites = [[0,1]]

Output: true
Explanation: First take course 1 (no prerequisites) and then take course 0.

Example 2:

Input: numCourses = 2, prerequisites = [[0,1],[1,0]]

Output: false
Explanation: In order to take course 1 you must take course 0, and to take course 0 you must take course 1. So it is impossible.

Constraints:

1 <= numCourses <= 1000
0 <= prerequisites.length <= 1000
All prerequisite pairs are unique.
'''
from typing import List


class Solution:
    # if there is a cycle then cant finish
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        all_courses = set([i for item in prerequisites for i in item])

        graph = {i: set() for i in all_courses}
        for j, i in prerequisites:
            graph[i].add(j)

        in_stack = {course: False for course in all_courses}
        visited = set()

        def dfs(i):
            nonlocal in_stack, visited

            if i in visited:
                return True

            visited.add(i)
            in_stack[i] = True

            for j in graph[i]:
                if in_stack[j]:
                    return False

                if j not in visited:
                    res = dfs(j)

                    if not res:
                        return False

            in_stack[i] = False
            return True

        for i in all_courses:
            if not dfs(i):
                return False

        return True

    # if it is topolocial sortable then can finish
    def canFinish_topological_sort(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        all_courses = set([i for item in prerequisites for i in item])
        total_courses = len(all_courses)

        graph = {i: set() for i in all_courses}
        for j, i in prerequisites:
            graph[i].add(j)

        topo_order = []

        # do topological sorting
        while len(topo_order) < total_courses:
            # find nodes with zero indegree
            reverse_graph = {}

            for i in graph:
                if i not in reverse_graph:
                    reverse_graph[i] = set()

                neighbours = graph[i]
                for neighbour in neighbours:
                    if neighbour not in reverse_graph:
                        reverse_graph[neighbour] = set([i])
                    else:
                        reverse_graph[neighbour].add(i)

            zero_node = None
            for i in reverse_graph:
                if len(reverse_graph[i]) == 0:
                    zero_node = i
                    break

            if zero_node == None:
                return False

            # remove that node from the graph
            for node in graph:
                if zero_node in graph[node]:
                    graph[node].remove(zero_node)
            del graph[zero_node]

            # add to topo_order
            topo_order.append(zero_node)

        return True


if __name__ == '__main__':
    s = Solution()

    numCourses = 2
    prerequisites = [[0, 1], [1, 0]]
    res = s.canFinish(numCourses, prerequisites)
    assert not res, f"expected False but got {res}"

    numCourses = 2
    prerequisites = [[0, 1]]
    res = s.canFinish(numCourses, prerequisites)
    assert res, f"expected True but got {res}"

    numCourses = 20
    prerequisites = [[0, 10], [3, 18], [5, 5], [6, 11], [11, 14], [13, 1], [15, 1], [17, 4]]
    res = s.canFinish(numCourses, prerequisites)
    assert not res, f"expected False but got {res}"




