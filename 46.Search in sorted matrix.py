from bisect import *
from heapq import *

#Approach 1 convert it into linear array and do binary search there!
class Item:
    def __init__(self, item, i=None, j=None):
        self.item = item
        self.i = i
        self.j = j

    def __lt__(self, other):
        return self.item < other.item

    def __str__(self):
        return f"Item(val={self.item}, i={self.i}, j={self.j})"

    def __repr__(self):
        return f"Item(val={self.item}, i={self.i}, j={self.j})"

def searchInSortedMatrix_linearApproach(matrix, target):
    modifiedMatrix = modifyMatrix(matrix)
    linear = getLinearMatrix(modifiedMatrix)
    pos = bisect(linear, Item(target))

    # because bisect returns index to the right of any existing thing
    if pos >= 1 and linear[pos - 1].item == target:
        return [linear[pos - 1].i, linear[pos - 1].j]
    else:
        return [-1, -1]

def getLinearMatrix(matrix):
    merged = []
    # like merge sort
    itr = merge(*matrix)
    while True:
        try:
            merged.append(next(itr))
        except Exception:
            break
    return merged

def modifyMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = Item(matrix[i][j], i, j)
    return matrix

#Approach 2 matrix approach

class MatrixItem:
    def __init__(self, item, i=None, j=None):
        self.item = item
        self.i = i
        self.j = j

    def __str__(self):
        return f"Item(val={self.item}, i={self.i}, j={self.j})"

    def __repr__(self):
        return f"Item(val={self.item}, i={self.i}, j={self.j})"

def modifyAndPreserveOriginalIndices(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = MatrixItem(matrix[i][j], i, j)
    return matrix

def searchInSortedMatrix(matrix, target):
    #in order to prese
    modifiedMatrix = modifyAndPreserveOriginalIndices(matrix)
    return util(modifiedMatrix, target)

def util(modifiedMatrix, target):
    notFound = [-1,-1]

    if not modifiedMatrix or all(list(map(lambda x: len(x) == 0,modifiedMatrix))):
        return notFound

    midI , midJ = len(modifiedMatrix) // 2, len(modifiedMatrix[0]) // 2

    rest1, rest2 = None, None
    matrixItem = modifiedMatrix[midI][midJ]

    if target == matrixItem.item:
        return [matrixItem.i, matrixItem.j]
    elif target > matrixItem.item:
        #exclude the whole uppper left rectangle with that element included and search in the rest
        rest1 = util([row[midJ+1:] for row in modifiedMatrix[:midI+1]], target)
        rest2 = util(modifiedMatrix[midI+1:], target)
    else:
        # exclude the whole bottom right rectangle with that element included and search in the rest
        rest1 = util([row[:midJ] for row in modifiedMatrix[midI:]], target)
        rest2 = util(modifiedMatrix[:midI], target)

    #not found in both
    if rest1 == notFound and rest2 == notFound:
        return notFound

    if rest1 != notFound:
        return rest1

    if rest2 != notFound:
        return rest2

    return notFound


if __name__ == '__main__':
    matrix = [
        [1,     4,     7,       12,     15,     1000],
        [2,     5,     19,      31,     32,     1001],
        [3,     8,     24,      33,     35,     1002],
        [40,    41,    42,      44,     45,     1003],
        [99,    100,   103,     106,    128,    1004]
    ]
    target = 128
    print(searchInSortedMatrix(matrix, target))
