'''
You are given an integer array nums where each element nums[i] indicates your maximum jump length at that position.

Return true if you can reach the last index starting from index 0, or false otherwise.

Example 1:

Input: nums = [1,2,0,1,0]

Output: true
Explanation: First jump from index 0 to 1, then from index 1 to 3, and lastly from index 3 to 4.

Example 2:

Input: nums = [1,2,1,0,1]

Output: false
Constraints:

1 <= nums.length <= 1000
0 <= nums[i] <= 1000

'''
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        cache = dict()

        def helper(i):
            if i in cache:
                return cache[i]

            if i == len(nums) - 1:
                cache[i] = True
                return True

            if i >= len(nums):
                cache[i] = False
                return False

            if nums[i] == 0:
                cache[i] = False
                return False

            is_possible = False

            for k in range(1, nums[i] + 1):
                is_possible = is_possible or helper(i + k)

            cache[i] = is_possible
            return is_possible

        return helper(0)