'''
You are given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:

Input: target = 10, nums = [2,1,5,1,5,3]

Output: 3
Explanation: The subarray [5,1,5] has the minimal length under the problem constraint.

Example 2:

Input: target = 5, nums = [1,2,1]

Output: 0
Constraints:

1 <= nums.length <= 100,000
1 <= nums[i] <= 10,000
1 <= target <= 1,000,000,000
Follow up: If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).

'''

from typing import List

class Solution:
    #sliding window solution 
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        min_len = float("inf")
        window_sum = 0

        for r in range(len(nums)):
            # grow
            window_sum += nums[r]

            # shrink if invalid
            while l <= r and window_sum >= target:
                # assign
                min_len = min(min_len, r - l + 1)

                # shrink
                window_sum -= nums[l]
                l += 1

        return min_len if min_len < float("inf") else 0

    ''' prefix sum + binary search on prefix sum
    . We can precompute prefix sums so that the sum of any subarray from index i to j is prefixSum[j+1] - prefixSum[i]. Since all numbers are positive, the prefix sum array is strictly increasing. 
    . For each starting index i, we can binary search for the smallest ending index j where the subarray sum is at least target.
    
    '''
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        prefixSum = [0] * (n + 1)
        for i in range(n):
            prefixSum[i + 1] = prefixSum[i] + nums[i]

        res = n + 1
        for i in range(n):
            l, r = i, n
            while l < r:
                mid = (l + r) // 2
                curSum = prefixSum[mid + 1] - prefixSum[i]
                if curSum >= target:
                    r = mid
                else:
                    l = mid + 1
            if l != n:
                res = min(res, l - i + 1)

        return res % (n + 1)