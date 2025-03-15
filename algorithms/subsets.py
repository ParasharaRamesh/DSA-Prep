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



if __name__ == '__main__':
    s = Solution()
    print(s.subsets([1, 2, 3]))
