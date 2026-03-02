'''
Given an n x n binary grid, in one step you can choose two adjacent rows of the grid and swap them.

A grid is said to be valid if all the cells above the main diagonal are zeros.

Return the minimum number of steps needed to make the grid valid, or -1 if the grid cannot be valid.

The main diagonal of a grid is the diagonal that starts at cell (1, 1) and ends at cell (n, n).

 

Example 1:


Input: grid = [[0,0,1],[1,1,0],[1,0,0]]
Output: 3
Example 2:


Input: grid = [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]]
Output: -1
Explanation: All rows are similar, swaps have no effect on the grid.
Example 3:


Input: grid = [[1,0,0],[1,1,0],[1,1,1]]
Output: 0
 

Constraints:

n == grid.length == grid[i].length
1 <= n <= 200
grid[i][j] is either 0 or 1

'''
from typing import List
from collections import *
from copy import deepcopy

# Tried a standard BFS approach but it was TLE
class Solution_TLE_BFS:
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)

        start = []

        for row in grid:
            row = list(map(lambda num: str(num), row))
            row = "".join(row)
            start.append(row)

        start = tuple(start)
        frontier = deque(
            [
                (
                    start,
                    0
                )
            ]
        )

        visited = set()
        visited.add(start)

        while frontier:
            state, d = frontier.popleft()

            if self.is_valid(state):
                return d

            #return all tuples
            neighbours = self.get_neighbours(state)

            for neigh in neighbours:
                if neigh not in visited:
                    visited.add(neigh)
                    frontier.append((neigh, d+1))

        return -1

    def is_valid(self, state):
        for i, row in enumerate(state):
            elems = row[i+1:]

            if len(elems) != elems.count("0"):
                return False
        
        return True

    def get_neighbours(self, state):
        neighbours = []

        state = list(state)

        for i in range(len(state) - 1):
            copy = deepcopy(state)
            copy[i], copy[i+1] = copy[i+1], copy[i]
            neighbours.append(tuple(copy))

        return neighbours

# Tried the same BFS approach but optimzied the entire thing with bit manipulation since all of the states are binary strings
class Solution_TLE_BFS_Binary_optimized:
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)

        start = ""

        for row in grid:
            row = list(map(lambda num: str(num), row))
            row = "".join(row)
            start += row

        # convert to int
        start = int(start,2)
        frontier = deque([(start,0)])

        visited = set()
        visited.add(start)

        while frontier:
            state, d = frontier.popleft()

            if self.is_valid(state, n):
                return d

            #return all tuples
            neighbours = self.get_neighbours(state, n)

            for neigh in neighbours:
                if neigh not in visited:
                    visited.add(neigh)
                    frontier.append((neigh, d+1))

        return -1

    def is_valid(self, state, n):
        mask = (1 << n) - 1
        suffix_mask = 0

        for i in range(n):
            elems = (state & mask) >> (n*i)
            
            # should have i number of 0s as suffix
            if elems & suffix_mask != 0:
                return False

            # move mask 
            mask <<= n

            suffix_mask <<= 1
            suffix_mask |= 1
        
        return True

    def get_neighbours(self, state, n):
        neighbours = []

        for i in range(n - 1):
            copy = state

            # extract row i
            row_mask = ((1 << n) - 1) << (n * i)
            elem_i = (copy & row_mask) >> (n * i)

            # extract row i+1
            row_mask_next = ((1 << n) - 1) << (n * (i + 1))
            elem_i_1 = (copy & row_mask_next) >> (n * (i + 1))

            # clear rows i and i+1
            clear_mask = ~(((1 << (2*n)) - 1) << (n * i))
            copy &= clear_mask

            # insert swapped rows
            swapped = (elem_i << n) | elem_i_1
            copy |= (swapped << (n * i))

            neighbours.append(copy)

        return neighbours

'''
This problem is NOT about reachability of a specific target state.
It is about placing rows greedily under monotonic constraints.

Although each BFS step only swaps adjacent rows, the set of reachable
states is the set of all permutations of rows.

The number of such permutations is n! (factorial growth).

Bit manipulation only reduces constant factors, not the size of the
state space. Therefore BFS necessarily explores an exponential number
of states and will always TLE for n up to 200.

The correct solution exploits the monotonic nature of the diagonal
constraint: once a row is valid at position i, it will remain valid
for all positions below i. This allows a greedy placement strategy
that minimizes the number of adjacent swaps.

Basically this is almost like a bubble sort problem where we try to place the row in the correct position and calculate how many swaps are needed to do so along the way!
'''

class Solution:
    def minSwaps(self, grid):
        '''
        Example input used throughout this walkthrough:

        grid = [
            [0, 0, 1],
            [1, 1, 0],
            [1, 0, 0]
        ]
        '''

        '''
        n is the grid dimension
        Example: n = 3
        '''
        n = len(grid)

        '''
        tz[i] stores the number of trailing zeros in row i.

        For the example:
        Row 0 -> [0,0,1] -> 0 trailing zeros
        Row 1 -> [1,1,0] -> 1 trailing zero
        Row 2 -> [1,0,0] -> 2 trailing zeros

        So initially:
        tz = [0, 1, 2]
        '''
        tz = []

        for row in grid:
            count = 0
            for x in reversed(row):
                if x == 0:
                    count += 1
                else:
                    break
            tz.append(count)

        '''
        swaps counts total adjacent swaps performed.

        Example:
        swaps = 0 initially
        '''
        swaps = 0

        '''
        We now place rows greedily from top to bottom.
        '''
        for i in range(n):
            '''
            For position i, we need at least (n - i - 1) trailing zeros.

            Example:
            i = 0 -> needed = 2
            i = 1 -> needed = 1
            i = 2 -> needed = 0
            '''
            needed = n - i - 1

            '''
            We scan downward to find the nearest row j >= i
            such that tz[j] >= needed.

            Because rows with tz[j] > needed are also valid not just exactly the ones where tz[j] == needed.
            '''
            j = i
            while j < n and tz[j] < needed:
                j += 1

            '''
            If j == n, no valid row exists and the answer is -1.
            '''
            if j == n:
                return -1

            '''
            Example walkthrough:

            --- When i = 0 ---
            tz = [0, 1, 2]
            needed = 2

            j scans:
            j = 0 -> tz[0] = 0 < 2
            j = 1 -> tz[1] = 1 < 2
            j = 2 -> tz[2] = 2 >= 2 (valid)

            So j = 2
            '''

            '''
            To bring row j up to position i, we need (j - i) swaps.

            Example:
            swaps += 2 - 0 = 2
            swaps = 2
            '''
            swaps += j - i

            '''
            We simulate those swaps by moving tz[j] to index i.

            Example after moving row j = 2 to i = 0:
            tz was: [0, 1, 2]
            tz becomes: [2, 0, 1]
            '''
            tz.insert(i, tz.pop(j))

            '''
            --- When i = 1 ---
            tz = [2, 0, 1]
            needed = 1

            j scans:
            j = 1 -> tz[1] = 0 < 1
            j = 2 -> tz[2] = 1 >= 1 (valid)

            swaps += 2 - 1 = 1
            swaps = 3

            tz becomes: [2, 1, 0]
            '''

            '''
            --- When i = 2 ---
            tz = [2, 1, 0]
            needed = 0

            tz[2] = 0 >= 0 (valid)
            swaps += 0
            tz unchanged
            '''

        '''
        Final state for the example:
        tz = [2, 1, 0]
        swaps = 3

        This corresponds to a valid grid configuration.
        '''
        return swaps