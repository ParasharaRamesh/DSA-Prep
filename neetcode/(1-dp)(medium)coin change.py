'''
You are given an integer array coins representing coins of different denominations (e.g. 1 dollar, 5 dollars, etc) and an integer amount representing a target amount of money.

Return the fewest number of coins that you need to make up the exact target amount. If it is impossible to make up the amount, return -1.

You may assume that you have an unlimited number of each coin.

Example 1:

Input: coins = [1,5,10], amount = 12

Output: 3
Explanation: 12 = 10 + 1 + 1. Note that we do not have to use every kind coin available.

Example 2:

Input: coins = [2], amount = 3

Output: -1
Explanation: The amount of 3 cannot be made up with coins of 2.

Example 3:

Input: coins = [1], amount = 0

Output: 0
Explanation: Choosing 0 coins is a valid way to make up 0.

Constraints:

1 <= coins.length <= 10
1 <= coins[i] <= 2^31 - 1
0 <= amount <= 10000

'''
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        cache = dict()

        def helper(i, amount):
            key = (i, amount)

            if key in cache:
                return cache[key]

            if amount == 0:
                cache[key] = 0
                return cache[key]

            if i >= len(coins):
                cache[key] = float("inf")
                return cache[key]

            inc = float("inf")
            exc = float("inf")

            if coins[i] <= amount:
                inc = 1 + helper(i, amount - coins[i])

            exc = helper(i + 1, amount)

            cache[key] = min(inc, exc)
            return cache[key]

        res = helper(0, amount)
        return res if res < float("inf") else -1
