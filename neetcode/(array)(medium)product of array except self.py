'''

Given an integer array nums, return an array output where output[i] is the product of all the elements of nums except nums[i].

Each product is guaranteed to fit in a 32-bit integer.

Follow-up: Could you solve it in O(n) time without using the division operation?

Example 1:

Input: nums = [1,2,4,6]

Output: [48,24,12,8]
Example 2:

Input: nums = [-1,0,1,2,3]

Output: [0,-6,0,0,0]
Constraints:

2 <= nums.length <= 1000
-20 <= nums[i] <= 20

'''

from collections import deque


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = []
        pre = []
        suf = deque([])

        p = 1
        for num in nums:
            p *= num
            pre.append(p)

        s = 1
        for num in reversed(nums):
            s *= num
            suf.appendleft(s)

        for i, num in enumerate(nums):
            if i == 0:
                res.append(suf[1])
            elif i == len(nums) - 1:
                res.append(pre[-2])
            else:
                res.append(pre[i - 1] * suf[i + 1])

        return res
