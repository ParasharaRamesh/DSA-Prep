'''
Alice and Bob are playing a game with piles of stones. There are an even number of piles arranged in a row, and each pile has a positive integer number of stones piles[i].

The objective of the game is to end with the most stones. The total number of stones across all the piles is odd, so there are no ties.

Alice and Bob take turns, with Alice starting first. Each turn, a player takes the entire pile of stones either from the beginning or from the end of the row. This continues until there are no more piles left, at which point the person with the most stones wins.

Assuming Alice and Bob play optimally, return true if Alice wins the game, or false if Bob wins.

Example 1:

Input: piles = [1,2,3,1]

Output: true
Explanation: Alice takes first pile, then Bob takes the last pile, then Alice takes the pile from the end and Bob takes the last remaining pile. Alice's score is 1 + 3 = 4. Bob's score is 1 + 2 = 3.

Example 2:

Input: piles = [2,1]

Output: true
Constraints:

2 <= piles.length <= 500
piles.length is even.
1 <= piles[i] <= 500
sum(piles[i]) is odd.

'''
from functools import cache

class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        @cache
        def dfs(l, r):
            if l > r:
                return 0
            even = (r - l + 1) % 2 == 0
            left = piles[l] if even else 0
            right = piles[r] if even else 0
            return max(dfs(l + 1, r) + left, dfs(l, r - 1) + right)

        total = sum(piles)
        alice_score = dfs(0, len(piles) - 1)
        return alice_score > total - alice_score

    # another solution is to just return True
