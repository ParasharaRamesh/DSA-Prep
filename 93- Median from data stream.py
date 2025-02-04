from heapq import *


class MedianFinder:
    def __init__(self):
        self.count = 0
        self.maxH = []
        self.minH = []

    def addNum(self, num: int) -> None:
        self.count += 1

        if not self.minH and not self.maxH:
            heappush(self.minH, num)
            return

        if num >= self.minH[0]:
            heappush(self.minH, num)
        else:
            heappush(self.maxH, -num)

        max_h_len = len(self.maxH)
        min_h_len = len(self.minH)

        if abs(max_h_len - min_h_len) <= 1:
            return
        elif max_h_len > min_h_len:
            curr_max = heappop(self.maxH)
            heappush(self.minH, -curr_max)
        elif max_h_len < min_h_len:
            curr_min = heappop(self.minH)
            heappush(self.maxH, -curr_min)
        else:
            print("invalid case")

    def findMedian(self) -> float:
        if self.count % 2 == 1:
            assert abs(len(self.maxH) - len(self.minH)) == 1, "heap diff is not 1 when count is odd"
            # return from the larger half
            if len(self.maxH) > len(self.minH):
                return -1 * self.maxH[0]
            else:
                return self.minH[0]
        else:
            assert abs(len(self.maxH) - len(self.minH)) == 0, "heap diff is not 0 when count is even"
            return (self.minH[0] - self.maxH[0]) / 2

if __name__ == '__main__':
    mf = MedianFinder()
    mf.addNum(1)
    print(mf.findMedian()) # 1
    mf.addNum(3)
    print(mf.findMedian()) # 2
    mf.addNum(2)
    print(mf.findMedian())  # 2
    mf.addNum(4)
    print(mf.findMedian()) # 2.5
    mf.addNum(0)
    print(mf.findMedian()) # 2


