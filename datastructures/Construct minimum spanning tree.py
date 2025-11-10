'''
edges is an adjacency list with len(edges) > no of nodes in the graph
edge[i] -> list of [(j, weight of i-j)...]

return minimum spanning tree

NOTE: This only works on UNDIRECTED GRAPHS!

for directed graph MST there is something called as the Chu Liu Edmonds Maximum Spanning Tree algorithm


'''

from collections import defaultdict
from heapq import *

class UnionFind:
    def __init__(self):
        self.parent = dict()

    def createSet(self, value):
        self.parent[value] = None

    def find(self, value):
        if value not in self.parent:
            return None

        curr = value
        while self.parent[curr] != None:
            curr = self.parent[curr]

        return curr

    def union(self, valueOne, valueTwo):
        parent1 = self.find(valueOne)
        parent2 = self.find(valueTwo)

        if parent1 != parent2:
            # make 2's parent 1
            self.parent[parent2] = parent1
            return True

        # if both parents are already same
        return False

#common helper function
def convertToAdjacencyList(mstList, n):
    minSpanningGraph = defaultdict(list)

    #convert to adjacency list
    for weight, node1, node2 in mstList:
        minSpanningGraph[node1].append([node2, weight])
        minSpanningGraph[node2].append([node1, weight])

    #convert to other type of adjacency list
    edges = [None for i in range(n)]

    for node in minSpanningGraph:
        neighbours = minSpanningGraph[node]
        edges[node] = neighbours

    return edges

#Approach 1
def primsAlgorithm(edges):
    '''
    PRIM's Algorithm (NODE CENTRIC)

    * works only if the entire graph is already connected as a single thing, but can modify it for islands of connected components!
    * start with a single vertex in the MST and have all of its edges in the min heap initially!
    * amongst the edges pick the node with the smallest distance and then add that to the mst if it is not already visited and also add to visited set
    * take its neighbours and add it to the heap of edges ( fringe elements !)
    * better to consider a visited set of nodes instead of edges because that makes it truly greedy and optimal. If it was visited set of edges, then we might have already seen 2 edges and we might add a 3rd unvisited edge into the visited set, even though those 3 edges together forms a cycle. Therefore it is better to keep track of destination nodes as the visisted set.

    :param edges:
    :return:
    '''
    # init
    n = len(edges)
    mstList = []

    # start with the vertex 0
    visited = set()
    visited.add(0)

    # get all the edges connecting to node 0
    edgeQ = []
    for neighbour, weight in edges[0]:
        edgeQ.append((weight, 0, neighbour))
    heapify(edgeQ)

    # until the minheap is exhausted
    while edgeQ:
        # find smallest not in visited
        weight, node1, node2 = heappop(edgeQ)

        # if node2 is not yet visited
        if node2 not in visited:
            # add to visited
            visited.add(node2)

            # add this to MST
            mstList.append((weight, node1, node2))

            # now add its neighbours into the edgeQ
            for neighbour, w in edges[node2]:
                if neighbour not in visited:
                    heappush(edgeQ, (w, node2, neighbour))

    #convert
    return convertToAdjacencyList(mstList, n)

#Approach 2
def kruskalsAlgorithm(edges):
    '''
    EDGE CENTRIC

    * Sort all edges and keep picking the lowest edges until it doesn't form a cycle.
    * if so discard that

    :param edges:
    :return:
    '''
    #result init
    mstList = []
    n = len(edges)

    #get all edges and put it in a min heap (weight, node1, node2) . Dont double count!
    edgeQ = []
    seen = set()
    for i, edge in enumerate(edges):
        for j, w in edge:
            if (j,i) not in seen:
                edgeQ.append((w, i, j))
                seen.add((i,j))
    del seen
    heapify(edgeQ)

    #pick each edge one by one , add it to MST, if it forms a cycle discard it!
    while edgeQ:
        weight, node1, node2 = heappop(edgeQ)

        #try adding to mst
        mstList.append((weight, node1, node2))

        #if it is cyclic remove that recently added edge and proceed forward
        if isCyclic(mstList):
            mstList.pop()

    #convert
    return convertToAdjacencyList(mstList, n)

# given [(w, n1, n2)] determine if cyclic
def isCyclic(edgeList):
    disjointedNodeSet = UnionFind()

    #init disjoint set
    for w, i, j in edgeList:
        if i not in disjointedNodeSet.parent:
            disjointedNodeSet.createSet(i)
        if j not in disjointedNodeSet.parent:
            disjointedNodeSet.createSet(j)

    for w, node1, node2 in edgeList:
        if not disjointedNodeSet.union(node1, node2):
            #not mergable as both have same parent, i.e belong in a cycle!
            return True

    return False


if __name__ == '__main__':
    # connected
    edges = [
        # 0
        [
            [1, 3],
            [2, 5]
        ],
        # 1
        [
            [0, 3],
            [2, 10],
            [3, 12],
            [4, 1]
        ],
        # 2
        [
            [0, 5],
            [1, 10],
            [4, 7]
        ],
        # 3
        [
            [1, 12],
            [4, 11]
        ],
        # 4
        [
            [1, 1],
            [2, 7],
            [3, 11]
        ]
    ]

    #disconnected
    # edges = [
    #   [
    #     [1, 1]
    #   ],
    #   [
    #     [0, 1]
    #   ],
    #   [
    #     [3, 1]
    #   ],
    #   [
    #     [2, 1]
    #   ]
    # ]

    # print(primsAlgorithm(edges))
    print(kruskalsAlgorithm(edges))
