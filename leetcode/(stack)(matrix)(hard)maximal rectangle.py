'''
Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

 

Example 1:


Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 6
Explanation: The maximal rectangle is shown in the above picture.
Example 2:

Input: matrix = [["0"]]
Output: 0
Example 3:

Input: matrix = [["1"]]
Output: 1
 

Constraints:

rows == matrix.length
cols == matrix[i].length
1 <= rows, cols <= 200
matrix[i][j] is '0' or '1'.
'''


from typing import List
class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        R = len(matrix)
        C = len(matrix[0])

        # change everything to ints
        for r in range(R):
            for c in range(C):
                matrix[r][c] = int(matrix[r][c])
        
        # make sure that at each row we make it as a histogram of heights as long as the base is a 1
        for r in range(1, R):
            for c in range(C):
                if matrix[r][c] == 1:
                    matrix[r][c] += matrix[r-1][c]

        # make sure to find the maximal rectangle area row by row
        max_area = 0
        for heights in matrix:
            largest_in_heights = self.largest_rect_area_in_heights(heights)
            max_area = max(max_area, largest_in_heights)

        return max_area

    # the same as the largest rectangle in historgram problem
    def largest_rect_area_in_heights(self, heights: List[int]) -> int:
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