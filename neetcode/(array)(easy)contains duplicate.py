'''
Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

'''

from collections import Counter
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)
        # counts = Counter(nums)
        # for num in counts:
        #     count = counts[num]
        #     if count > 1:
        #         return True
        # return False
