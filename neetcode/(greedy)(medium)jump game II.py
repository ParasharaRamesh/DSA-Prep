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

'''
. inside the range from [l,r] figure out what is the furthest you can reach. Therefore in one jump you can reach anywhere from [l, farthest]
. once we find the max farthest in the range [l, r] that constitutes as one jump
. move l to the next one after r (i.e after current window) & move r to the current farthest point
. the moment r is greater than the last index, we just stop
'''

class Solution:
    def jump(self, nums: List[int]) -> int:
        l, r = 0, 0
        jumps = 0

        # kind of like sliding window
        while r < len(nums) - 1:
            # inside the range from [l,r] figure out what is the furthest you can reach. Therefore in one jump you can reach anywhere from [l, farthest]
            farthest = 0
            for i in range(l, r + 1):
                farthest = max(farthest, i + nums[i])

            # once we find the max farthest in the range [l, r] that constitutes as one jump
            jumps += 1

            # move l to the next one after r (i.e after current window) & move r to the current farthest point
            l = r + 1
            r = farthest

        # the moment r is greater than the last index, we just stop
        return jumps

if __name__ == '__main__':
    s = Solution()

    nums = [7,0,9,6,9,6,1,7,9,0,1,2,9,0,3]
    expected = 2
    ans = s.jump(nums)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [2]
    expected = 0
    ans = s.jump(nums)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [1, 2]
    expected = 1
    ans = s.jump(nums)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [2,1,2,1,0]
    expected = 2
    ans = s.jump(nums)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [2,4,1,1,1]
    expected = 2
    ans = s.jump(nums)
    assert expected == ans, f"{expected = }, {ans = }"