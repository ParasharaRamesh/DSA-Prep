from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return -1

    def leftmost(self, nums: List[int], target: int) -> int:
        # Find the leftmost occurrence or insertion index
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                # Case 1: Match, but keep going left
                r = m - 1
            elif nums[m] < target:
                # Case 2: Go right
                l = m + 1
            else:  # nums[m] > target
                # Case 3: Go left
                r = m - 1
        return l  # l is the insertion index or first occurrence

    def rightmost(self, nums: List[int], target: int) -> int:
        # Find the rightmost occurrence or insertion index
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                # Case 1: Match, but keep going right
                l = m + 1
            elif nums[m] < target:
                # Case 2: Go right
                l = m + 1
            else:  # nums[m] > target
                # Case 3: Go left
                r = m - 1
        # If found, r points to last occurrence; otherwise, l is insertion index
        return r if r >= 0 and nums[r] == target else l