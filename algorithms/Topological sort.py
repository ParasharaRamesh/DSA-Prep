import heapq
from collections import defaultdict, Counter


#old method slow
def getZeroIndegreeNodeAndModifyGraph(indegreeList):
    zeroIndegreeNode = None

    # find 0 degree node
    for node in indegreeList:
        if len(indegreeList[node]) == 0:
            zeroIndegreeNode = node
            break

    if zeroIndegreeNode != None:
        # remove that node from the graph
        del indegreeList[zeroIndegreeNode]

        # for that node remove its connection
        for node in indegreeList:
            if zeroIndegreeNode in indegreeList[node]:
                indegreeList[node].remove(zeroIndegreeNode)

    # return 0 degree and modified indegree list!
    return zeroIndegreeNode, indegreeList


def topologicalSort(jobs, deps):
    # init
    topoSort = []
    containsCycle = False

    indegreeList = dict()
    for job in jobs:
        indegreeList[job] = []

    # construct indegree list
    for i, j in deps:
        indegreeList[j].append(i)

    # keep iterating until there is nothing left
    while jobs:
        zeroIndegreeJob, indegreeList = getZeroIndegreeNodeAndModifyGraph(indegreeList)

        # if no 0 degree node exists, return empty
        if zeroIndegreeJob == None:
            containsCycle = True
            break

        # else add it to the topo sort list
        topoSort.append(zeroIndegreeJob)
        jobs.remove(zeroIndegreeJob)

    # return final topological sorted result
    return topoSort if not containsCycle else []

# uses heapq and a graph and a reverse graph.. but technically heap is not needed at all since we only store the 0 degree nodes
def topological_sort(n, edges):
    # Step 1: Build adjacency list and reverse graph (indegree tracking)
    graph = defaultdict(list)  # Normal adjacency list
    reverse_graph = defaultdict(set)  # Reverse graph using sets for fast removal

    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].add(u)  # Reverse edges (store parents)

    # Step 2: Use a Min-Heap to store nodes with zero indegree ( heap is not needed at all!)
    min_heap = []
    for node in range(n):
        if node not in reverse_graph:  # Nodes with no incoming edges
            heapq.heappush(min_heap, node)

    # Step 3: Process nodes in topological order
    topo_order = []
    while min_heap:
        node = heapq.heappop(min_heap)  # Get smallest zero-indegree node
        topo_order.append(node)

        # Remove this node from the graph
        for neighbor in graph[node]:
            reverse_graph[neighbor].remove(node)  # Remove dependency
            if not reverse_graph[neighbor]:  # If no more parents left
                heapq.heappush(min_heap, neighbor)
                del reverse_graph[neighbor]  # Cleanup to avoid memory issues

        del graph[node]  # Remove processed node completely

    # Step 4: Cycle detection
    if len(topo_order) < n:
        return []  # Cycle detected (not all nodes were processed)

    return topo_order


if __name__ == '__main__':
    # deps = [
    #     [3, 1],
    #     [8, 1],
    #     [8, 7],
    #     [5, 7],
    #     [5, 2],
    #     [1, 4],
    #     [1, 6],
    #     [1, 2],
    #     [7, 6]
    # ]
    # jobs = [1, 2, 3, 4, 5, 6, 7, 8]
    # print(topologicalSort(jobs, deps))


    # Example Usage:
    n = 6
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    print(topological_sort(n, edges))  # Output: [4, 5, 0, 2, 3, 1] (or similar valid order)

    # Example with a cycle:
    edges_with_cycle = [(0, 1), (1, 2), (2, 0)]  # Cycle: 0 → 1 → 2 → 0
    print(topological_sort(3, edges_with_cycle))  # Output: [] (cycle detected)
