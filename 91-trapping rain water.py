'''

You are given an array non-negative integers height which represent an elevation map. Each value height[i] represents the height of a bar, which has a width of 1.

Return the maximum area of water that can be trapped between the bars.

intution:

at each height: you can trap water only if the max heights to its left & right (max_l, max_r) are both greater than curr_height. then it is min(max_l, max_r)

how to build this  is the main question

'''
from typing import List
from heapq import *
from collections import deque


class Solution:
    def get_left_right(self, height):
        left = deque([0])
        right = deque([0])
        max_l, max_r = height[0], height[-1]

        # build left array
        for h in height[1:]:
            left.append(max_l)
            max_l = max(max_l, h)

        # build right array
        for h in reversed(height[:-1]):
            right.appendleft(max_r)
            max_r = max(max_r, h)

        return list(left), list(right)

    # with left and right preprocessed arrays
    def trap_lr(self, height: List[int]) -> int:
        left, right = self.get_left_right(height)
        print(f"left is {left}, right is {right}")

        total = 0
        for i, h in enumerate(height):
            max_l = left[i]
            max_r = right[i]

            print(f"at i:{i}, height is {h}, left is {max_l}, right is {max_r}, total now is {total}")
            if (max_l > h) and (max_r > h):
                total += min(max_l, max_r) - h
                print(f"-> contributes {min(max_l, max_r)}")
            else:
                print(f" -> no contribution!")
        return total

    # 2 pointers
    def trap_2_pointers(self, height: List[int]) -> int:
        '''
        Core idea here is that it is similar to flood fill algorithm, water always moves from lower to higher levels from both ends

        If we know that the left boundary is lesser than right boundary, we dont care about any other max_right in the unexplored middle region which could have been lesser than left!
        this is because, if at all there was then that would have been processed when coming from the other side as the right boundary should have been smaller initially to let the water flood in, in which case we would have accounted for it in the other end.

        so when left boundary is lesser than right, we move left pointer and vice versa
        '''

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]

        total = 0
        while left <= right:
            if left_max < right_max:
                total += max(left_max, height[left]) - height[left]
                left_max = max(left_max, height[left])
                # print(f"at left-> {left}, contribution is {max(left_max, height[left]) - height[left]}, total is now {total}, left_max is {left_max}")
                left += 1
            else:
                total += max(right_max, height[right]) - height[right]
                right_max = max(right_max, height[right])
                # print(f"at right-> {right}, contribution is {max(right_max, height[right]) - height[right]}, total is now {total}, right_max is {right_max}")
                right -= 1

        return total

    # flood fill using heaps
    def trap(self, height: List[int]) -> int:
        left_wall, right_wall = height[0], height[-1]
        curr_level = min(left_wall, right_wall) # curr level of water

        water_heap = [(left_wall, 0), (right_wall, len(height) - 1)] # (height, index)
        heapify(water_heap)

        visited = [False] * len(height)
        total = 0

        while water_heap:
            curr_min_wall_height, i = heappop(water_heap)

            # if the curr_level of water is greater than the wall height then it can store something, no point in checking max on the other side, water moves floods in only after rising level by level, if something smaller was there on the other side, the other end would have been processed first!
            total += max(curr_level, curr_min_wall_height) - curr_min_wall_height
            visited[i] = True
            curr_level = max(curr_level, curr_min_wall_height)

            neighbours = [i - 1, i + 1]
            for neighbour_ind in neighbours:
                if (0 <= neighbour_ind < len(height)) and (not visited[neighbour_ind]):
                    heappush(water_heap, (height[neighbour_ind], neighbour_ind))

        return total

if __name__ == '__main__':
    s = Solution()
    print(s.trap([0, 2, 0, 3, 1, 0, 1, 3, 2, 1]))  # 9
