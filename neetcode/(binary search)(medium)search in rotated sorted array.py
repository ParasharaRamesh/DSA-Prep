'''
You are given an array of length n which was originally sorted in ascending order. It has now been rotated between 1 and n times. For example, the array nums = [1,2,3,4,5,6] might become:

[3,4,5,6,1,2] if it was rotated 4 times.
[1,2,3,4,5,6] if it was rotated 6 times.
Given the rotated sorted array nums and an integer target, return the index of target within nums, or -1 if it is not present.

You may assume all elements in the sorted rotated array nums are unique,

A solution that runs in O(n) time is trivial, can you write an algorithm that runs in O(log n) time?

Example 1:

Input: nums = [3,4,5,6,1,2], target = 1

Output: 4
Example 2:

Input: nums = [3,5,6,0,1,2], target = 4

Output: -1
Constraints:

1 <= nums.length <= 1000
-1000 <= nums[i] <= 1000
-1000 <= target <= 1000

Insights: find the split point and do binary search on the two halves

'''


from typing import List
class Solution:
    def binarysearch(self, nums, l, r, target):
        while l <= r:
            m = (l + r) // 2

            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1

        return -1

    # m ST [lm] and [m+1 r]
    def find_split(self, nums, l, r):
        while l < r:
            m = (l + r) // 2
            if nums[l] < nums[m]:
                l = m + 1 if nums[m] < nums[m + 1] else m
            elif nums[l] >= nums[m]:
                r = m - 1 if nums[m - 1] < nums[m] else m

        return l

    def search_two_pass(self, nums: List[int], target: int) -> int:
        l = 0
        r = len(nums) - 1

        if nums[l] < nums[r]:
            return self.binarysearch(nums, l, r, target)

        m = self.find_split(nums, l, r)
        # print(f"m: {m}, left: {nums[l:m+1]}, right: {nums[m+1:]}")
        left = self.binarysearch(nums, l, m, target)

        if left != -1:
            return left
        else:
            return self.binarysearch(nums, m + 1, r, target)

    # one pass
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            if target == nums[mid]:
                return mid

            # Case 1: Left portion is sorted [l...mid]
            # Example: [4, 5, 6, 7, 0, 1, 2], l=0 (4), mid=3 (7), nums[l] <= nums[mid]
            if nums[l] <= nums[mid]:
                # If target is outside the sorted left portion:
                # 1. target > nums[mid] (target is even larger than the largest in this portion)
                # 2. target < nums[l] (target is smaller than the smallest in this portion)
                # Example: target = 0. 0 < 4 is True. Target must be in the right portion.
                if target > nums[mid] or target < nums[l]:
                    l = mid + 1
                # Target is within the sorted range [nums[l], nums[mid]]
                else:
                    r = mid - 1

            # Case 2: Right portion is sorted [mid...r]
            # Example: [6, 7, 0, 1, 2, 4, 5], l=0 (6), mid=3 (1), nums[l] > nums[mid]
            else:
                # If target is outside the sorted right portion:
                # 1. target < nums[mid] (target is even smaller than the smallest in this portion)
                # 2. target > nums[r] (target is larger than the largest in this portion)
                # Example: target = 6. 6 > 5 is True. Target must be in the left portion.
                if target < nums[mid] or target > nums[r]:
                    r = mid - 1
                # Target is within the sorted range [nums[mid], nums[r]]
                else:
                    l = mid + 1
        return -1
