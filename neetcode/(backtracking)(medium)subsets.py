'''
Given an array nums of unique integers, return all possible subsets of nums.

The solution set must not contain duplicate subsets. You may return the solution in any order.

Example 1:

Input: nums = [1,2,3]

Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
Example 2:

Input: nums = [7]

Output: [[],[7]]
Constraints:

1 <= nums.length <= 10
-10 <= nums[i] <= 10

'''

from typing import List
from itertools import *
from functools import *
from copy import deepcopy

class Solution:
    def getBinaryNumbers(self, n: int) -> List[int]:
        nums = list(range(0, 2 ** n))
        selectors = []
        for num in nums:
            b = f"{num:0{n}b}"
            b = [int(x) for x in b]
            selectors.append(b)
        return selectors

    def subsets_using_binary_counting(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        binaryNumbers = self.getBinaryNumbers(n)
        subsets = []
        for binaryNumber in binaryNumbers:
            subsets.append(list(compress(nums, binaryNumber)))
        return subsets

    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        self.helper(nums, [], all_subsets)
        return all_subsets

    def helper(self, nums, curr_subset, all_subsets):
        if len(nums) == 0:
            all_subsets.append(curr_subset)
            return

        self.helper(nums[1:], curr_subset + [nums[0]], all_subsets)
        self.helper(nums[1:], curr_subset, all_subsets)

    def subsets_backtracking(self, nums):
        res = []

        def helper(i, subset):
            if i == len(nums):
                res.append(subset[:])
                return 

            # exclude
            helper(i+1, subset)

            # include
            subset.append(nums[i])
            helper(i + 1, subset)   
            subset.pop()

        helper(0, [])
        return res

if __name__ == "__main__":
    s = Solution()
    print(s.subsets_backtracking([1,2,3]))  

