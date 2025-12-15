'''
You are given an integer array nums where nums[i] represents the amount of money the ith house has. The houses are arranged in a circle, i.e. the first house and the last house are neighbors.

You are planning to rob money from the houses, but you cannot rob two adjacent houses because the security system will automatically alert the police if two adjacent houses were both broken into.

Return the maximum amount of money you can rob without alerting the police.

Example 1:

Input: nums = [3,4,3]

Output: 4
Explanation: You cannot rob nums[0] + nums[2] = 6 because nums[0] and nums[2] are adjacent houses. The maximum you can rob is nums[1] = 4.

Example 2:

Input: nums = [2,9,8,3,6]

Output: 15
Explanation: You cannot rob nums[0] + nums[2] + nums[4] = 16 because nums[0] and nums[4] are adjacent houses. The maximum you can rob is nums[1] + nums[4] = 15.

Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 100

'''
from typing import List
from collections import defaultdict

class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        if n == 1:
            return nums[0]

        # do it twice on two different arrays
        return max(self.rob1(nums[1:]), self.rob1(nums[:-1]))

    #house robber 1 solution
    def rob1(self, nums: List[int]) -> int:
        cache = dict()

        def helper(i):
            if i in cache:
                return cache[i]

            if i >= len(nums):
                cache[i] = 0
                return 0

            exc = helper(i + 1)
            inc = nums[i] + helper(i + 2)
            cache[i] = max(exc, inc)
            return cache[i]

        return helper(0)

    #mysolution: keep track of a flag
    def rob(self, nums: List[int]) -> int:
        cache = dict()
        n = len(nums)

        if n == 1:
            return nums[0]

        def helper(i, from_start):
            key = (i, from_start)

            if key in cache:
                return cache[key]

            if from_start:
                # cant include the last one
                if i >= len(nums) - 1:
                    cache[key] = 0
                    return 0
            elif i >= len(nums):
                # can include the last one
                cache[key] = 0
                return 0

            exc = helper(i + 1, from_start)
            inc = nums[i] + helper(i + 2, from_start)

            cache[key] = max(exc, inc)
            return cache[key]

        return max(helper(0, True), helper(1, False))

    # my solution but in bottom up 
    def rob(self, nums: List[int]) -> int:
        cache = defaultdict(int)
        n = len(nums)

        if n == 1:
            return nums[0]

        # base case
        for j in range(n, n+3):
            cache[(j, False)] = 0
            
        cache[(n-1,False)] = nums[n-1]

        for j in range(n-1, n + 3):
            cache[(j, True)] = 0 

        # reverse topo order
        for i in range(n-2, -1, -1):
            for from_start in [True, False]:
                key = (i, from_start)

                exc = cache[(i + 1, from_start)]
                inc = nums[i] + cache[(i + 2, from_start)]

                cache[key] = max(exc, inc)

        return max(
            cache[(0, True)],
            cache[(1, False)]
        )