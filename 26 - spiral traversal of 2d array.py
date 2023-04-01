# is it possible to add to visited set
def canAddToVisited(i, j, n, m, visited):
    xCheck = (i >= 0) and (i < n)
    yCheck = (j >= 0) and (j < m)
    isAlreadyVisited = (i, j) in visited

    return xCheck and yCheck and not isAlreadyVisited


# movement checks
def isRightPossible(i, j, n, m, visited):
    return canAddToVisited(i, j + 1, n, m, visited)

def isDownPossible(i, j, n, m, visited):
    return canAddToVisited(i + 1, j, n, m, visited)

def isLeftPossible(i, j, n, m, visited):
    return canAddToVisited(i, j - 1, n, m, visited)

def isUpPossible(i, j, n, m, visited):
    return canAddToVisited(i - 1, j, n, m, visited)


# movement functions
def moveRight(i, j):
    return i, j + 1

def moveDown(i, j):
    return i + 1, j

def moveLeft(i, j):
    return i, j - 1

def moveUp(i, j):
    return i - 1, j

#main
def spiralTraverse(array):
    visited = set()
    spiralList = []

    movementChecks = [isRightPossible, isDownPossible, isLeftPossible, isUpPossible]
    movements = [moveRight, moveDown, moveLeft, moveUp]

    n = len(array)
    m = len(array[0])

    # indices
    i = 0
    j = 0
    movementIndex = 0

    while len(spiralList) != n * m:
        if canAddToVisited(i, j, n, m, visited):
            spiralList.append(array[i][j])
            visited.add((i, j))

        if movementChecks[movementIndex](i, j, n, m, visited):
            i, j = movements[movementIndex](i, j)
        else:
            # cycle through movements only if the current movement fails
            movementIndex = (movementIndex + 1) % len(movements)

    return spiralList


if __name__ == '__main__':
    tests = [
        [
            [1, 2, 3],
            [6, 5, 4]
        ],
        [
            [1, 2, 3, 4],
            [12, 13, 14, 5],
            [11, 16, 15, 6],
            [10, 9, 8, 7]
        ]
    ]

    for test in tests:
        print(spiralTraverse(test))
