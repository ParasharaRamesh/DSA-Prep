'''
You are given an integer array heights where heights[i] represents the height of the
ith bar.

You may choose any two bars to form a container. Return the maximum amount of water a container can store.

Example 1:



Input: height = [1,7,2,5,4,7,3,6]

Output: 36
Example 2:

Input: height = [2,2,2]

Output: 4
Constraints:

2 <= height.length <= 1000
0 <= height[i] <= 1000

'''

from typing import *


class Solution:
    '''
    Why this works:
    The area is calculated as min(height[left], height[right]) * (right - left).
    The height of the container is limited by the shorter line.
    
    If height[left] < height[right], the left line is the bottleneck.
    - If we move the right pointer inwards, the width decreases.
    - The height will be min(height[left], height[new_right]). Since height[left] is already the shorter one,
      the new height cannot possibly exceed height[left].
    - So, moving the right pointer (the taller one) guarantees a smaller or equal area (less width, same or less height).
    
    Therefore, to potentially find a larger area, we MUST move the shorter pointer. 
    We don't know if the next line will be taller, but we know that keeping the current shorter line 
    and moving the other side is guaranteed to not give a better result.
    '''
    def maxArea(self, heights: List[int]) -> int:
        start = 0
        end = len(heights) - 1

        ma = 0
        while start < end:
            ma = max(ma, (end - start) * min(heights[start], heights[end]))

            if heights[start] < heights[end]:
                start += 1
            elif heights[start] > heights[end]:
                end -= 1
            else:
                end -= 1

        return ma

    def maxArea_suboptimal(self, heights: List[int]) -> int:
        left = 0
        right = len(heights) - 1

        greatestArea = 0

        while left < right:
            width = right - left

            if heights[left] < heights[right]:
                # get curr area
                height = heights[left]
                currArea = height * width

                # set new area
                greatestArea = max(currArea, greatestArea)

                # move left ptr rightward
                left = self.moveLeftPtr(greatestArea, heights, left, right)
            else:
                # get curr area
                height = heights[right]
                currArea = height * width

                # set new area
                greatestArea = max(currArea, greatestArea)

                # move right ptr leftward
                right = self.moveRightPtr(greatestArea, heights, left, right)

        return greatestArea

    def moveLeftPtr(self, greatestArea, heights, left, right):
        '''
        Move left ptr rightward until heights[left] >= heights[right]
        '''
        i = left + 1
        while i < right:
            width = right - i
            height = heights[i]
            currArea = width * height

            if currArea > greatestArea:
                break
            i += 1

        return i

    def moveRightPtr(self, greatestArea, heights, left, right):
        '''
        Move right ptr leftward until heights[right] >= heights[left]
        '''
        i = right - 1
        while i > left:
            width = i - left
            height = heights[i]
            currArea = width * height

            if currArea > greatestArea:
                break
            i -= 1

        return i


if __name__ == '__main__':
    s = Solution()
    h1 = [1, 8, 6, 2, 5, 4, 8, 3, 7]  # 49
    print(s.maxArea(h1))

    h2 = [1, 1]  # 1
    print(s.maxArea(h2))

    h3 = [1, 2, 4, 3]  # 4
    print(s.maxArea(h3))
