'''
Given an integer array nums, return the length of the longest strictly increasing subsequence.

A subsequence is a sequence that can be derived from the given sequence by deleting some or no elements without changing the relative order of the remaining characters.

For example, "cat" is a subsequence of "crabt".
Example 1:

Input: nums = [9,1,4,2,3,3,7]

Output: 4
Explanation: The longest increasing subsequence is [1,2,3,7], which has a length of 4.

Example 2:

Input: nums = [0,3,1,3,2,3]

Output: 4
Constraints:

1 <= nums.length <= 1000
-1000 <= nums[i] <= 1000
'''
from bisect import bisect_left
from collections import UserDict
from typing import List


class Solution:
    '''
    Dynamic programming O(N2) solutions
    '''
    #topdown memoization approach
    def lengthOfLIS_memo(self, nums: List[int]) -> int:
        cache = dict()

        def helper(i, curr_num):
            key = (i, curr_num)

            if key in cache:
                return cache[key]

            if i == len(nums):
                cache[key] = 0
                return 0

            # include
            inc = 0
            if nums[i] > curr_num:
                inc = 1 + helper(i + 1, nums[i])

            # exclude
            exc = helper(i + 1, curr_num)

            cache[key] = max(inc, exc)
            return cache[key]

        return helper(0, float("-inf"))

    # bottom up approach which works because the constaints are only from -1000 to 1000
    def lengthOfLIS_bottomup(self, nums: List[int]) -> int:
        n = len(nums)
        cache = dict()

        # base cases
        for i in range(-1001, 1001):
            cache[(n, i)] = 0

        # go through all states
        for i in range(n - 1, -1, -1):
            for curr_num in range(-1001, 1001):
                key = (i, curr_num)

                # include
                inc = 0
                if nums[i] > curr_num:
                    inc = 1 + cache[(i + 1, nums[i])]

                # exclude
                exc = cache[(i + 1, curr_num)]

                cache[key] = max(inc, exc)

        return cache[(0, -1001)]

    # bottom up approach again but with smart userdict cache
    def lengthOfLIS_bottom_up_userdict(self, nums: List[int]) -> int:
        n = len(nums)
        cache = SmartCache(n)

        #eliminated the base case filling by usage of SmartCache!
        for i in range(n - 1, -1, -1):
            for curr_num in range(-1001, 1001):
                key = (i, curr_num)
                inc = 0

                if nums[i] > curr_num:
                    inc = 1 + cache[(i + 1, nums[i])]
                exc = cache[(i + 1, curr_num)]

                cache[key] = max(inc, exc)

        return cache[(0, -1001)]

    ''' 
    binary search: O(nlogn) approach.
    
    Basically for every number try to slot it into the longest strictly increasing subsequence by either:
    a. appending to the end if it is bigger than the biggest
    b. replacing some old value so that we give ourselves a chance to grow even further
        e.g. [4,10,4,3,8,9]. it grows in the following manner:
        [4] - [4,10] - [4,10] (4 replaces the 4) - [3,10] (3 replaces the 4) - [3,8] (8 replaces the 10) - [3,8,9] (Longest strictly increasing subsequence!)
    c. lets say it was just [4,10,3] -> even though 3 replaces the 4 in the last pass to make it [3,10]
        - the len(LIS) is just 2, but 3,10 was not the correct LIS but rather 4,10 was!
        - which means any future changes to the LIS list which is of the same length are invalid! so the first time it ws 4,10 that itself is the LIS       
    '''
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []

        for num in nums:
            i = bisect_left(sub, num)

            if i == len(sub):
                sub.append(num)
            else:
                sub[i] = num

        return len(sub)

class SmartCache(UserDict):
    def __init__(self, n):
        super().__init__()
        self.n = n  # needed to recognize base case

    def __missing__(self, key):
        i, curr_num = key
        if i == self.n:
            self[key] = 0
            return 0

        #important to always raise a KeyError since that is the default behaviour of missing anyways
        raise KeyError(f"Key {key} not handled by SmartCache")