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


if __name__ == '__main__':
    deps = [
        [3, 1],
        [8, 1],
        [8, 7],
        [5, 7],
        [5, 2],
        [1, 4],
        [1, 6],
        [1, 2],
        [7, 6]
    ]
    jobs = [1, 2, 3, 4, 5, 6, 7, 8]
    print(topologicalSort(jobs, deps))
