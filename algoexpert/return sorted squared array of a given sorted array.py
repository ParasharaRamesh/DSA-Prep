from bisect import *

#better approach O(n) time and space
def sortedSquaredArray(array):
    start = 0
    end = len(array) - 1
    res = []
    while start != end:
        if abs(array[start]) >= abs(array[end]):
            res.append(array[start] ** 2)
            start += 1
        else:
            res.append(array[end] ** 2)
            end -= 1

    # add the last one left!
    res.append(array[start] ** 2)

    # reverse the list
    return res[::-1]


# approach 1, O(n + nlogn)
def sortedSquaredArray1(array):
    i = 0
    negSquares = []
    while i < len(array) and array[i] < 0:
        negSquares.append(array[i] ** 2)
        i += 1

    # took care of positives seperately
    posSquares = list(map(lambda x: x ** 2, array[i:]))

    # for each negative square insert it using binary search/bisection algorithm
    for ns in negSquares:
        insort(posSquares, ns)

    return posSquares
