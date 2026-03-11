'''
Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

 

Example 1:

Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
Example 2:

Input: nums = [2,0,1]
Output: [0,1,2]
 

Constraints:

n == nums.length
1 <= n <= 300
nums[i] is either 0, 1, or 2.
 

Follow up: Could you come up with a one-pass algorithm using only constant extra space?
'''
from collections import Counter

class Solution:
    def sortColors_count_and_overwrite(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        counts = Counter(nums)

        i = 0
        for num in range(3):
            while counts[num] > 0:
                nums[i] = num
                i += 1
                counts[num] -= 1

    def sortColors_3pointer(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # b represents boundary
        b0 = -1
        b2 = len(nums)

        i = 0

        while i < b2:
            while nums[i] == 0 or nums[i] == 2:
                if nums[i] == 0:
                    b0 += 1
                    nums[i], nums[b0] = nums[b0], nums[i]
                elif nums[i] == 2:
                    b2 -= 1 
                    nums[i], nums[b2] = nums[b2], nums[i]

                if i == b0 or i == b2:
                    break

            i += 1

