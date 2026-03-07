'''
You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose any two stones and smash them together. Suppose the stones have weights x and y with x <= y. The result of this smash is:

If x == y, both stones are destroyed, and
If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
At the end of the game, there is at most one stone left.

Return the smallest possible weight of the left stone. If there are no stones left, return 0.

Example 1:

Input: stones = [2,4,1,5,6,3]

Output: 1
Explanation:

We smash 2 and 1 which makes the array [1,4,5,6,3].
We smash 4 and 3 which makes the array [1,1,5,6].
We smash 5 and 6 which makes the array [1,1,1].
We smash 1 and 1 which makes the array [1].
Example 2:

Input: stones = [4,4,1,7,10]

Output: 2
Constraints:

1 <= stones.length <= 30
1 <= stones[i] <= 100
'''
from functools import cache

class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        stoneSum = sum(stones)
        target = stoneSum // 2

        @cache
        def dfs(i, total):
            if total >= target or i == len(stones):
                return abs(total - (stoneSum - total))

            return min(dfs(i + 1, total), dfs(i + 1, total + stones[i]))

        return dfs(0, 0)
