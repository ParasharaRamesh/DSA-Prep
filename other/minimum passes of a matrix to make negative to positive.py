'''
Given a matrix of possibly unequal width and height, how many passes of the matrix is required to make all the negative numbers into positive numbers?
In one pass you can convert a negative number -> positive only iff it's neighbours has atleast one positive value.

So there might be a few passes where some of the negative numbers can become positive only after other negative numbers have flipped therefore we need to determine that number!

'''


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Position) and (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def isValid(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        isXValid = (0 <= self.x) and (self.x < n)
        isYValid = (0 <= self.y) and (self.y < m)
        return isXValid and isYValid

class Item:
    def __init__(self, position, val):
        self.position = position
        self.val = val

    def __eq__(self, other):
        return isinstance(other, Item) and (self.position == other.position) and (self.val == other.val)

    def __hash__(self):
        return hash((self.position, self.val))


def getAllItems(matrix):
    positiveItems = []
    negativeItems = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            val = matrix[i][j]
            position = Position(i, j)
            item = Item(position, val)
            if val > 0:
                positiveItems.append(item)
            elif val < 0:
                negativeItems.append(item)
    return positiveItems, negativeItems


def getNegativeNeighbours(matrix, item):
    position = item.position
    neighbourPositions = [
        Position(position.x - 1, position.y),
        Position(position.x + 1, position.y),
        Position(position.x, position.y - 1),
        Position(position.x, position.y + 1)
    ]

    validPositions = list(filter(lambda position: position.isValid(matrix), neighbourPositions))
    neigbours = list(map(lambda position: Item(position, matrix[position.x][position.y]), validPositions))
    negativeNeighbours = list(filter(lambda neighbour: neighbour.val < 0, neigbours))
    return set(negativeNeighbours)


def minimumPassesOfMatrix(matrix):
    passes = 0

    positiveItems, negativeItems = getAllItems(matrix)
    itemsToBeChanged = set()

    while negativeItems:
        wereThereAnyPositiveItems = len(positiveItems) > 0
        while positiveItems:
            positiveItem = positiveItems.pop()
            negativeNeighbours = getNegativeNeighbours(matrix, positiveItem)
            if len(negativeNeighbours) > 0:
                itemsToBeChanged = itemsToBeChanged.union(negativeNeighbours)

        # increment passes
        if wereThereAnyPositiveItems:
            passes += 1
        else:
            return -1

        # now changeEach of the items to be changed in the original matrix and
        for itemToChange in itemsToBeChanged:
            # change matrix item
            matrix[itemToChange.position.x][itemToChange.position.y] *= -1

            # remove from negativeItems list
            if itemToChange in negativeItems:
                negativeItems.remove(itemToChange)

        # change positiveItems -> itemsToBeChanged and reinit itemsToBeChanged
        positiveItems = list(itemsToBeChanged)
        itemsToBeChanged = set()

    return passes


if __name__ == '__main__':
    # should be 3
    matrix = [
        [0, -1, -3, 2, 0],
        [1, -2, -5, -1, -3],
        [3, 0, 0, -4, -1]
    ]
    print(minimumPassesOfMatrix(matrix))
