'''
You are given an array of integers temperatures where temperatures[i] represents the daily temperatures on the ith day.

Return an array result where result[i] is the number of days after the ith day before a warmer temperature appears on a future day. If there is no day in the future where a warmer temperature will appear for the ith day, set result[i] to 0 instead.

Example 1:

Input: temperatures = [30,38,30,36,35,40,28]

Output: [1,4,1,2,1,0,0]
Example 2:

Input: temperatures = [22,21,20]

Output: [0,0,0]
Constraints:

1 <= temperatures.length <= 1000.
1 <= temperatures[i] <= 100

Insights: monotonic stack (monotonically decreasing) - next greater element

'''
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        '''
        Finds the number of days until a warmer temperature for each day.
        Uses a monotonically decreasing stack to track temperatures waiting for a warmer day.
        '''
        res = [0] * len(temperatures)  # default to 0 (no warmer day found)
        stack = []  # stores (index, temperature) pairs
        
        for i, temp in enumerate(temperatures):
            # if current temp violates monotonically decreasing stack, keep popping and update results
            while stack and stack[-1][1] < temp:
                prev_i, prev_temp = stack.pop()
                res[prev_i] = i - prev_i  # days until warmer temperature
            
            # add current day to maintain monotonically decreasing stack
            stack.append((i, temp))
        
        # remaining elements in stack have no warmer day (already initialized to 0)
        return res