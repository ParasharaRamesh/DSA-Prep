'''
You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.

Find the minimum y-coordinate value of a horizontal line such that the total area covered by squares above the line equals the total area covered by squares below the line.

Answers within 10-5 of the actual answer will be accepted.

Note: Squares may overlap. Overlapping areas should be counted only once in this version.

 

Example 1:

Input: squares = [[0,0,1],[2,2,1]]

Output: 1.00000

Explanation:



Any horizontal line between y = 1 and y = 2 results in an equal split, with 1 square unit above and 1 square unit below. The minimum y-value is 1.

Example 2:

Input: squares = [[0,0,2],[1,1,1]]

Output: 1.00000

Explanation:



Since the blue square overlaps with the red square, it will not be counted again. Thus, the line y = 1 splits the squares into two equal parts.

 

Constraints:

1 <= squares.length <= 5 * 104
squares[i] = [xi, yi, li]
squares[i].length == 3
0 <= xi, yi <= 109
1 <= li <= 109
The total area of all the squares will not exceed 1015.
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
    def get_active_width_tle(self, intervals):
        if not intervals:
            return 0
        
        total_width = 0
        
        # Initialize with the first interval
        # We process all intervals in the loop. The first one will just merge with itself (no-op)
        # but it sets up the initial state correctly.
        curr_start, curr_end = intervals[0]
        
        for start, end in intervals:
            if start >= curr_end:
                # Disjoint interval found. Add the previous accumulated width.
                total_width += curr_end - curr_start
                curr_start, curr_end = start, end
            else:
                # Overlapping interval. Extend the current end if needed.
                curr_end = max(curr_end, end)
        
        # Add the last interval
        total_width += curr_end - curr_start
        return total_width

    # Scan line based solution TLE :(
    def separateSquares_tle(self, squares: List[List[int]]) -> float:
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
            active_width = self.get_active_width_tle(active_widths)
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

    # using segment tree approach
    def separateSquares(self, squares: List[List[int]]) -> float:
        # sort based on the y coordinate
        squares.sort(key = lambda coord: coord[1])

        # Collect all x-coordinates
        xs = set()
        for x, _, l in squares:
            xs.add(x)
            xs.add(x + l)

        xs = list(sorted(xs))

        # the leaves of the segment tree are the x coordinates [x[i], x[i+1])
        x_index = {x: i for i, x in enumerate(xs)}

        # add the events at each y coordinate
        events = []
        for square in squares:
            x, y, l = square

            # these indices will help us add to the segment tree
            segment_start_ind = x_index[x]
            segment_end_ind = x_index[x + l]

            # 1 -> OPEN , -1 -> CLOSE
            events.append((y, segment_start_ind, segment_end_ind, 1))
            events.append((y + l, segment_start_ind, segment_end_ind, -1))

        events.sort(key=lambda event: event[0])

        # at each y calculate the active width and keep track of the accumulated area in a list
        st = SegmentTree(xs)

        total_area = 0
        areas = [] # of type (prev_y, w, h)

        # for the first one we can just add it to the segment tree
        prev_y, l1, l2, delta = events[0]
        st.update(l1, l2, delta)

        for curr_y, l1, l2, delta in events[1:]:
            active_width = st.get_active_width()
            active_height = curr_y - prev_y
            active_area = active_width * active_height

            if active_area > 0:
                # keep track of the total area so that we can do one more pass
                total_area += active_area

                # keep track such that at each y, starting from there what is the active width and active height one can expect as we do the scan line
                areas.append((prev_y, active_width, active_height))

            # based on OPEN or CLOSE update the segment tree for this curr_y
            st.update(l1, l2, delta)
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
        

class Node:
    def __init__(self, left, right):
        self.left = left          # index in xs
        self.right = right        # index in xs
        self.count = 0            # coverage count of this entire range left -> right
        self.covered_len = 0      # actual covered x-length
        self.left_child = None
        self.right_child = None

# NOTE: all the l , r , left , right represent indexes of the x coordinates and not the x coordinates themselves
class SegmentTree:
    def __init__(self, xs):
        """
        xs: sorted list of unique x-coordinates
        Leaves represent intervals [xs[i], xs[i+1])
        """
        self.xs = xs
        self.root = self._build(0, len(xs) - 1) # there are len(xs) - 1 intervals and the right is not inclusive!
    
    def _build(self, left, right):
        """
        Build a static segment tree over x-index range [left, right)
        """
        node = Node(left, right)

        if right - left == 1:
            # Leaf node: atomic x-interval based on x_index map
            return node

        mid = (left + right) // 2
        node.left_child = self._build(left, mid)
        node.right_child = self._build(mid, right)
        return node

    def get_active_width(self):
        """
        Return total active x-length at current scanline y
        """
        return self.root.covered_len

    def update(self, l, r, delta):
        """
        Public update method:
        add delta (+1 or -1) to coverage count over index range [l, r)
        """
        self._update(self.root, l, r, delta)

    def _update(self, node, l, r, delta):
        # No overlap
        if node.right <= l or node.left >= r:
            return

        # Fully covered
        if l <= node.left and node.right <= r:
            node.count += delta
            self.update_node(node)
            return

        # Partial overlap
        self._update(node.left_child, l, r, delta)
        self._update(node.right_child, l, r, delta)
        self.update_node(node)

    def update_node(self, node):
        """
        Recompute node.covered_len based on:
        1. node.count (authoritative coverage)
        2. children's covered lengths (if no authority)
        """
        # Case 1: This interval is fully covered by >=1 active square
        if node.count > 0:
            node.covered_len = self.xs[node.right] - self.xs[node.left]
            return

        # Case 2: No square fully covers this interval
        if node.right - node.left == 1:
            # Leaf node: no children, no coverage
            node.covered_len = 0
        else:
            # We must rely on children (if any)
            node.covered_len = (
                node.left_child.covered_len +
                node.right_child.covered_len
            )



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

