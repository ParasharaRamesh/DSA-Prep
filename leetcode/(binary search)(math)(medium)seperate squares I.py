'''
You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.

Find the minimum y-coordinate value of a horizontal line such that the total area of the squares above the line equals the total area of the squares below the line.

Answers within 10-5 of the actual answer will be accepted.

Note: Squares may overlap. Overlapping areas should be counted multiple times.

 

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

2 solutions:
1.  need to do binary search solution on the solution space of min y to max y
2. Scan line solution:

🧠 Scanline intuition — splitting total area by a horizontal line

. Core idea: Instead of guessing the y-coordinate (binary search), build the area from bottom to top and stop exactly when half the total area is reached.
. Key observations:
    - Each square contributes area only in a vertical interval
        - Square with bottom y and side l contributes width l for all y ∈ [y, y+l)
    - Only y-boundaries matter
        - The area behavior changes only at square start (y) or square end (y+l) (note its L and one i.e. side length)
        - Between two such y-values (checkpoints), the total intersected width is constant
    - Area grows linearly between boundaries (based on the height traversed by the scan line)
        - If active width = W
        - Moving scanline up by Δy adds area = W × Δy
    - This reduces the problem to integration
        - Accumulate area strip by strip
        - Once target area is crossed, solve a simple linear equation

Algorithm outline

For each square:
    Add +side_length at y
    Add -side_length at y + side_length

Sort all y-boundaries

Sweep upward:
    Maintain active_width
    Add area between consecutive y-points

When accumulated area crosses total_area / 2:
    Solve this linear quation:
    target = area_so_far + active_width × (answer_y - previous_y)
    directly for answer_y

Why no binary search?
    - The area function is piecewise linear
    - So when the target is crossed, we compute the answer exactly — no guessing

'''
from typing import List
from bisect import *
from sortedcontainers import *

class Solution:
    # Scan line based solution (way faster than the binary search solution below)
    def separateSquares(self, squares: List[List[int]]) -> float:
        """
        Scanline approach:
        We sweep a horizontal line from bottom to top and keep track of
        how much total square-width is currently intersected by the scanline.
        Area accumulates linearly between consecutive y-checkpoints.
        """

        # events[y] = change in active horizontal width at height y
        # +l when a square starts contributing width
        # -l when a square stops contributing width
        events = SortedDict()

        total_area = 0.0

        # Each square contributes:
        # - area = l * l
        # - width l active in the vertical interval [y, y + l)
        for _, y, l in squares:
            bottom_y = y
            top_y = y + l

            events[bottom_y] = events.get(bottom_y, 0) + l
            events[top_y] = events.get(top_y, 0) - l

            total_area += l * l

        # We want the horizontal line where area below it = half of total area
        target_area = total_area / 2.0

        # Sorted list of all y-coordinates where something changes
        y_points = list(events.keys())

        # Initialize scanline state
        active_width = events[y_points[0]]   # width active just above first y
        previous_y = y_points[0]
        accumulated_area = 0.0

        # Sweep upward through all checkpoint intervals
        for current_y in y_points[1:]:
            vertical_gap = current_y - previous_y

            # Area added in this vertical strip
            # Because of the way scanline works in between the checkpoints the active width doesnt change at all 
            area_in_strip = active_width * vertical_gap

            """
            If adding this strip's area crosses the target,
            then the answer lies somewhere between previous_y and current_y.

            Since active_width is constant in this interval:
                target_area = accumulated_area + active_width * (answer_y - previous_y)
            Solve for answer_y directly.
            """
            if accumulated_area < target_area <= accumulated_area + area_in_strip:
                return previous_y + (target_area - accumulated_area) / active_width

            # Otherwise, safely accumulate and move up
            accumulated_area += area_in_strip

            # Update active width at this y-boundary
            active_width += events[current_y]

            # Move scanline upward
            previous_y = current_y

        # Problem guarantees a solution, so this line should never be reached
        return 0.0

    # my initial binary search solution 
    def separateSquares_binary_search(self, squares: List[List[int]]) -> float:
        # create list of (y1, y2)
        self.y_coords = [[y, y + l] for x, y, l in squares]

        # definitely need to sort based on y coor and then length
        self.y_coords.sort(key = lambda y_coord: (y_coord[0], y_coord[1]))

        # get prefix areas
        total_area = sum([(self.y_coords[i][1] - self.y_coords[i][0]) ** 2 for i in range(len(self.y_coords))])
        target_area = total_area/2

        # solution lies between min y and max y 
        l = self.y_coords[0][0]
        r = max(self.y_coords, key = lambda y_coord: y_coord[1])[1]

        while l < r and abs(l-r) > 1e-5:
            m = (l + r) / 2
            area_below_m = self.area_below(m)
            if area_below_m >= target_area:
                # even if the area below m equals the target we still want to move downward as we want to find the min y where this holds, otherwise we might be slicing the gap between squares when we can go even further below
                r = m
            else:
                l = m

        return (l + r) / 2

    def area_below(self, y):
        area = 0 
        
        # do bisect_left -> i everything in range [:i-1] is included below this line or intersects; but do linear scan to find out which ones it intersects; 
        i = bisect_left(self.y_coords, y, key=lambda y_coord: y_coord[0])
        
        # for intersecting one get the area below 
        start = i - 1

        # keep going below and at every point check if there are any squares being intersected
        while start >= 0:
            if self.y_coords[start][0] < y < self.y_coords[start][1]:
                area += self.bottom_intersected_area_of_square(self.y_coords[start], y)
            else:
                # can include the full area of the square
                area += (self.y_coords[start][1] - self.y_coords[start][0]) ** 2

            start -= 1 

        return area

    # pass (y1, y2), y
    def bottom_intersected_area_of_square(self, y_coords_of_square, y):
        y1, y2 = y_coords_of_square
        l = abs(y2 - y1)

        if y <= y1:
            return 0

        intersected_area = abs(y - y1) * l
        return intersected_area

if __name__ == "__main__":
    s = Solution()

    squares = [[0,0,1],[2,2,1]]
    expected = 1.0
    ans = s.separateSquares(squares)
    assert abs(expected - ans) <= 10**-5, f"{expected=} {ans=}"

    squares = [[0,0,2],[1,1,1]]
    expected = 1.16667
    ans = s.separateSquares(squares)
    assert abs(expected - ans) <= 10**-5, f"{expected=} {ans=}"

    squares = [[8,16,1],[6,15,10]]
    expected = 19.95000
    ans = s.separateSquares(squares)
    assert abs(expected - ans) <= 10**-5, f"{expected=} {ans=}"

