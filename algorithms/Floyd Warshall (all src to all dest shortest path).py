# Python Program for Floyd Warshall Algorithm

# Solves the all-pairs shortest path
# problem using Floyd Warshall algorithm
def floydWarshall(graph):
    V = len(graph)

    # Add all vertices one by one to
    # the set of intermediate vertices.
    for k in range(V):

        # Pick all vertices as source one by one
        for i in range(V):

            # Pick all vertices as destination
            # for the above picked source
            for j in range(V):

                # If vertex k is on the shortest path from
                # i to j, then update the value of graph[i][j]

                if ((graph[i][j] == -1 or
                     graph[i][j] > (graph[i][k] + graph[k][j]))
                        and (graph[k][j] != -1 and graph[i][k] != -1)):
                    graph[i][j] = graph[i][k] + graph[k][j]


if __name__ == "__main__":
    graph = [
        [0, 4, -1, 5, -1],
        [-1, 0, 1, -1, 6],
        [2, -1, 0, 3, -1],
        [-1, -1, 1, 0, 2],
        [1, -1, -1, 4, 0]
    ]

    floydWarshall(graph)
    for i in range(len(graph)):
        for j in range(len(graph)):
            print(graph[i][j], end=" ")
        print()
