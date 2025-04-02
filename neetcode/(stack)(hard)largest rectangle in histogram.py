'''
You are given an array of integers heights where heights[i] represents the height of a bar. The width of each bar is 1.

Return the area of the largest rectangle that can be formed among the bars.

Note: This chart is known as a histogram.

Example 1:

Input: heights = [7,1,7,2,2,4]

Output: 8
Example 2:

Input: heights = [1,3,7]

Output: 7
Constraints:

1 <= heights.length <= 1000.
0 <= heights[i] <= 1000

Insights:

- for each height try to find the left and right most boundaries such that this height can be included
- some kind of preprocessing is needed and then we can do h * (r - l + 1) and find the max in O(n)
preprocess logic
- as long as its greater than curr keep incrementing
- TLE solution did preprocessing n^2 need to reduce that

Optimal:

- Use monotonic increasing stack where you store indices also so that way we know we can keep increasing the heights as far as possible
- the moment we see something lower ,we pop as much as possible and compute the area of that popped region
- in the end we are still left with heights in the stack which is in increasing order of heights so just compute the areas there


'''
from typing import List
from collections import deque


class Solution:

    # TLE O(n2)
    def preprocess(self, heights):
        left = []
        right = []

        for i in range(len(heights)):
            curr = heights[i]

            # left
            l = i
            while l >= 0 and heights[l] >= curr:
                l -= 1
            left.append(l + 1)

            # right
            r = i
            while r < len(heights) and heights[r] >= curr:
                r += 1
            right.append(r - 1)

        return left, right

    def largestRectangleArea_tle(self, heights: List[int]) -> int:
        left, right = self.preprocess(heights)
        max_area = 0

        for i, h in enumerate(heights):
            area = h * (right[i] - left[i] + 1)
            max_area = max(max_area, area)

        return max_area

    # optimal
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        stack = []

        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                p_i, p_h = stack.pop()
                max_area = max(max_area, p_h * (i - p_i))
                start = p_i
            stack.append((start, h))


        for i, h in stack:
            max_area = max(max_area, h * (len(heights) - i))

        return max_area


if __name__ == '__main__':
    s = Solution()

    heights = [2, 1, 5, 6, 2, 3]
    res = s.largestRectangleArea(heights)
    print(res, res == 10)

    heights = [2, 4]
    res = s.largestRectangleArea(heights)
    print(res, res == 4)
