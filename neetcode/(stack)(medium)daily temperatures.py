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

Insights: monotonic stack

'''
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)

        stack = [(temperatures[0], 0)] # temp, index

        for i in range(1, len(temperatures)):
            temp = temperatures[i]

            if not stack:
                stack.append((temp, i))
                continue

            if stack[-1][0] >= temp:
                stack.append((temp, i))
            else:
                while stack and stack[-1][0] < temp:
                    ele, j = stack.pop()
                    res[j] = i - j
                stack.append((temp, i))

        while stack:
            ele, k = stack.pop()
            res[k] = 0

        return res