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
from collections import defaultdict
from typing import List


class Solution:
    def __init__(self):
        self.cache = dict()

    # bit space inefficient but very similar principles
    def maxCoins_mysolution(self, nums: List[int]) -> int:
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

            # joining the ends
            total_burst_i = burst_i + self.maxCoins(nums[:i] + nums[i + 1:])
            max_coins = max(max_coins, total_burst_i)

        self.cache[key] = max_coins

        return max_coins

    # topdown neetcode inspired solution: since we are dealing with subarray slices, we can as well just use l & r
    def maxCoins_memo(self, nums: List[int]) -> int:
        # extending the ends
        nums = [1] + nums + [1]

        cache = dict()

        def helper(l, r):
            key = (l, r)

            if key in cache:
                return cache[key]

            # invalid state
            if l > r:
                cache[key] = 0
                return 0

            max_coins = 0
            for i in range(l, r + 1):
                # burst everything else first
                coins = helper(l, i - 1) + helper(i + 1, r)

                # then burst ith balloon ( with whatever is left )
                coins += nums[l - 1] * nums[i] * nums[r + 1]
                max_coins = max(max_coins, coins)

            cache[key] = max_coins
            return max_coins

        # excluding the ends
        return helper(1, len(nums) - 2)

    def maxCoins_tabulation(self, nums: List[int]) -> int:
        # extending the ends
        n = len(nums)
        nums = [1] + nums + [1]

        cache = defaultdict(int)

        for l in range(n, 0, -1):
            for r in range(l, n + 1):
                key = (l, r)

                # invalid state l > r will be handled by default dict

                max_coins = 0
                for i in range(l, r + 1):
                    # burst everything else first
                    coins = cache[(l, i - 1)] + cache[(i + 1, r)]

                    # then burst ith balloon ( with whatever is left )
                    coins += nums[l - 1] * nums[i] * nums[r + 1]
                    max_coins = max(max_coins, coins)

                cache[key] = max_coins

        # excluding the ends
        return cache[(1, n)]
