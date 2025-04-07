'''
You are given an array of positive integers nums.

Return true if you can partition the array into two subsets, subset1 and subset2 where sum(subset1) == sum(subset2). Otherwise, return false.

Example 1:

Input: nums = [1,2,3,4]

Output: true
Explanation: The array can be partitioned as [1, 4] and [2, 3].

Example 2:

Input: nums = [1,2,3,4,5]

Output: false
Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 50

Insights:
- need to see why this is 1D dp and not 2D dp

'''

from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        cache = {}

        def helper(i, target):
            key = (i, target)

            if key in cache:
                return cache[key]

            if i == len(nums):
                cache[key] = False
                return False

            if target < 0:
                cache[key] = False
                return False

            if target == 0:
                cache[key] = True
                return True

            cache[key] = helper(i + 1, target - nums[i]) or helper(i + 1, target)
            return cache[key]

        total = sum(nums)
        if total % 2:
            return False

        return helper(0, total // 2)


