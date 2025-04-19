'''
You are given a 2-D matrix board containing 'X' and 'O' characters.

If a continous, four-directionally connected group of 'O's is surrounded by 'X's, it is considered to be surrounded.

Change all surrounded regions of 'O's to 'X's and do so in-place by modifying the input board.

Example 1:



Input: board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","O","O","X"],
  ["X","X","X","O"]
]

Output: [
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","O"]
]
Explanation: Note that regions that are on the border are not considered surrounded regions.

Constraints:

1 <= board.length, board[i].length <= 200
board[i][j] is 'X' or 'O'.

'''
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        m = len(board)
        n = len(board[0])

        # Find all Os
        all_o = set()

        for i in range(m):
            for j in range(n):
                if board[i][j] == "O":
                    all_o.add((i, j))

        ''' keep another set for visited Os but add it only if it is not in the boundaries.
            add (i,j) but the moment something is in the edge remove everything from this set as they shouldnt be changed
        '''
        frontier = set()
        if len(all_o) > 0:
            frontier.add(list(all_o)[0])

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        regions = dict()  # region_id -> [is_boundary, set()]

        region_id = 0
        while all_o:
            while frontier:
                oi, oj = frontier.pop()
                all_o.discard((oi, oj))

                if region_id not in regions:
                    regions[region_id] = {"is_boundary_region": False, "locs": set()}

                # check if boundary, then clear all changes, else add to changes
                is_boundary = (oi == 0) or (oi == m - 1) or (oj == 0) or (oj == n - 1)
                regions[region_id]["locs"].add((oi, oj))
                if is_boundary:
                    regions[region_id]["is_boundary_region"] = True

                for direction in directions:
                    di, dj = direction
                    ni, nj = oi + di, oj + dj

                    # check if already popped from all_o and also check if O and inside board (despite boundary)
                    is_valid_pos = (0 <= ni < m) and (0 <= nj < n)

                    is_o = is_valid_pos and board[ni][nj] == "O"
                    is_still_present = (ni, nj) in all_o
                    already_in_frontier = (ni, nj) in frontier

                    if is_o and is_still_present and not already_in_frontier:
                        frontier.add((ni, nj))

            region_id += 1

            # new frontier
            if len(all_o) > 0:
                frontier.add(list(all_o)[0])

        # change all of the O's to X's (for that group) ?
        for region_id in regions:
            if not regions[region_id]["is_boundary_region"]:
                for loc in regions[region_id]["locs"]:
                    i, j = loc
                    board[i][j] = "X"