'''
All ways to detect cycles:

* inefficient way is to keep track of the ancestory of nodes travelled as a path list for each node
1. Undirected graphs:
    a. Union Find:
        - Use union find and as we are doing union, if they belong to the same component already then that means that there is a cycle
    b. Use DFS (recursion)(parent tracking)
        - for every node also pass the parent and keep track of the visited set as well
        - if a neighbour node is not visited, then explore it
        - if a neighbour node is already visited, check if the neighbour node is not the parent , then it is definitely an ancestor
    c. BFS/DFS with explicit q/stack
        - just have extra memory space for all the nodes and keep track of whether it is in the stack at any point of time or not

2. Directed graphs:
    a. topological sort
        - if it is topologically sortable then it has no cycles
    b. BFS/DFS with explicit q/stack
        - just have extra memory space for all the nodes and keep track of whether it is in the stack at any point of time or not
    c. Linked list:
        - tortoise hare algorithm
'''


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


def has_cycle_undirected(graph, node, parent, visited):
    visited[node] = True

    for neighbor in graph[node]:
        if not visited[neighbor]:  # DFS traversal
            if has_cycle_undirected(graph, neighbor, node, visited):
                return True
        elif neighbor != parent:  # Found a back edge (cycle)
            return True

    return False


def is_cyclic_undirected(graph, n):
    visited = [False] * n

    for node in range(n):  # Check for disconnected components
        if not visited[node]:
            if has_cycle_undirected(graph, node, -1, visited):
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


def is_cyclic_undirected(graph, n):
    visited = [False] * n

    for start in range(n):  # Handle disconnected components
        if not visited[start]:
            stack = [(start, -1)]  # (node, parent)

            while stack:
                node, parent = stack.pop()

                if visited[node]:
                    continue

                visited[node] = True

                for neighbor in graph[node]:
                    if not visited[neighbor]:  # Visit unvisited neighbors
                        stack.append((neighbor, node))
                    elif neighbor != parent:  # Found a back edge (cycle)
                        return True

    return False


def is_cyclic_directed(graph, n):
    visited = [False] * n
    stack = [False] * n  # Track nodes in the current DFS path
    explicit_stack = []  # Stack for iterative DFS

    for start in range(n):  # Handle disconnected components
        if not visited[start]:
            explicit_stack.append((start, "ENTER"))

            while explicit_stack:
                node, action = explicit_stack.pop()

                if action == "EXIT":  # Mark node as exited
                    stack[node] = False
                    continue

                if visited[node]:  # Already visited, skip
                    continue

                # Mark as visited and in recursion stack
                visited[node] = True
                stack[node] = True
                explicit_stack.append((node, "EXIT"))  # Add exit phase

                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        explicit_stack.append((neighbor, "ENTER"))
                    elif stack[neighbor]:  # Found a back edge (cycle)
                        return True

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