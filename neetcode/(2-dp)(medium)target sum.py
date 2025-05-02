'''
You are given an array of integers nums and an integer target.

For each number in the array, you can choose to either add or subtract it to a total sum.

For example, if nums = [1, 2], one possible sum would be "+1-2=-1".
If nums=[1,1], there are two different ways to sum the input numbers to get a sum of 0: "+1-1" and "-1+1".

Return the number of different ways that you can build the expression such that the total sum equals target.

Example 1:

Input: nums = [2,2,2], target = 2

Output: 3
Explanation: There are 3 different ways to sum the input numbers to get a sum of 2.
+2 +2 -2 = 2
+2 -2 +2 = 2
-2 +2 +2 = 2

Constraints:

1 <= nums.length <= 20
0 <= nums[i] <= 1000
-1000 <= target <= 1000

'''
from collections import defaultdict
from typing import List


class Solution:
    def findTargetSumWays_memo(self, nums: List[int], target: int) -> int:
        n = len(nums)
        cache = dict()

        # topdown recursion
        def helper(i, left):
            key = (i, left)

            if key in cache:
                return cache[key]

            if i == n:
                cache[key] = 1 if left == 0 else 0
                return cache[key]

            cache[key] = helper(i + 1, left - nums[i]) + helper(i + 1, left + nums[i])
            return cache[key]

        return helper(0, target)

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        cache = defaultdict(int)

        # case2: if i == n and left == 0 -> 1 | All other cases are 0 by defaultdict
        cache[(n, 0)] = 1

        total_target = sum(nums)
        for i in range(n - 1, -1, -1):
            for left in range(-total_target, total_target + 1):
                key = (i, left)
                cache[key] = cache[(i + 1, left - nums[i])] + cache[(i + 1, left + nums[i])]

        return cache[(0, target)]

if __name__ == '__main__':
    s = Solution()

    nums = [2, 2]
    target = 0
    expected = 2
    ans = s.findTargetSumWays(nums, target)
    assert expected == ans, f"{expected = } {ans = }"

    nums = [2, 2, 2]
    target = 4
    expected = 0
    ans = s.findTargetSumWays(nums, target)
    assert expected == ans, f"{expected = } {ans = }"

    nums = [2, 2, 2]
    target = 2
    expected = 3
    ans = s.findTargetSumWays(nums, target)
    assert expected == ans, f"{expected = } {ans = }"
