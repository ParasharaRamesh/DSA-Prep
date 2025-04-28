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
    def rob(self, nums: List[int]) -> int:
        cache = dict()

        def helper(i, cost):
            key = (i, cost)

            if key in cache:
                return cache[key]

            # print(f"i:{i}, cost: {cost}")
            if i >= len(nums):
                # print(f"final OUT i: {i}, ans: {cost}")
                cache[key] = cost
                return cost

            if i == len(nums) - 1:
                # print(f"final - last i: {i}, {cost} + {nums[i]} -> ans: {cost + nums[i]}")
                cache[key] = cost + nums[i]
                return cost + nums[i]


            inc = helper(i + 2, cost + nums[i])
            exc = helper(i + 1, cost)
            cache[key] =  max(inc, exc)
            # print(f"final i: {i}, ans: {cache[key]}")
            return cache[key]

        return helper(0, 0)