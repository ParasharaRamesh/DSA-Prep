'''
Alice and Bob are playing a game with piles of stones. There are several stones arranged in a row, and each stone has an associated value which is an integer given in the array stoneValue.

Alice and Bob take turns, with Alice starting first. On each player's turn, that player can take 1, 2, or 3 stones from the first remaining stones in the row.

The score of each player is the sum of the values of the stones taken. The score of each player is 0 initially.

The objective of the game is to end with the highest score, and the winner is the player with the highest score and there could be a tie. The game continues until all the stones have been taken.

Assume Alice and Bob play optimally.

Return "Alice" if Alice will win, "Bob" if Bob will win, or "Tie" if they will end the game with the same score.

Example 1:

Input: stoneValue = [2,4,3,1]

Output: "Alice"
Explanation: In first move, Alice will pick the first three stones (2,4,3) and in the second move Bob will pick the last remaining stone (1). The final score of Alice is (2 + 4 + 3 = 9) which is greater than the Bob's score (1).

Example 2:

Input: stoneValue = [1,2,1,5]

Output: "Bob"
Explanation: In first move, Alice will pick the first three stones (1,2,1) and in the second move Bob will pick the last remaining stone (5). The final score of Alice is (1 + 2 + 1 = 4) which is lesser than the Bob's score (5).

Example 3:

Input: stoneValue = [5,-3,3,5]

Output: "Tie"
Explanation: In first move, Alice will pick the first three stones (5,-3,3) and in the second move Bob will pick the last remaining stone (5). The final score of Alice is (5 + -3 + 3 = 5) which is equal to the Bob's score (5).

Constraints:

1 <= stoneValue.length <= 50,000
-1000 <= stoneValue[i] <= 1000

'''
from typing import List
from functools import cache

class Solution:
   # neetcode inspired solution: at each i irrespective of who starts, what is the advantage that player has (i.e. delta wrt the other player's score?). If the delta is positive -> that player wins
   def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        dp = {}

        def dfs(i):
            if i >= n:
                return 0
            if i in dp:
                return dp[i]

            res, total = float("-inf"), 0
            for j in range(i, min(i + 3, n)):
                total += stoneValue[j]
                res = max(res, total - dfs(j + 1))

            dp[i] = res
            return res

        result = dfs(0)
        if result == 0:
            return "Tie"
        return "Alice" if result > 0 else "Bob"
     
    def stoneGameIII_memoization(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        ps = [0]
        for stone in stoneValue:
            ps.append(ps[-1] + stone)

        range_sum = lambda l, r: ps[r+1] - ps[l]
        total = range_sum(0, n-1)

        # best score alice can make
        @cache
        def f(i, alice):
            if i >= n:
                return 0

            res = float("-inf") if alice else float("inf")

            for j in range(3):
                if i + j < n:
                    remaining = f(i + j + 1, alice ^ True)

                    if alice:
                        take_j = range_sum(i, i + j) + remaining
                        res = max(res, take_j)
                    else:
                        res = min(res, remaining)

            return res

        alice_score = f(0, True)
        bob_score = total - alice_score

        print(f"{alice_score=} {bob_score=}")

        if alice_score > bob_score:
            return "Alice"
        elif alice_score < bob_score:
            return "Bob"
        else:
            return "Tie"
          
    def stoneGameIII_tabulation(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        ps = [0]
        for stone in stoneValue:
            ps.append(ps[-1] + stone)

        range_sum = lambda l, r: ps[r+1] - ps[l]
        total = range_sum(0, n-1)

        cache = dict()

        # base cases
        for alice in [True, False]:
            for i in range(n, n+3):
                cache[(i, alice)] = 0

        # reverse topo order
        for i in range(n-1, -1, -1):
            for alice in [True, False]:
                key = (i, alice)
                res = float("-inf") if alice else float("inf")

                for j in range(3):
                    if i + j < n:
                        remaining = cache[(i + j + 1, alice ^ True)]

                        if alice:
                            take_j = range_sum(i, i + j) + remaining
                            res = max(res, take_j)
                        else:
                            res = min(res, remaining)

                cache[key] = res

        alice_score = cache[(0, True)]
        bob_score = total - alice_score

        print(f"{alice_score=} {bob_score=}")

        if alice_score > bob_score:
            return "Alice"
        elif alice_score < bob_score:
            return "Bob"
        else:
            return "Tie"

  

