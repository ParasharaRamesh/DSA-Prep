'''
Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.



Example 1:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
Example 2:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true
Example 3:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false


Constraints:

m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consists of only lowercase and uppercase English letters.


Follow up: Could you use search pruning to make your solution faster with a larger board?
'''

from typing import List
from collections import deque, defaultdict


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])

        locs = defaultdict(list)

        for i in range(m):
            for j in range(n):
                locs[board[i][j]].append((i,j))

        if not all([(ch in locs) for ch in set(word)]):
            return False

        frontier = deque([(word[0], [loc]) for loc in locs[word[0]]])
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        while frontier:
            s, path = frontier.popleft()

            if word == s:
                return True

            for direction in directions:
                i, j = path[-1]
                di, dj = direction
                ni, nj = i + di, j + dj

                if (0 <= ni < m) and (0 <= nj < n) and (len(s) + 1 <= len(word)) and ((ni, nj) not in set(path)):
                    new = s + board[ni][nj]
                    if word.startswith(new):
                        frontier.append((new, path + [(ni, nj)]))


        return False