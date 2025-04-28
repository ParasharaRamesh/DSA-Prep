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
from collections import defaultdict, UserDict
from typing import List

class Solution:
    def coinChange_topdown(self, coins: List[int], amount: int) -> int:
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

    def coinChange_bottomup(self, coins: List[int], amount: int) -> int:
        cache = defaultdict(int)
        n = len(coins)

        # base cases (handled inside loops)
        for i in range(n, -1, -1):
            #just went through all of the amounts
            for amt in range(0, amount + 1):
                key = (i, amt)

                if amt == 0:
                    cache[key] = 0
                elif i == n:
                    cache[key] = float("inf")
                else:
                    inc = float("inf")
                    exc = float("inf")

                    if coins[i] <= amt:
                        inc = 1 + cache[(i, amt - coins[i])]

                    exc = cache[(i + 1, amt)]

                    cache[key] = min(inc, exc)

        res = cache[(0, amount)]
        return res if res < float("inf") else -1

    def coinChange_bottomup_trick(coins: List[int], amount: int) -> int:
        n = len(coins)
        dp = SmartDP(n) #refer to the class below

        # Fill states starting from i = n-1 to 0
        for i in range(n - 1, -1, -1):
            for amt in range(1, amount + 1):
                #none of the conditions are needed, since if a key is missing, dp will return the correct one automatically! :)
                inc = 1 + dp[(i, amt - coins[i])]
                exc = dp[(i + 1, amt)]
                dp[(i, amt)] = min(inc, exc)

        res = dp[(0, amount)]
        return res if res < float("inf") else -1


#useful for the bottom up trick for dp
class SmartDP(UserDict):
    def __init__(self, coins_len):
        super().__init__()
        self.coins_len = coins_len

    def __missing__(self, key):
        i, amt = key

        if amt < 0:
            return float("inf")
        elif amt == 0:
            value = 0
        elif i >= self.coins_len:
            value = float("inf")
        else:
            value = float("inf")

        self[key] = value  # memoize
        return value