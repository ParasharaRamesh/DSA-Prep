'''
You are given an array of integers nums, where nums[i] represents the maximum length of a jump towards the right from index i. For example, if you are at nums[i], you can jump to any index i + j where:

j <= nums[i]
i + j < nums.length
You are initially positioned at nums[0].

Return the minimum number of jumps to reach the last position in the array (index nums.length - 1). You may assume there is always a valid answer.

Example 1:

Input: nums = [2,4,1,1,1,1]

Output: 2
Explanation: Jump from index 0 to index 1, then jump from index 1 to the last index.

Example 2:

Input: nums = [2,1,2,1,0]

Output: 2
Constraints:

1 <= nums.length <= 1000
0 <= nums[i] <= 100
'''
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        l, r = 0, 0
        res = 0

        while r < len(nums) - 1:
            farthest = 0
            for i in range(l, r + 1):
                farthest = max(farthest, i + nums[i])
            l = r + 1
            r = farthest
            res += 1

        return res

