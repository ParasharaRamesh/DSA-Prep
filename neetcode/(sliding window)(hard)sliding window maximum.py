'''
You are given an array of integers nums and an integer k. There is a sliding window of size k that starts at the left edge of the array. The window slides one position to the right until it reaches the right edge of the array.

Return a list that contains the maximum element in the window at each step.

Example 1:

Input: nums = [1,2,1,0,4,2,6], k = 3

Output: [2,2,4,4,6]

Explanation:
Window position            Max
---------------           -----
[1  2  1] 0  4  2  6        2
 1 [2  1  0] 4  2  6        2
 1  2 [1  0  4] 2  6        4
 1  2  1 [0  4  2] 6        4
 1  2  1  0 [4  2  6]       6
Constraints:

1 <= nums.length <= 1000
-1000 <= nums[i] <= 1000
1 <= k <= nums.length

Insights:

. max heap plus static sliding window
. throw away anything not in relevant range

'''

from heapq import *
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        windows = []
        max_heap = []

        # init
        for i in range(k):
            heappush(max_heap, (-nums[i], i))
        windows.append(-max_heap[0][0])

        # go through the rest, each element is the new elem in the window
        for r in range(k, len(nums)):
            l = r - (k - 1)

            # add it first
            heappush(max_heap, (-nums[r], r))

            # throw away until not relevant
            while not (l <= max_heap[0][1] <= r):
                heappop(max_heap)

            windows.append(-max_heap[0][0])

        return windows
