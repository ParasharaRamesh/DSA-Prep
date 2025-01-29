'''
leetcode 743.

You are given a network of n directed nodes, labeled from 1 to n. You are also given times, a list of directed edges where times[i] = (ui, vi, ti).

ui is the source node (an integer from 1 to n)
vi is the target node (an integer from 1 to n)
ti is the time it takes for a signal to travel from the source to the target node (an integer greater than or equal to 0).
You are also given an integer k, representing the node that we will send a signal from.

Return the minimum time it takes for all of the n nodes to receive the signal. If it is impossible for all the nodes to receive the signal, return -1 instead.

'''
from heapq import *
from typing import List

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # build graph
        graph = {i: [] for i in range(1, n + 1)}

        for time in times:
            u, v, t = time
            graph[u].append((t, v))

        best_times = {i: float("inf") for i in range(1, n + 1)}
        frontier = [(0, k, k)]  # time, u, v
        seen_edges = set()

        while frontier:
            # time_to_v_via_u, u, v = frontier.pop()
            time_to_v_via_u, u, v = heappop(frontier)

            v_best_time = best_times[v]
            if time_to_v_via_u <= v_best_time:
                best_times[v] = time_to_v_via_u

            for neighbor in graph[v]:
                time_to_neigh, neigh_node = neighbor
                if (v, neigh_node) not in seen_edges:
                    # frontier.append((time_to_v_via_u + time_to_neigh, v, neigh_node))
                    heappush(frontier,(time_to_v_via_u + time_to_neigh, v, neigh_node))
                    seen_edges.add((v, neigh_node))

        are_all_nodes_visited = all([best_times[node] != float("inf") for node in best_times])

        if not are_all_nodes_visited:
            return -1
        else:
            return max(best_times.values())


if __name__ == '__main__':
    s = Solution()

    times = [[1, 2, 1], [2, 3, 1], [1, 4, 4], [3, 4, 1]]
    n = 4
    k = 1
    print(s.networkDelayTime(times, n, k)) # 3


    times = [[1,2,1],[2,3,1]]
    n = 3
    k = 2
    print(s.networkDelayTime(times, n, k)) # -1

    times = [[1,2,1],[2,1,3]]
    n = 2
    k = 2
    print(s.networkDelayTime(times, n, k)) # 3

    times = [[3, 5, 78], [2, 1, 1], [1, 3, 0], [4, 3, 59], [5, 3, 85], [5, 2, 22], [2, 4, 23], [1, 4, 43], [4, 5, 75],
             [5, 1, 15], [1, 5, 91], [4, 1, 16], [3, 2, 98], [3, 4, 22], [5, 4, 31], [1, 2, 0], [2, 5, 4], [4, 2, 51],
             [3, 1, 36], [2, 3, 59]]
    n = 5
    k = 5
    print(s.networkDelayTime(times, n, k)) #31