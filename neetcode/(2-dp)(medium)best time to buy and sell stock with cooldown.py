'''
You are given an integer array prices where prices[i] is the price of NeetCoin on the ith day.

You may buy and sell one NeetCoin multiple times with the following restrictions:

After you sell your NeetCoin, you cannot buy another one on the next day (i.e., there is a cooldown period of one day).
You may only own at most one NeetCoin at a time.
You may complete as many transactions as you like.

Return the maximum profit you can achieve.

Example 1:

Input: prices = [1,3,4,0,4]

Output: 6
Explanation: Buy on day 0 (price = 1) and sell on day 1 (price = 3), profit = 3-1 = 2. Then buy on day 3 (price = 0) and sell on day 4 (price = 4), profit = 4-0 = 4. Total profit is 2 + 4 = 6.

Example 2:

Input: prices = [1]

Output: 0
Constraints:

1 <= prices.length <= 5000
0 <= prices[i] <= 1000
'''

from typing import List


class Solution:
    # TLE : on leetcode 208/210 but worked on neetcode
    def maxProfit_memo(self, prices: List[int]) -> int:
        # trivial case as cannot sell
        if len(prices) == 1:
            return 0

        n = len(prices)
        cache = dict()

        def helper(i, existing_profit):
            key = (i, existing_profit)

            if key in cache:
                return cache[key]

            if i >= n:
                cache[key] = existing_profit
                return cache[key]

            # exclude: buying on ith day and move ahead
            exc = helper(i + 1, existing_profit)

            # include: choose to buy on ith day
            buy = prices[i]

            # choose to sell on jth day
            best_inc = 0
            for j in range(i + 1, n):
                sell = prices[j]
                if sell >= buy:
                    profit = sell - buy
                    inc = helper(j + 2, existing_profit + profit)
                    best_inc = max(best_inc, inc)

            cache[key] = max(exc, best_inc)
            return cache[key]

        return helper(0, 0)

    # bottom up approach: TLE in leetcode 208/210, but worked in neetcode
    def maxProfit_tab(self, prices: List[int]) -> int:
        # trivial case as cannot sell
        if len(prices) == 1:
            return 0

        n = len(prices)
        cache = dict()

        # base cases
        total_profit = sum(prices)
        for p in range(total_profit + 1):
            cache[(n, p)] = p

        # visit all states
        for i in range(n - 1, -1, -1):
            for existing_profit in range(total_profit, -1, -1):
                key = (i, existing_profit)

                # exclude: buying on ith day and move ahead
                exc = cache.get((i + 1, existing_profit), existing_profit)

                # include: choose to buy on ith day
                buy = prices[i]

                # choose to sell on jth day
                best_inc = 0
                for j in range(i + 1, n):
                    sell = prices[j]
                    if sell >= buy:
                        profit = sell - buy
                        inc = cache.get((j + 2, existing_profit + profit), existing_profit + profit)
                        best_inc = max(best_inc, inc)

                cache[key] = max(exc, best_inc)

        return cache[(0, 0)]

    # Top down worked in leetcode :)
    def maxProfit_memo_2(self, prices: List[int]) -> int:
        # trivial case as cannot sell
        if len(prices) == 1:
            return 0

        n = len(prices)
        cache = dict()

        # 2d dp because at each point we need to know whether we are allowed to buy or we are in cooling because we may have bought something before!
        def helper(i, can_buy):
            key = (i, can_buy)

            if key in cache:
                return cache[key]

            if i >= n:
                cache[key] = 0
                return 0

            if not can_buy:
                # just go to the next one
                cache[key] = helper(i + 1, True)
                return cache[key]

            # in case can_buy is already True

            # exclude: buying on ith day and move ahead
            exc = helper(i + 1, True)

            # include: choose to buy on ith day
            buy = prices[i]

            # choose to sell on jth day
            best_inc = 0
            for j in range(i + 1, n):
                sell = prices[j]
                if sell >= buy:
                    profit = sell - buy
                    inc = profit + helper(j + 2, True)
                    best_inc = max(best_inc, inc)

            cache[key] = max(exc, best_inc)
            return cache[key]

        # always allowed to buy when starting
        return helper(0, True)

    # bottom up approach 2 works :)
    def maxProfit_tab_2(self, prices: List[int]) -> int:
        # trivial case as cannot sell
        if len(prices) == 1:
            return 0

        n = len(prices)
        cache = dict()

        # base cases
        cache[(n, True)] = 0
        cache[(n, False)] = 0
        cache[(n + 1, True)] = 0
        cache[(n + 1, False)] = 0

        # all states
        for i in range(n - 1, -1, -1):
            for can_buy in [False, True]:
                key = (i, can_buy)

                if can_buy:
                    # exclude: buying on ith day and move ahead
                    exc = cache[(i + 1, True)]

                    # include: choose to buy on ith day
                    buy = prices[i]

                    # choose to sell on jth day
                    best_inc = 0
                    for j in range(i + 1, n):
                        sell = prices[j]
                        if sell >= buy:
                            profit = sell - buy
                            inc = profit + cache[(j + 2, True)]
                            best_inc = max(best_inc, inc)

                    cache[key] = max(exc, best_inc)
                else:
                    # just go to the next one
                    cache[key] = cache[(i + 1, True)]

        # always allowed to buy when starting
        return cache[(0, True)]

if __name__ == '__main__':
    s = Solution()

    prices = [1, 2, 3, 0, 2]
    expected = 3
    ans = s.maxProfit(prices)
    assert expected == ans, f"{expected=}, {ans=}"

    prices = [1, 3, 4, 0, 4]
    expected = 6
    ans = s.maxProfit(prices)
    assert expected == ans, f"{expected=}, {ans=}"

    prices = [1]
    expected = 0
    ans = s.maxProfit(prices)
    assert expected == ans, f"{expected=}, {ans=}"
