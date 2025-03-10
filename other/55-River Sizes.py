'''
Given a matrix where 0's are land and 1's are the water.
 return the list of all river sizes ( i.e. size of connected component) in any order
'''
def riverSizes(matrix):
    sizes = []
    riverLocations = []

    # get all the locations of all the 1s first
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                riverLocations.append((i, j))

    # for each 1 , do a dfs there and count the component size and add it to sizes
    while riverLocations:
        riverLocation = riverLocations[0]

        currConnectedComponent = [riverLocation]
        componentSize = 0

        while currConnectedComponent:
            # for curr node, increase size and remove from the list of all 1s
            currLocation = currConnectedComponent.pop()
            componentSize += 1

            if currLocation in riverLocations:
                riverLocations.remove(currLocation)

            # add in frontier
            neighbours = getNeighbouringRivers(currLocation, matrix, riverLocations, currConnectedComponent)
            currConnectedComponent.extend(neighbours)

        # add size of current connected component
        sizes.append(componentSize)

    return sizes


def isValidPosition(i, j, m, n):
    return 0 <= i < m and 0 <= j < n


def getNeighbouringRivers(riverLocation, matrix, riverLocations, currConnectedComponent):  # ensure its not in frontier
    i, j = riverLocation
    m = len(matrix)
    n = len(matrix[0])
    neighbours = []

    # positions
    left = (i, j - 1)
    up = (i - 1, j)
    right = (i, j + 1)
    down = (i + 1, j)

    # left
    if isValidPosition(left[0], left[1], m, n) \
            and left in riverLocations \
            and left not in currConnectedComponent \
            and matrix[left[0]][left[1]] == 1:
        neighbours.append(left)

    # up
    if isValidPosition(up[0], up[1], m, n) \
            and up in riverLocations \
            and up not in currConnectedComponent \
            and matrix[up[0]][up[1]] == 1:
        neighbours.append(up)

    # right
    if isValidPosition(right[0], right[1], m, n) \
            and right in riverLocations \
            and right not in currConnectedComponent \
            and matrix[right[0]][right[1]] == 1:
        neighbours.append(right)

    # down
    if isValidPosition(down[0], down[1], m, n) \
            and down in riverLocations \
            and down not in currConnectedComponent \
            and matrix[down[0]][down[1]] == 1:
        neighbours.append(down)

    return neighbours


if __name__ == '__main__':
    matrix = [
        [1, 1, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0]
    ]
    # # 1, 2, 2, 2, 5

    # matrix = [
    #     [1, 1, 1],
    #     [1, 1, 1],
    #     [1, 1, 1]
    # ]
    print(riverSizes(matrix))
