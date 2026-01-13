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
. need to do binary search solution on the solution space of min y to max y
. keep checking area below the line quickly and do binary search with that

'''
from typing import List
from bisect import *

class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        # create list of (y1, y2)
        self.y_coords = [[y, y + l] for x, y, l in squares]

        # definitely need to sort based on y coor and then length
        self.y_coords.sort(key = lambda y_coord: (y_coord[0], y_coord[1]))

        # get prefix areas
        self.prefix_areas = [(self.y_coords[0][1] - self.y_coords[0][0]) ** 2]

        for i in range(1, len(self.y_coords)):
            area = (self.y_coords[i][1] - self.y_coords[i][0]) ** 2
            self.prefix_areas.append(self.prefix_areas[-1] + area)

        # get total area
        total_area = self.prefix_areas[-1]
        target_area = total_area/2

        # solution lies between min y and max y 
        l = self.y_coords[0][0]
        r = self.y_coords[-1][1]

        while l < r:
            m = (l + r) / 2
            area_below_m = self.area_below(m)
            if area_below_m == target_area:
                r = m
            elif area_below_m > target_area:
                r = m
            else:
                l = m

        return l 

    def area_below(self, y):
        area = 0 
        
        # we can do binary search and find out which squares are below and which are intersected
        # do bisect_left -> i everythin below [:i-1] is included ; but do linear scan to find out which ones it intersects; 
        i = bisect_left(self.y_coords, y, key=lambda y_coord: y_coord[0])
        
        # for intersecting one get the area below 
        intersecting_area = 0
        start = i - 1

        while start >= 0 and self.y_coords[start][0] < y < self.y_coords[start][1]:
            intersecting_area += self.bottom_intersected_area_of_square(self.y_coords[start], y)
            start -= 1 

        # full squares below area
        full_squares_area = self.prefix_areas[start]
        
        area = full_squares_area + intersecting_area
        return area

    # pass (y1, y2), y
    def bottom_intersected_area_of_square(self, square, y):
        y1, y2 = square
        l = abs(y2 - y1)

        if y <= y1:
            return 0

        return abs(y - y1) * l 


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