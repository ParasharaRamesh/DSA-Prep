'''
You are given an integer n, break it into the sum of k positive integers, where k >= 2, and maximize the product of those integers.

Return the maximum product you can get.

Example 1:

Input: n = 4

Output: 4
Explanation: 4 = 2 + 2, 2 x 2 = 4.

Example 2:

Input: n = 12

Output: 81
Explanation: 12 = 3 + 3 + 3 + 3, 3 x 3 x 3 x 3 = 81.

Constraints:

2 <= n <= 58

Thoughts:
1. there is an O(N) math solution but thats hard to come up with 
2. the simple solution is to just use dp 
 * the tricky thing is the initialization of res. we are ensuring that if num == n, we return 0 as we are not allowed to break it into just 1 part
 * which means for any other number lesser than that n we can just return the number itself as it is the starting point ( e.g. if 4 is broken into 3 and 1 ; then we dont need to break up the 3 further down into 2 and 1 and can instead retain the 3 as is!)
'''

class Solution:
    def integerBreak_memo(self, n: int) -> int:
        dp = dict()

        def helper(num):
            if num in dp:
                return dp[num]

            if num == 1:
                dp[num] = 1
                return 1

            res = 0 if num == n else num # as this is the starting

            for i in range(1, num):
                val = helper(i) * helper(num - i)
                res = max(res, val)

            dp[num] = res
            return res

        return helper(n)

    def integerBreak_tabulation(self, n: int) -> int:
        dp = {1: 1}

        for num in range(1, n + 1):
            res = 0 if num == n else num # as this is the starting

            for i in range(1, num):
                val = dp[i] * dp[num - i]
                res = max(res, val)

            dp[num] = res

        return dp[n]