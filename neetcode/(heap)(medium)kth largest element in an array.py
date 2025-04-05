'''
Given an unsorted array of integers nums and an integer k, return the kth largest element in the array.

By kth largest element, we mean the kth largest element in the sorted order, not the kth distinct element.

Follow-up: Can you solve it without sorting?

Example 1:

Input: nums = [2,3,1,5,4], k = 2

Output: 4
Example 2:

Input: nums = [2,3,1,1,5,5,4], k = 3

Output: 4
Constraints:

1 <= k <= nums.length <= 10000
-1000 <= nums[i] <= 1000

Insights:


'''
from typing import List
from heapq import *

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums = [num * -1 for num in nums]
        heapify(nums)

        ans = None
        for _ in range(k):
            ans = heappop(nums)

        return ans * -1