'''
You are given an integer array nums where nums[i] represents the amount of money the ith house has. The houses are arranged in a straight line, i.e. the ith house is the neighbor of the (i-1)th and (i+1)th house.

You are planning to rob money from the houses, but you cannot rob two adjacent houses because the security system will automatically alert the police if two adjacent houses were both broken into.

Return the maximum amount of money you can rob without alerting the police.

Example 1:

Input: nums = [1,1,3,3]

Output: 4
Explanation: nums[0] + nums[2] = 1 + 3 = 4.

Example 2:

Input: nums = [2,9,8,3,6]

Output: 16
Explanation: nums[0] + nums[2] + nums[4] = 2 + 8 + 6 = 16.

Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 100
'''
from typing import List


class Solution:
    #topdown
    def rob_topdown(self, nums: List[int]) -> int:
        cache = dict()

        def helper(i):
            if i in cache:
                return cache[i]

            if i >= len(nums):
                cache[i] = 0
                return 0

            exc = helper(i+1)
            inc = nums[i] + helper(i+2)
            cache[i] = max(exc, inc)
            return cache[i]

        return helper(0)

    #bottomup
    def rob(self, nums: List[int]) -> int:
        cache = dict()

        n = len(nums)

        #basecases
        cache[n] = 0
        cache[n+1] = 0
        cache[n+2] = 0

        #reverse topological
        for i in range(n-1, -1, -1):
            exc = cache[i+1]
            inc = nums[i] + cache[i+2]
            cache[i] = max(exc, inc)

        return cache[0]
