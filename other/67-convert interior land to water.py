'''
land is 1s and water is 0s

island is one which is not connected to land on the border... ( first/last row /column)

remove all islands and replace them with a 0
'''
def getNeighbours(matrix, pos, visited):
    x = pos[0]
    y = pos[1]
    m = len(matrix)
    n = len(matrix[0])

    possibleNeighbours = [
        (x,y-1),
        (x,y+1),
        (x-1,y),
        (x+1,y)
    ]
    neighbours = []
    for newX, newY in possibleNeighbours:
        newPos = (newX, newY)
        if 0 <= newX < m and 0 <= newY < n and matrix[newX][newY] == 1 and newPos not in visited:
            neighbours.append(newPos)

    return neighbours

def dfs(matrix, pos):
    visited = set()
    q = [pos]
    while q:
        toVisit = q.pop()
        visited.add(toVisit)
        neighbours = getNeighbours(matrix, toVisit, visited)
        q.extend(neighbours)
    return visited

def visitLandOnEdge(matrix, pos, landOnEdge):
    traversed = dfs(matrix, pos)
    landOnEdge = landOnEdge.union(traversed)
    return landOnEdge

def traverseUnseenInteriorIslands(matrix, pos, seenIslands):
    traversed = dfs(matrix, pos)
    seenIslands = seenIslands.union(traversed)
    return seenIslands

def removeIslands(matrix):
    # init
    landsOnEdge = set()
    seenIslands = set()
    m = len(matrix)
    n = len(matrix[0])

    # find land connected with edges first
    # do the edge rows
    landsOnEdge = traverseLandOnEdgeRows(landsOnEdge, matrix, m, n)

    # do the edge columns
    landsOnEdge = traverseLandOnEdgeColumns(landsOnEdge, matrix, m, n)

    # have a cache of the seen island's position and traverse interior points
    for i in range(1, m):
        for j in range(1, n):
            pos = (i, j)
            if matrix[i][j] == 1 and pos not in landsOnEdge and pos not in seenIslands:
                seenIslands = traverseUnseenInteriorIslands(matrix, pos, seenIslands)

    # from all the seen islands convert it to water
    for seenPos in seenIslands:
        matrix[seenPos[0]][seenPos[1]] = 0

    return matrix

def traverseLandOnEdgeRows(landOnEdge, matrix, m, n):
    for i in [0, m - 1]:
        for x in range(n):
            pos = (i, x)
            if matrix[pos[0]][pos[1]] == 1 and pos not in landOnEdge:
                landOnEdge = visitLandOnEdge(matrix, pos, landOnEdge)
    return landOnEdge

def traverseLandOnEdgeColumns(landOnEdge, matrix, m, n):
    for x in range(m):
        for i in [0, n - 1]:
            pos = (x, i)
            if matrix[pos[0]][pos[1]] == 1 and pos not in landOnEdge:
                landOnEdge = visitLandOnEdge(matrix, pos, landOnEdge)
    return landOnEdge

if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 1]
    ]

    print(removeIslands(matrix))
