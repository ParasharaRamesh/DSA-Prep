'''
You are given an array nums of integers, which may contain duplicates. Return all possible subsets.

The solution must not contain duplicate subsets. You may return the solution in any order.

Example 1:

Input: nums = [1,2,1]

Output: [[],[1],[1,2],[1,1],[1,2,1],[2]]
Example 2:

Input: nums = [7,7]

Output: [[],[7], [7,7]]
Constraints:

1 <= nums.length <= 11
-20 <= nums[i] <= 20

'''
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        all_subsets = set()

        def helper(i, subset):
            if i == len(nums):
                all_subsets.add(tuple(subset))
                return

            helper(i + 1, subset)
            helper(i + 1, subset + [nums[i]])

        nums.sort()
        helper(0, [])

        return list(
            map(
                lambda x: list(x),
                all_subsets
            )
        )

if __name__ == '__main__':
    s = Solution()
    print(s.subsetsWithDup([1,2,1]))
