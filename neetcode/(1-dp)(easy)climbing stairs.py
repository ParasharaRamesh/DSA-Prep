'''
You are given an integer n representing the number of steps to reach the top of a staircase. You can climb with either 1 or 2 steps at a time.

Return the number of distinct ways to climb to the top of the staircase.

Example 1:

Input: n = 2

Output: 2
Explanation:

1 + 1 = 2
2 = 2
Example 2:

Input: n = 3

Output: 3
Explanation:

1 + 1 + 1 = 3
1 + 2 = 3
2 + 1 = 3
Constraints:

1 <= n <= 30
'''

from functools import cache

class Solution:
    def climbStairs_topdown_with_lrucache(self, n: int) -> int:
        @cache
        def helper(i):
            if i > n:
                return 0

            if i == n:
                return 1

            return helper(i + 1) + helper(i + 2)

        res = helper(0)
        return res

    def climbStairs_topdown(self, n: int) -> int:
        cache = dict()

        def helper(i):
            key = i

            if key in cache:
                return cache[key]

            if i > n:
                cache[key] = 0
                return 0

            if i == n:
                cache[key] = 1
                return 1

            cache[key] = helper(i + 1) + helper(i + 2)
            return cache[key]

        res = helper(0)
        return res

    def climbStairs_bottomup(self, n: int) -> int:
        cache = dict()

        # base cases
        cache[0] = 0
        cache[1] = 1
        cache[2] = 2

        for i in range(3, n + 1):
            cache[i] = cache[i - 1] + cache[i - 2]

        return cache[n]
