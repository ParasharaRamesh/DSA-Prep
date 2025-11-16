'''
Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

'''

from collections import Counter
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # option 1 (check if length of set is less than length of array)
        return len(set(nums)) < len(nums)

        # option 2 (use counter to count the number of times each number appears)
        # counts = Counter(nums)
        # for num in counts:
        #     count = counts[num]
        #     if count > 1:
        #         return True
        # return False

        # option 3 (use hashset to see ifthere is a duplicate anywhere)
        # seen = set()
        # for num in nums:
        #     if num in seen:
        #         return True
        #     seen.add(num)
        # return False
