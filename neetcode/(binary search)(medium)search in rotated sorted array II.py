'''
You are given an array of length n which was originally sorted in non-decreasing order (not necessarily with distinct values). It has now been rotated between 1 and n times. For example, the array nums = [1,2,3,4,5,6] might become:

[3,4,5,6,1,2] if it was rotated 4 times.
[1,2,3,4,5,6] if it was rotated 6 times.
Given the rotated sorted array nums and an integer target, return true if target is in nums, or false if it is not present.

You must decrease the overall operation steps as much as possible.

Example 1:

Input: nums = [3,4,4,5,6,1,2,2], target = 1

Output: true
Example 2:

Input: nums = [3,5,6,0,0,1,2], target = 4

Output: false
Constraints:

1 <= nums.length <= 5000
-10,000 <= target, nums[i] <= 10,000
nums is guaranteed to be rotated at some pivot.
'''

class Solution:
    def binarysearch(self, nums, l, r, target):
        while l <= r:
            m = (l + r)//2

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
            m = (l + r)//2
            if nums[l] < nums[m]:
                l = m + 1 if nums[m] < nums[m + 1] else m
            elif nums[l] >= nums[m]:
                r = m - 1 if nums[m-1] < nums[m] else m

        return l

    def search_unique(self, nums: List[int], target: int) -> int:
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
            return self.binarysearch(nums, m+1, r, target)
        
    def search(self, nums: List[int], target: int) -> bool:
        unique = []
        seen = set()

        for num in nums:
            if num in seen:
                continue
            
            seen.add(num)
            unique.append(num)
        
        res = self.search_unique(unique, target)
        return res != -1 
