'''
Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

 

Example 1:

Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.
Example 2:

Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.
 

Constraints:

1 <= nums.length <= 1000
0 <= nums[i] <= 106
1 <= k <= min(50, nums.length)
'''
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        l, r = max(nums), sum(nums)

        ans = float("inf")
        while l <= r:
            m = (l + r)//2

            splits = self.get_num_splits(nums, m)
            if splits == k:
                ans = min(ans, m)
                r = m - 1
            elif splits > k:
                l = m + 1
            else:
                r = m - 1

        return ans if ans < float("inf") else l

    def get_num_splits(self, nums, max_sum):
        k = 1
        curr = 0

        for num in nums:
            if curr + num <= max_sum: 
                curr += num
            else:
                curr = num
                k += 1

        return k 
