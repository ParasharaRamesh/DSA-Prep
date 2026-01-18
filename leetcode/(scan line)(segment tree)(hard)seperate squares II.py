'''
You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.

Find the minimum y-coordinate value of a horizontal line such that the total area of the squares above the line equals the total area of the squares below the line.

Answers within 10-5 of the actual answer will be accepted.

Note: Squares may overlap. Overlapping areas should be counted ONLY ONCE.

 

Example 1:

Input: squares = [[0,0,1],[2,2,1]]

Output: 1.00000

Explanation:



Any horizontal line between y = 1 and y = 2 will have 1 square unit above it and 1 square unit below it. The lowest option is 1.

Example 2:

Input: squares = [[0,0,2],[1,1,1]]

Output: 1.16667

Explanation:



The areas are:

Below the line: 7/6 * 2 (Red) + 1/6 (Blue) = 15/6 = 2.5.
Above the line: 5/6 * 2 (Red) + 5/6 (Blue) = 15/6 = 2.5.
Since the areas above and below the line are equal, the output is 7/6 = 1.16667.

 

Constraints:

1 <= squares.length <= 5 * 10**4
squares[i] = [xi, yi, li]
squares[i].length == 3
0 <= xi, yi <= 10**9
1 <= li <= 10**9
The total area of all the squares will not exceed 10**12.
'''

'''
Thoughts:

. We can still use the same kind of scan line solution from the seperate squares I however calculation of the active width becomes tricky this time around
. Therefore this time, for the events at each y we can keep track of the starting and closing x coordinate and also mention the type as
"OPEN" or "CLOSE"
. Using these events we can calculate the active width at each y coordinate similar to merge interval , while also calculating the new total area of all the intersecting shapes
. Then we can do one final pass using the same idea of the mathematical equation to calculate the correct coordinate
'''

from typing import List
from bisect import *
from sortedcontainers import *

class Solution:
    # all intervals are already sorted just need the total length of the intervals after merging
    def get_active_width(self, intervals):
        if not intervals:
            return 0
        
        if len(intervals) == 1:
            return intervals[0][1] - intervals[0][0]

        prev_start, prev_end = intervals[0]
        first_time = True

        total_width = 0

        for start, end in intervals[1:]:
            if start > prev_end:
                # to add the area of the first interval 
                if first_time:
                    total_width += prev_end - prev_start
                    first_time = False

                # add curr width 
                total_width += end - start
                prev_start, prev_end = start, end
            else:
                # update prev_end to the new merged end
                prev_end = max(prev_end, end)
                total_width += prev_end - prev_start

        return total_width
        

    # Scan line based solution
    def separateSquares(self, squares: List[List[int]]) -> float:
        # sort based on the y coordinate
        squares.sort(key = lambda coord: coord[1])

        # add the events at each y coordinate
        events = SortedList(key = lambda item: item[0])
        for square in squares:
            x, y, l = square
            events.add((y, (x, x + l), "OPEN"))
            events.add((y + l, (x, x + l), "CLOSE"))


        # at each y calculate the active width and keep track of the accumulated area in a list
        total_area = 0
        areas = [] # of type (prev_y, w, h)

        # we will keep track of [(x1, x2),..] => added at each y
        active_widths = SortedList(key = lambda xs: xs[0])

        # for the first one we can just add it to the active width
        prev_y, (x1, x2), event_type = events[0]
        active_widths.add((x1, x2))

        for event in events[1:]:
            curr_y, (x1, x2), event_type = event
           
            # calculate the active width, for the area spanned by the horizontal strip from prev_y -> y
            active_width = self.get_active_width(active_widths)
            active_height = curr_y - prev_y
            active_area = active_width * active_height

            if active_area > 0:
                # keep track of the total area so that we can do one more pass
                total_area += active_area

                # keep track such that at each y, starting from there what is the active width and active height one can expect as we do the scan line
                areas.append((prev_y, active_width, active_height))

            # calculate the active width at this y, by adding this interval or removing it 
            if event_type == "OPEN":
                active_widths.add((x1, x2))
            elif event_type == "CLOSE":
                active_widths.discard((x1, x2))

            # set new prev y
            prev_y = curr_y
            
        # We want the horizontal line where area below it = half of total area
        target_area = total_area / 2
        accumulated_area = 0.0        

        # Sweep upward through the already accumulated areas
        for y, active_width, active_height in areas:
            # Area added in this vertical strip
            # Because of the way scanline works in between the checkpoints the active width doesnt change at all 
            area_in_strip = active_width * active_height

            """
            If adding this strip's area crosses the target,
            then the answer lies somewhere between previous_y and current_y.

            Since active_width is constant in this interval:
                target_area = accumulated_area + active_width * (answer_y - previous_y)
            Solve for answer_y directly.
            """
            if accumulated_area < target_area <= accumulated_area + area_in_strip:
                return y + (target_area - accumulated_area) / active_width

            # Otherwise, safely accumulate and move up
            accumulated_area += area_in_strip

        # Problem guarantees a solution, so this line should never be reached
        return 0.0

if __name__ == "__main__":
    s = Solution()

    squares = [[0,0,1],[2,2,1]]
    expected = 1.0
    ans = s.separateSquares(squares)
    assert abs(expected - ans) <= 10**-5, f"{expected=} {ans=}"

    squares = [[0,0,2],[1,1,1]]
    expected = 1.0
    ans = s.separateSquares(squares)
    assert abs(expected - ans) <= 10**-5, f"{expected=} {ans=}"

