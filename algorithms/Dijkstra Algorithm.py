from heapq import *

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
