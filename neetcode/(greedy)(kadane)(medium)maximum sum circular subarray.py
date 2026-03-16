'''
Given a circular integer array nums of length n, return the maximum possible sum of a non-empty subarray of nums.

A circular array means the end of the array connects to the beginning of the array. Formally, the next element of nums[i] is nums[(i + 1) % n] and the previous element of nums[i] is nums[(i - 1 + n) % n].

A subarray may only include each element of the fixed buffer nums at most once. Formally, for a subarray nums[i], nums[i + 1], ..., nums[j], there does not exist i <= k1, k2 <= j with k1 % n == k2 % n.

 

Example 1:

Input: nums = [1,-2,3,-2]
Output: 3
Explanation: Subarray [3] has maximum sum 3.
Example 2:

Input: nums = [5,-3,5]
Output: 10
Explanation: Subarray [5,5] has maximum sum 5 + 5 = 10.
Example 3:

Input: nums = [-3,-2,-3]
Output: -2
Explanation: Subarray [-2] has maximum sum -2.
 

Constraints:

n == nums.length
1 <= n <= 3 * 104
-3 * 104 <= nums[i] <= 3 * 104
'''
class Solution:
    '''
    Using kadane -> find both max subarray and min subarray and total
    if max subarray is neg -> return max sub array sum
    else: max(max_sum, total - min_sum) => this ensures that things wrap around
    '''
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        n = len(nums)

        local_max = nums[0]
        global_max = nums[0]
        total = nums[0]
        local_min = nums[0]
        global_min = nums[0]

        for num in nums[1:]:
            local_max = max(local_max + num, num)
            local_min = min(local_min + num, num)
            global_max = max(global_max, local_max)
            global_min = min(global_min, local_min)
            total += num

        print(f"{total=} {global_max=} {global_min=}")

        # best we can do
        if global_max < 0:
            return global_max

        #wrap around
        return max(global_max, total - global_min)

    def maxSubarraySumCircular_nc(self, nums: List[int]) -> int:
        n = len(nums)
        right_max = [0] * n
        right_max[-1] = nums[-1]
        suffix_sum = nums[-1]

        for i in range(n - 2, -1, -1):
            suffix_sum += nums[i]
            right_max[i] = max(right_max[i + 1], suffix_sum)

        max_sum = nums[0]
        cur_max = 0
        prefix_sum = 0

        for i in range(n):
            cur_max = max(cur_max, 0) + nums[i]
            max_sum = max(max_sum, cur_max)
            prefix_sum += nums[i]
            if i + 1 < n:
                max_sum = max(max_sum, prefix_sum + right_max[i + 1])

        return max_sum
