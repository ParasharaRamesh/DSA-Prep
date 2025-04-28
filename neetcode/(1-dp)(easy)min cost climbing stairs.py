'''
You are given an array of integers cost where cost[i] is the cost of taking a step from the ith floor of a staircase. After paying the cost, you can step to either the (i + 1)th floor or the (i + 2)th floor.

You may choose to start at the index 0 or the index 1 floor.

Return the minimum cost to reach the top of the staircase, i.e. just past the last index in cost.

Example 1:

Input: cost = [1,2,3]

Output: 2
Explanation: We can start at index = 1 and pay the cost of cost[1] = 2 and take two steps to reach the top. The total cost is 2.

Example 2:

Input: cost = [1,2,1,2,1,1,1]

Output: 4
Explanation: Start at index = 0.

Pay the cost of cost[0] = 1 and take two steps to reach index = 2.
Pay the cost of cost[2] = 1 and take two steps to reach index = 4.
Pay the cost of cost[4] = 1 and take two steps to reach index = 6.
Pay the cost of cost[6] = 1 and take one step to reach the top.
The total cost is 4.
Constraints:

2 <= cost.length <= 100
0 <= cost[i] <= 100
'''
from typing import List


class Solution:
    #top down memoization
    def minCostClimbingStairs_topdown(self, cost: List[int]) -> int:
        cache = dict()
        def climb(i):
            if i in cache:
                return cache[i]

            if i >= len(cost):
                cache[i] = 0
                return 0

            cache[i] = cost[i] + min(climb(i + 1), climb(i + 2))
            return cache[i]

        return min(climb(0), climb(1))

    #bottom up
    def minCostClimbingStairs_bottomup(self, cost: List[int]) -> int:
        cache = dict()

        cache[0] = cost[0]
        def climb(i):
            if i in cache:
                return cache[i]

            if i >= len(cost):
                cache[i] = 0
                return 0

            cache[i] = cost[i] + min(climb(i + 1), climb(i + 2))
            return cache[i]

        return min(climb(0), climb(1))