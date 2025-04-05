'''
The median is the middle value in a sorted list of integers. For lists of even length, there is no middle value, so the median is the mean of the two middle values.

For example:

For arr = [1,2,3], the median is 2.
For arr = [1,2], the median is (1 + 2) / 2 = 1.5
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far.
Example 1:

Input:
["MedianFinder", "addNum", "1", "findMedian", "addNum", "3" "findMedian", "addNum", "2", "findMedian"]

Output:
[null, null, 1.0, null, 2.0, null, 2.0]

Explanation:
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.findMedian(); // return 1.0
medianFinder.addNum(3);    // arr = [1, 3]
medianFinder.findMedian(); // return 2.0
medianFinder.addNum(2);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
Constraints:

-100,000 <= num <= 100,000
findMedian will only be called after adding at least one integer to the data structure.

Insights:

* We maintain a maxheap and a minheap for the stream of incoming numbers. [....maxheap][minheap....]
* Idea being that if at all they are nearly identical in length then:
    - even case: just pop max and pop min respectively and take average
    - odd case: just pop the element from the heap which has one more element than the other
* As numbers come into the stream we try to maintain it such a way:
    - push to min heap first
    - if a number is bigger than the min in minheap then push to minheap else push to maxheap ( so that we maintain the [....maxheap][minheap....] order)
    - after this ensure that the max difference in lengths is 1, if not pop from the bigger heap and push into the smaller heap interms of length.

'''

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
