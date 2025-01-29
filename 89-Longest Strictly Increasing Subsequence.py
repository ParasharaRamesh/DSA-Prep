'''
Given an integer array nums, return the length of the longest strictly increasing
subsequence
.



Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4
Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1


'''
from typing import List
from bisect import bisect_left

class Solution:
    def lengthOfLIS_dp(self, nums: List[int]) -> int:
        cache = dict()

        def helper(i, curr_num):
            key = (i, curr_num)

            if key in cache:
                return cache[key]

            if i == len(nums):
                cache[key] = 0
                return 0

            inc = 0
            exc = 0
            # include
            if nums[i] > curr_num:
                inc = 1 + helper(i + 1, nums[i])

            # exclude
            exc = helper(i + 1, curr_num)

            cache[key] = max(inc, exc)
            return cache[key]

        return helper(0, float("-inf"))

    # uses binary search
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []

        for num in nums:
            i = bisect_left(sub, num)

            if len(sub) == i:
                sub.append(num)
            else:
                sub[i] = num

        return len(sub)

if __name__ == '__main__':
    s = Solution()
    # nums = [10,9,2,5,3,7,101,18]
    nums = [0,1,0,3,2,3]
    print(s.lengthOfLIS(nums))