'''
There are n gas stations along a circular route. You are given two integer arrays gas and cost where:

gas[i] is the amount of gas at the ith station.
cost[i] is the amount of gas needed to travel from the ith station to the (i + 1)th station. (The last station is connected to the first station)
You have a car that can store an unlimited amount of gas, but you begin the journey with an empty tank at one of the gas stations.

Return the starting gas station's index such that you can travel around the circuit once in the clockwise direction. If it's impossible, then return -1.

It's guaranteed that at most one solution exists.

Example 1:

Input: gas = [1,2,3,4], cost = [2,2,4,1]

Output: 3
Explanation: Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
Travel to station 0. Your tank = 4 - 1 + 1 = 3
Travel to station 1. Your tank = 3 - 2 + 2 = 3
Travel to station 2. Your tank = 3 - 2 + 3 = 4
Travel to station 3. Your tank = 2 - 4 + 4 = 2

Example 2:

Input: gas = [1,2,3], cost = [2,3,2]

Output: -1
Explanation:
You can't start at station 0 or 1, since there isn't enough gas to travel to the next station.
If you start at station 2, you can move to station 0, and then station 1.
At station 1 your tank = 0 + 3 - 2 + 1 - 2 = 0.
You're stuck at station 1, so you can't travel around the circuit.

Constraints:

1 <= gas.length == cost.length <= 1000
0 <= gas[i], cost[i] <= 1000
'''
from typing import List

'''
NON-TRIVIAL EXAMPLE TRACE:
gas  = [2, 1, 1, 10, 1]
cost = [1, 2, 3, 1, 4]
Total Gas = 15, Total Cost = 11 (Sum check: 15 >= 11, so a solution MUST exist)

Iteration Trace:
1. i=0: g=2, c=1. delta = +1. total_delta = 1. index = 0.
   (Car has 1 unit of gas after reaching station 1)
2. i=1: g=1, c=2. delta = -1. total_delta = 1 + (-1) = 0. index = 0.
   (Car has 0 units of gas after reaching station 2)
3. i=2: g=1, c=3. delta = -2. total_delta = 0 + (-2) = -2. 
   *** FAILS at i=2 ***
   Action: Reset total_delta = 0, set index = i + 1 = 3.
   Crucial Logic: We skip indices 1 and 2 because we reached station 1 with surplus 
   gas (+1) and still failed at station 2. Starting at 1 or 2 with 0 gas 
   would fail even worse!
4. i=3: g=10, c=1. delta = +9. total_delta = 9. index = 3.
5. i=4: g=1, c=4. delta = -3. total_delta = 9 + (-3) = 6. index = 3.

Loop ends. Return index 3.
'''


class Solution:
    '''
    . Brute force is n^2 , start from all indices and go around
    . In case sum(gas) < sum(cost) -> then it is not possible -> return -1
    . Else, it is definitely possible:
        - start with index 0 and move forward as much as possible until the total_diff < 0.
        - in which case reset the total_diff and move the possible index to i + 1.
        - Why can we skip all indices between the current start and i?
          Intuition: If we start at station A and get stuck at station B, then any station K
          between A and B (A < K <= B) also cannot be a starting station.
          Reason: We reached K from A with some gas surplus (>=0).
          If we couldn't reach B with that extra surplus, we definitely won't reach it starting from K with 0 gas.
    '''
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # Sigma(gi - ci) < 0 => Sigma(gi) < Sigma(ci)
        if sum(gas) < sum(cost):
            return -1

        # find the first index from where things are fine. if not reset
        total_delta = 0
        index = 0
        for i, item in enumerate(zip(gas, cost)):
            g, c = item
            total_delta += g - c

            # If total_delta < 0, it means we cannot reach station i+1 starting from 'index'.
            # Based on the greedy property, any station from 'index' to 'i' cannot be the 
            # starting station either.
            # Example: 
            # gas  = [1, 2, 5, 1, 1]
            # cost = [2, 2, 1, 1, 1]
            # i=0: delta = 1-2 = -1 (Fail). index becomes 1.
            # i=1: delta = 2-2 = 0.
            # i=2: delta = 0 + (5-1) = 4.
            # ... and so on.
            if total_delta < 0:
                total_delta = 0
                index = i + 1

        # We don't need to check the wrap-around (circular part) because:
        # 1. We already checked if sum(gas) >= sum(cost).
        # 2. If a solution exists, this greedy approach is guaranteed to find the start of it.
        # 3. If we finished the loop and total_delta >= 0, the 'index' found is the valid start.
        return index



if __name__ == '__main__':
    s = Solution()

    gas = [5, 8, 2, 8]
    cost = [6, 5, 6, 6]
    expected = 3
    ans = s.canCompleteCircuit(gas, cost)
    assert ans == expected, f"{expected = }, {ans = }"

    gas = [4, 1, 2, 3]
    cost = [1, 2, 2, 4]
    expected = 0
    ans = s.canCompleteCircuit(gas, cost)
    assert ans == expected, f"{expected = }, {ans = }"

    gas = [3, 4, 1, 2]
    cost = [4, 1, 2, 2]
    expected = 1
    ans = s.canCompleteCircuit(gas, cost)
    assert ans == expected, f"{expected = }, {ans = }"

    gas = [1, 2, 3, 4]
    cost = [2, 2, 4, 1]
    expected = 3
    ans = s.canCompleteCircuit(gas, cost)
    assert ans == expected, f"{expected = }, {ans = }"

    gas = [1, 2, 3]
    cost = [2, 3, 2]
    expected = -1
    ans = s.canCompleteCircuit(gas, cost)
    assert ans == expected, f"{expected = }, {ans = }"
