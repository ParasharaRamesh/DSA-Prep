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


class Solution:
    '''
    . Brute force is n^2 , start from all indices and go around
    . In case sum(gas) < sum(cost) -> then it is not possible -> return -1
    . Else, it is definitely possible:
        - start with index 0 and move forward as much as possible until the total_diff < 0.
        - in which case reset the total_diff and move the possible index to i + 1

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
            if total_delta < 0:
                total_delta = 0
                index = i + 1

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
