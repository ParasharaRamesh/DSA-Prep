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

    def search(self, nums: List[int], target: int) -> int:
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
