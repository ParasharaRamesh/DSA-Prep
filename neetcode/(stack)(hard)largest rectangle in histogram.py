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

        # Stack stores tuples: (start_index, height)
        #
        # Meaning of an entry (s, h):
        #   "There is a rectangle of height h that can extend
        #    continuously from index s up to the previous index."
        #
        # IMPORTANT:
        #   The stack is NOT storing raw bars.
        #   It stores "how far left" each height can stretch.
        stack = []

        for i, h in enumerate(heights):

            # By default, assume the current bar starts at i.
            # This may move LEFT if we pop taller bars.
            start = i

            """
            If the current height is smaller than the height on top of the stack,
            then the top rectangle can no longer extend to index i.

            Example:
              heights = [2, 3, 1]
                                ↑
                                i = 2, h = 1

              Stack before processing 1:
                [(0,2), (1,3)]

              Since 3 > 1, rectangle (1,3) must end at i-1 = 1.
            """
            while stack and stack[-1][1] > h:
                prev_start, prev_height = stack.pop()

                """
                . Finalize the area for prev_height.
                . Any area with height having prev_height cannot extend to the left since everything to the left of it is smaller than it, meaning it can only extend to the right up until i-1 (inclusive)

                Example:
                  prev_start = 1, prev_height = 3, i = 2

                  Rectangle:
                    height = 3
                    width  = (2 - 1) = 1
                    area   = 3 * 1
                """
                max_area = max(max_area, prev_height * (i - prev_start))

                """
                THIS IS THE CRITICAL LINE:
                    start = prev_start

                . We do this everytime we pop, and keep updating it

                Why do we do this? (Concrete example)

                Continuing the example:
                  heights = [2, 3, 1]
                               ↑   ↑
                             prev   curr

                . We eventually want to push curr into the stack in the correct increasing order, but where does it start from ? (clearly all the way from index 0 since 2 and 3 also has a height of 1 unit within it)
                We just popped (1,3).
                But notice:
                  - height 2 at index 0
                  - height 3 at index 1

                Both are >= current height 1.

                So the current bar (height = 1) can extend left
                NOT just from index 2,
                but all the way back to index 0.

                If we did NOT do on every pop:
                    start = prev_start

                and instead pushed (2,1), we'd lose the rectangle:
                    height = 1, width = 3

                Correct behavior:
                  start becomes 1, then 0 as we pop more bars.
                """
                start = prev_start

            """
            At this point, either:
              - the stack is empty, OR
              - the top of the stack has height <= current height

            So it is safe to push the current height.

            Example stack states:
              heights = [2, 3, 1]

              After processing 1:
                stack = [(0,1)]
            """
            stack.append((start, h))

        """
        Any entries left in the stack were never blocked by a smaller bar to the right.
        So their rectangles extend until the end of the histogram.

        Example:
          heights = [2, 4, 6]
          stack   = [(0,2), (1,4), (2,6)]

        Each extends to index len(heights).
        """
        n = len(heights)
        for start, h in stack:
            max_area = max(max_area, h * (n - start))

        return max_area


if __name__ == '__main__':
    s = Solution()

    heights = [2, 1, 5, 6, 2, 3]
    res = s.largestRectangleArea(heights)
    print(res, res == 10)

    heights = [2, 4]
    res = s.largestRectangleArea(heights)
    print(res, res == 4)
