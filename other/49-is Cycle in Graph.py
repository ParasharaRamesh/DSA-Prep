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

def cycleInUndirectedGraph(edges):
    #init disjoint set with each node as its own set
    disjointNodeSet = UnionFind()
    for i in range(len(edges)):
        disjointNodeSet.createSet(i)

    #go through each edge
    for i, edge in enumerate(edges):
        for j in edge:
             if not disjointNodeSet.union(i,j):
                 return True

    return False

#approach 1 using dfs/bfs or use topological sort
def cycleInGraph(edges):
    visited = set()
    unvisited = set(list(range(len(edges))))
    frontier = [(0,[0])] #item, ancestor at that point

    while unvisited:
        curr = None
        ancestor = []

        if frontier:
            curr, ancestor = frontier.pop()
        else:
            #remove whatever was visited
            unvisited = unvisited - visited

            if unvisited:
                #if any is left pop it and use that!
                curr = unvisited.pop()
                ancestor = [curr]
            else:
                continue

        visited.add(curr)

        for neighbour in edges[curr]:
            if neighbour in ancestor:
                return True

            if neighbour not in visited:
                frontier.append((neighbour, ancestor + [neighbour]))

    return False

if __name__ == '__main__':
    edges = [
        [],
        [0, 3],
        [0],
        [1, 2]
    ]
    #
    # edges = [
    #       [1],
    #       [2, 3, 4, 5, 6, 7],
    #       [],
    #       [2, 7],
    #       [5],
    #       [],
    #       [4],
    #       []
    # ]
    print(cycleInGraph(edges))