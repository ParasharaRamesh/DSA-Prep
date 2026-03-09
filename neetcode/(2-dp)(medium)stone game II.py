'''
Alice and Bob continue their games with piles of stones. There are a number of piles arranged in a row, and each pile has a positive integer number of stones piles[i]. The objective of the game is to end with the most stones.

Alice and Bob take turns, with Alice starting first.

On each player's turn, that player can take all the stones in the first X remaining piles, where 1 <= X <= 2M. Then, we set M = max(M, X). Initially, M = 1.

The game continues until all the stones have been taken.

Assuming Alice and Bob play optimally, return the maximum number of stones Alice can get.

Example 1:

Input: piles = [3,1,2,5,7]

Output: 10
Explanation: Alice takes first pile, then Bob takes the second pile, then Alice takes the next two piles and Bob takes the last remaining pile. This makes Alice's score 3 + 2 + 5 = 10, which is the maximum Alice can get.

Example 2:

Input: piles = [4,3,2,5,10]

Output: 11
Constraints:

1 <= piles.length <= 100
1 <= piles[i] <= 10,000

'''

from functools import cache

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        ps = [0]
        for pile in piles:
            ps.append(ps[-1] + pile)

        prefix_sum = lambda l, r: ps[r+1] - ps[l]
        n = len(piles)

        @cache
        def f(i, m, is_alice):
            if i >= n:
                return 0

            res = 0 if is_alice else float("inf")
            for x in range(1, 2*m + 1):
                if i + x - 1 >= n:
                    break

                new_m = max(m, x)
                alice_score_after_move = f(i + x, new_m, is_alice ^ True)
                                
                if is_alice:
                    taken = prefix_sum(i, i + x - 1)
                    res = max(res, taken + alice_score_after_move)
                else:
                    res = min(res, alice_score_after_move)

            return res

        return f(0, 1, True)
