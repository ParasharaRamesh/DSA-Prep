'''
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.



Example 1:

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
Example 2:

Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.
Example 3:

Input: amount = 10, coins = [10]
Output: 1


Constraints:

1 <= coins.length <= 300
1 <= coins[i] <= 5000
All the values of coins are unique.
0 <= amount <= 5000
'''

from collections import defaultdict
from typing import List


class Solution:
    def change_memo(self, amount: int, coins: List[int]) -> int:
        cache = dict()

        def helper(i, left):
            key = (i, left)

            if key in cache:
                return cache[key]

            if i >= len(coins):
                cache[key] = 0
                return 0

            if left == 0:
                cache[key] = 1
                return 1

            total = 0

            if coins[i] <= left:
                total += helper(i, left - coins[i])

            total += helper(i + 1, left)

            cache[key] = total
            return total

    def change_tabulation(self, amount: int, coins: List[int]) -> int:
        cache = defaultdict(int)

        # when left == 0 (notice that i had to go till len(coins) => just blindly reverse the top down conditions!)
        for i in range(len(coins) + 1):
            cache[(i, 0)] = 1

        # when i >= len(coins) handled by default dict

        for i in range(len(coins) - 1, -1, -1):
            for left in range(0, amount + 1):
                key = (i, left)

                total = 0

                if coins[i] <= left:
                    total += cache[(i, left - coins[i])]

                total += cache[(i + 1, left)]

                cache[key] = total

        return cache[(0, amount)]
