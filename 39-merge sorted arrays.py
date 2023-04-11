from heapq import *


def mergeSortedArrays(arrays):
    res = []

    # init heap with starting elements
    # note: in python heap has (priority, item) so always sorts by the priority whereas item can be anything!
    indexHeap = [[arrays[index][0], [index, 0]] for index in range(len(arrays))]
    heapify(indexHeap)

    while indexHeap:
        # get smallest and add to res
        element, indices = heappop(indexHeap)
        arrayIndex, inArrayIndex = indices

        res.append(element)

        if inArrayIndex + 1 < len(arrays[arrayIndex]):
            heapItemToBePushed = [arrays[arrayIndex][inArrayIndex + 1], [arrayIndex, inArrayIndex + 1]]
            heappush(indexHeap, heapItemToBePushed)

    return res


if __name__ == '__main__':
    arrays = [
        [1, 5, 9, 21],
        [-1, 0],
        [-124, 81, 121],
        [3, 6, 12, 20, 150]
    ]

    print(mergeSortedArrays(arrays))
