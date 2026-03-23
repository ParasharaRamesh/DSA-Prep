'''
You are given an integer array matchsticks where matchsticks[i] is the length of the ith matchstick. You want to use all the matchsticks to make one square. You should not break any stick, but you can link them up, and each matchstick must be used exactly one time.

Return true if you can make this square and false otherwise.

 

Example 1:


Input: matchsticks = [1,1,2,2,2]
Output: true
Explanation: You can form a square with length 2, one side of the square came two sticks with length 1.
Example 2:

Input: matchsticks = [3,3,3,3,4]
Output: false
Explanation: You cannot find a way to form a square with all the matchsticks.
 

Constraints:

1 <= matchsticks.length <= 15
1 <= matchsticks[i] <= 108
'''
from functools import cache

class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        n = len(nums)

        if total % k != 0:
            return False

        target = total // k

        if max(nums) > target:
            return False


        subset_sums = [0]*k 
        nums.sort(reverse=True)

        def f(i):
            nonlocal subset_sums

            if i == n:
                for j in range(k):
                    if subset_sums[j] != target:
                        return False

                return True

            for j in range(k):
                if subset_sums[j] + nums[i] <= target:
                    subset_sums[j] += nums[i]

                    if f(i + 1):
                        return True

                    subset_sums[j] -= nums[i]

                if subset_sums[j] == 0:
                    break

            return False

        return f(0)

class Solution:
    def makesquare_simple_tle(self, matchsticks: List[int]) -> bool:
        if sum(matchsticks) % 4 != 0:
            return False

        sides = [0] * 4

        def dfs(i):
            if i == len(matchsticks):
                return sides[0] == sides[1] == sides[2] == sides[3]

            for side in range(4):
                sides[side] += matchsticks[i]
                if dfs(i + 1):
                    return True
                sides[side] -= matchsticks[i]

            return False

        return dfs(0)

    '''
    Intuition
        The brute force approach explores many redundant paths. We can prune significantly with two optimizations. First, sort matchsticks in descending order so larger sticks are placed first, failing faster when a configuration is impossible. Second, skip trying to place a matchstick on an empty side if we already tried another empty side, since empty sides are interchangeable.

    Algorithm
        Calculate the total length and target side length. Return false if total is not divisible by 4.
        Sort matchsticks in descending order for early pruning.
        In the recursive function, try placing the current matchstick on each side:
            Skip if adding the matchstick would exceed the target length.
            If placement succeeds recursively, return true.
            Backtrack by removing the matchstick.
            If the current side is empty after backtracking, stop trying other sides (they are equivalent).
        Return true if all matchsticks are placed successfully.
    '''
    def makesquare(self, matchsticks: List[int]) -> bool:
        total = sum(matchsticks)
        if total % 4 != 0:
            return False

        sides = [0] * 4
        length = total // 4

        if max(matchsticks) > length:
            return False

        matchsticks.sort(reverse=True)

        def dfs(i):
            if i == len(matchsticks):
                return sides[0] == sides[1] == sides[2] == sides[3] == length

            for side in range(4):
                if sides[side] + matchsticks[i] <= length:
                    sides[side] += matchsticks[i]
                    if dfs(i + 1):
                        return True
                    sides[side] -= matchsticks[i]

                # putting it into any other empty side will also yield the same problem therefore we can skip this
                if sides[side] == 0:
                    break

            return False

        return dfs(0)

    def makesquare_bitmasking_dp(self, matchsticks: List[int]) -> bool:
        if sum(matchsticks) % 4 != 0:
            # trivial case
            return False

        n = len(matchsticks)
        side = sum(matchsticks) // 4

        if max(matchsticks) > side:
            return False

        # NOTE: unused here is a bit mask which can be cached
        @cache
        def f(cuts, used, sum):
            if cuts == 0:
                # check if unused sum up to side
                left = 0
                for j in range(n):
                    mask = 1 << j
                    if (used & mask != mask):
                        left += matchsticks[j]

                return left == side

            '''
            Go through every unused matchstick 
                - if it all it is usable and the current group sum + match stick <= side -> can be picked
                    - reduce the number of cuts and check if that path leads to an answer
                - if not backtrack
            '''
            for j in range(n):
                mask = 1 << j
                if (used & mask != mask) and sum + matchsticks[j] <= side:
                    used ^= mask

                    if sum + matchsticks[j] == side :
                        # cuts should be decremented and the sum restarts from 0
                        if f(cuts - 1, used, 0):
                            return True
                    # cuts should not be decremented!
                    elif f(cuts, used, sum + matchsticks[j]):
                        return True

                    used ^= mask
            
            return False
        
        # we need to make 3 cuts to get 4 groups each having a sum of side
        return f(3, 0, 0)

        
