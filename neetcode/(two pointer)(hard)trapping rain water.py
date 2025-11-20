'''
You are given an array non-negative integers height which represent an elevation map. 
Each value height[i] represents the height of a bar, which has a width of 1.

Return the maximum area of water that can be trapped between the bars.

General Intuition:
For any bar at index 'i', the amount of water it can hold on top of it is determined by:
    water[i] = min(max_height_to_left, max_height_to_right) - height[i]
If min(max_left, max_right) <= height[i], it cannot hold any water.

We have 3 main approaches to solve this:
1. Precomputation (Dynamic Programming): Store max_left and max_right for every index.
2. Two Pointers: Optimize space by calculating max_left and max_right on the fly.
3. Flood Fill (Heap/BFS): View the problem as water flowing from the outside in, bounded by the shortest wall.
'''

from typing import List
from heapq import *
from collections import deque

class Solution:
    
    def trap_precomputation(self, height: List[int]) -> int:
        '''
        Approach 1: Precomputation (Dynamic Programming)
        
        Why it works:
        The core equation is water[i] = min(max_l[i], max_r[i]) - height[i].
        Instead of searching for the max left and right walls for every single element (which would be O(N^2)),
        we can pre-calculate these values in two passes.
        
        Complexity:
        - Time: O(N) - We iterate through the array 3 times (left pass, right pass, calculation pass).
        - Space: O(N) - We store two extra arrays of size N.
        '''
        if not height:
            # Edge case: Empty input array cannot trap water
            return 0
            
        n = len(height)
        # Initialize arrays to store the maximum height found so far to the left and right of each index
        max_left = [0] * n
        max_right = [0] * n
        
        # 1. Build the max_left array
        # The first element's left max is itself (or 0 if we consider strictly left, but including itself simplifies logic)
        current_max = 0
        for i in range(n):
            # For index i, the maximum height to its left (including itself) is tracked
            current_max = max(current_max, height[i])
            max_left[i] = current_max
            
        # 2. Build the max_right array
        # We iterate backwards from the end of the array
        current_max = 0
        for i in range(n - 1, -1, -1):
            # For index i, the maximum height to its right (including itself) is tracked
            current_max = max(current_max, height[i])
            max_right[i] = current_max
            
        # 3. Calculate trapped water
        total_water = 0
        for i in range(n):
            # The water level at index i is determined by the shorter of the two tallest walls surrounding it
            limiting_height = min(max_left[i], max_right[i])
            
            # The actual water trapped is the limiting height minus the bar's own height
            # If the bar is taller than the limiting height, this term would be 0 (since max_left/right includes height[i])
            water_at_i = limiting_height - height[i]
            
            # Add to total
            total_water += water_at_i
            
        return total_water

    def trap_two_pointers(self, height: List[int]) -> int:
        '''
        Approach 2: Two Pointers
        
        Why it works:
        In the precomputation approach, we realized we need min(max_l, max_r).
        Notice that for any index, we don't actually need to know the EXACT value of the larger wall.
        We only need to know the value of the SMALLER wall because that's the bottleneck.
        
        If max_l < max_r, then min(max_l, max_r) is definitely max_l. It doesn't matter how big max_r is, 
        water level is limited by max_l. So we can process the left side.
        Conversely, if max_r < max_l, we are limited by the right side.
        
        Complexity:
        - Time: O(N) - Single pass from both ends meeting in the middle.
        - Space: O(1) - Only constant extra space used.
        '''
        if not height:
            return 0
            
        # Initialize pointers at both ends of the array
        left, right = 0, len(height) - 1
        
        # Initialize max heights seen so far from left and right
        left_max, right_max = height[left], height[right]
        
        total_water = 0
        
        while left < right:
            # We compare the max heights found so far.
            # The side with the smaller max height is the "bottleneck" or limiting factor.
            if left_max < right_max:
                # Since left_max < right_max, we know that for the current 'left' position,
                # the water level is definitely limited by left_max.
                # (Even if there's a huge wall somewhere between left and right, left_max is still the limit).
                
                # Move left pointer inward
                left += 1
                
                # Update left_max with the new height
                left_max = max(left_max, height[left])
                
                # Calculate water: The max possible water level is left_max.
                # We subtract the current height. If current height is the new max, result is 0.
                total_water += left_max - height[left]
            else:
                # Similarly, if right_max is the smaller (or equal) boundary, it is the limiting factor.
                # We can safely calculate water for the 'right' position.
                
                # Move right pointer inward
                right -= 1
                
                # Update right_max
                right_max = max(right_max, height[right])
                
                # Calculate water
                total_water += right_max - height[right]
                
        return total_water

    def trap_flood_fill(self, height: List[int]) -> int:
        '''
        Approach 3: Flood Fill (using Min-Heap)
        
        Why it works:
        Imagine the array as a 3D terrain. Water will spill out from the lowest boundary.
        We can start from the outer boundaries and move inwards, always processing the lowest wall first.
        This ensures that when we visit a cell, we are approaching it from the lowest possible "leak" point 
        that connects it to the outside world.
        
        This is effectively Dijkstra's algorithm or a Priority-Queue based BFS.
        The "cost" to reach a cell is the height of the boundary we crossed.
        
        Complexity:
        - Time: O(N log N) - Each element is pushed and popped from the heap once.
        - Space: O(N) - To store the visited array and the heap.
        '''
        if not height:
            return 0
            
        n = len(height)
        visited = [False] * n
        
        # Min-heap stores tuples of (height, index)
        # We want to process the shortest walls first
        min_heap = []
        
        # Add the first and last bars to the heap as the initial boundaries
        # These are the "walls" that hold the water in from the sides
        heappush(min_heap, (height[0], 0))
        heappush(min_heap, (height[n-1], n-1))
        visited[0] = True
        visited[n-1] = True
        
        total_water = 0
        # This tracks the maximum height of the wall we have crossed so far to get to the current cell
        # It represents the effective water level for the current region
        max_height_so_far = 0
        
        while min_heap:
            # Get the shortest wall from the boundary
            curr_height, curr_index = heappop(min_heap)
            
            # Update the max height encountered on this path.
            # If we are at a lower height than max_height_so_far, it means we are in a "valley"
            # and can trap water up to max_height_so_far.
            max_height_so_far = max(max_height_so_far, curr_height)
            
            # Check neighbors (left and right)
            neighbors = [curr_index - 1, curr_index + 1]
            
            for neighbor in neighbors:
                # If neighbor is within bounds and not visited
                if 0 <= neighbor < n and not visited[neighbor]:
                    # Mark as visited so we don't process it again
                    visited[neighbor] = True
                    
                    # Calculate water for this neighbor
                    # If the neighbor's height is less than max_height_so_far, it traps water.
                    # If it's taller, max(0, negative) is 0.
                    water = max(0, max_height_so_far - height[neighbor])
                    total_water += water
                    
                    # Add the neighbor to the heap to continue the traversal
                    # We push the neighbor's actual height, not the water level
                    heappush(min_heap, (height[neighbor], neighbor))
                    
        return total_water

if __name__ == '__main__':
    s = Solution()
    test_case = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Test Case: {test_case}")
    print(f"Precomputation: {s.trap_precomputation(test_case)}") # Expected: 6
    print(f"Two Pointers:   {s.trap_two_pointers(test_case)}")   # Expected: 6
    print(f"Flood Fill:     {s.trap_flood_fill(test_case)}")     # Expected: 6
