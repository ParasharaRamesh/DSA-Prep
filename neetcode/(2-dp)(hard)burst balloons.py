'''
You are given an array of integers nums of size n. The ith element represents a balloon with an integer value of nums[i]. You must burst all of the balloons.

If you burst the ith balloon, you will receive nums[i - 1] * nums[i] * nums[i + 1] coins. If i - 1 or i + 1 goes out of bounds of the array, then assume the out of bounds value is 1.

Return the maximum number of coins you can receive by bursting all of the balloons.

Example 1:

Input: nums = [4,2,3,7]

Output: 167

Explanation:
nums = [4,2,3,7] --> [4,3,7] --> [4,7] --> [7] --> []
coins =  4*2*3    +   4*3*7   +  1*4*7  + 1*7*1 = 143
Constraints:

n == nums.length
1 <= n <= 300
0 <= nums[i] <= 100

'''
from typing import List


class Solution:
    def __init__(self):
        self.cache = dict()

    def maxCoins(self, nums: List[int]) -> int:
        key = tuple(nums)

        if key in self.cache:
            return self.cache[key]

        if len(nums) == 1:
            self.cache[key] = nums[0]
            return nums[0]

        max_coins = 0

        for i, num in enumerate(nums):
            if i == 0:
                burst_i = num * nums[i + 1]
            elif i == len(nums) - 1:
                burst_i = num * nums[i - 1]
            else:
                burst_i = nums[i - 1] * num * nums[i + 1]

            total_burst_i = burst_i + self.maxCoins(nums[:i] + nums[i + 1:])
            max_coins = max(max_coins, total_burst_i)

        self.cache[key] = max_coins

        return max_coins
