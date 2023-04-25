import heapq


class MinHeap:
    def __init__(self, array):
        self.heap = self.buildHeap(array)

    # main functions
    def buildHeap(self, array):
        mid = (len(array) - 2) // 2
        for i in reversed(range(mid + 1)):
            array = self.siftDown(i, array)
        return array

    def peek(self):
        return self.heap[0] if self.heap else None

    def remove(self):
        if self.heap:
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            removedElement = self.heap.pop()
            self.heap = self.siftDown(0, self.heap)
            return removedElement

    def insert(self, value):
        self.heap.append(value)
        self.heap = self.siftUp(len(self.heap) - 1, self.heap)

    # helper functions
    def siftDown(self, index, heap):
        curr = index
        while True:
            childIndex1, childIndex2 = self.getChildren(curr, heap)
            minChildIndex = None
            isChild1Present = childIndex1 != None
            isChild2Present = childIndex2 != None

            if not isChild1Present and not isChild2Present:
                break
            elif isChild1Present and not isChild2Present:
                minChildIndex = childIndex1
            else:
                #both present
                minChildIndex = childIndex1
                if heap[childIndex2] < heap[childIndex1]:
                    minChildIndex = childIndex2

            if heap[curr] > heap[minChildIndex]:
                heap[curr], heap[minChildIndex] = heap[minChildIndex], heap[curr]
                curr = minChildIndex
            else:
                # settled down
                break
        return heap

    def siftUp(self, index, heap):
        curr = index
        while True:
            parentIndex = self.getParent(curr)

            # if parent is non existent!
            if parentIndex == None:
                break

            if heap[curr] < heap[parentIndex]:
                heap[curr], heap[parentIndex] = heap[parentIndex], heap[curr]
                curr = parentIndex
            else:
                # if you cant go any more up!
                break
        return heap

    def getChildren(self, parentIndex, heap):
        child1 = 2 * parentIndex + 1
        child2 = 2 * parentIndex + 2

        isChild1InBounds = (child1 < len(heap))
        isChild2InBounds = (child2 < len(heap))
        if isChild1InBounds and isChild2InBounds:
            return child1, child2
        elif isChild1InBounds and not isChild2InBounds:
            return child1, None
        else:
            return None, None

    def getParent(self, childIndex):
        parentIndex = (childIndex - 1) // 2
        return parentIndex if parentIndex >= 0 else None

    def followsMinHeapProperty(self):
        array = self.heap[:]
        q = [(array[0], 0)]

        while q:
            curr, i = q.pop()
            child1, child2 = self.getChildren(i, array)
            isChild1Present = child1 != None
            isChild2Present = child2 != None

            if not isChild1Present and not isChild2Present:
                continue
            elif isChild1Present and not isChild2Present:
                if curr <= array[child1]:
                    q.append((array[child1], child1))
                else:
                    return False
            else:
                # both present
                if curr <= array[child1] and curr <= array[child2]:
                    q.append((array[child1], child1))
                    q.append((array[child2], child2))
                else:
                    return False

        return True


if __name__ == '__main__':
    # array = [5,3,1,8,0]
    # array = [48, 12, 24, 7, 8, -5, 24, 391, 24, 56, 2, 6, 8, 41]
    array = [544, -578, 556, 713, -655, -359, -810, -731, 194, -531, -685, 689, -279, -738, 886, -54, -320, -500, 738,
             445, -401, 993, -753, 329, -396, -924, -975, 376, 748, -356, 972, 459, 399, 669, -488, 568, -702, 551, 763,
             -90, -249, -45, 452, -917, 394, 195, -877, 153, 153, 788, 844, 867, 266, -739, 904, -154, -947, 464, 343,
             -312, 150, -656, 528, 61, 94, -581]
    copy = array[:]
    mh = MinHeap(array)

    heapq.heapify(copy)
    # mh.followsMinHeapProperty(copy)
    mh.followsMinHeapProperty()
