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

# from functools import cache

class Solution:
    def helper(self, n, res, cache):
        if n in cache:
            return cache[n]

        if n < 0:
            cache[n] = 0
            return 0

        if n == 0:
            res += 1
            cache[n] = res
            return res

        cache[n] = self.helper(n-1, res, cache) + self.helper(n-2, res, cache)
        return cache[n]

    def climbStairs(self, n: int) -> int:
        res = 0
        cache = dict()
        res = self.helper(n, res, cache)
        return res