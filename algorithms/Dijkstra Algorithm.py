import heapq
from heapq import *
from typing import List, Dict


# my solution ( uses a pq of all edges, after adding all of the edges of the first source element)
def dijkstrasAlgorithm(start, edges):
    # init
    distances = [float("inf") for i in range(len(edges))]
    distances[start] = 0
    unvisited = set(list(range(len(edges))))
    visited = set()
    edgeQ = []

    # put the edges of start node in this edgeQ and heapify it!
    for neighbour, weight in edges[start]:
        edgeQ.append((weight, start, neighbour))
        #closest neighbour's initial value
        distances[neighbour] = weight
    heapify(edgeQ)

    # could have as well started with (0, source, source) and not added the first edges to reduce the no of lines of this code!

    visited.add(start)
    while unvisited:
        if edgeQ:
            w, i, j = heappop(edgeQ)
            if j not in visited:
                visited.add(j)
                #add fringe stuff
                for neighbour, weight in edges[j]:
                    heappush(edgeQ, (weight, j, neighbour))
                    bestEstimateDistanceToNeighbourFromJ = distances[j] + weight
                    if bestEstimateDistanceToNeighbourFromJ < distances[neighbour]:
                        distances[neighbour] = bestEstimateDistanceToNeighbourFromJ
        else:
            unvisited -= visited
            for leftOutNode in unvisited:
                #to ensure they arent connected!
                distances[leftOutNode] = -1
            #flush it out
            unvisited.clear()
    return distances


# neetcode solution ( just uses the (distance to vertex, vertex) and a seen set, if something is already seen just skip, and for the fringe neighbours just add it in the ones not seen else skip/ continue. This way we always pick the smallest
class Solution:
    # Implementation for Dijkstra's shortest path algorithm
    def shortestPath(self, n: int, edges: List[List[int]], src: int) -> Dict[int, int]:
        adj = {}
        for i in range(n):
            adj[i] = []

        # s = src, d = dst, w = weight
        for s, d, w in edges:
            adj[s].append([d, w])

        # Compute shortest paths
        shortest = {}
        minHeap = [[0, src]]
        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            if n1 in shortest:
                continue
            shortest[n1] = w1

            for n2, w2 in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap, [w1 + w2, n2])

        # Fill in missing nodes
        for i in range(n):
            if i not in shortest:
                shortest[i] = -1

        return shortest

if __name__ == '__main__':
    start = 0
    edges = [
        [
            [1, 7]
        ],
        [
            [2, 6],
            [3, 20],
            [4, 3]
        ],
        [
            [3, 14]
        ],
        [
            [4, 2]
        ],
        [],
        []
    ]
    print(dijkstrasAlgorithm(start, edges))
