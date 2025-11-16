'''
You are given a a 9 x 9 Sudoku board board. A Sudoku board is valid if the following rules are followed:

Each row must contain the digits 1-9 without duplicates.
Each column must contain the digits 1-9 without duplicates.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without duplicates.
Return true if the Sudoku board is valid, otherwise return false

Note: A board does not need to be full or be solvable to be valid.

Input: board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","8",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]

Output: true

Input: board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","1",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]

Output: false
Explanation: There are two 1's in the top-left 3x3 sub-box.

Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit 1-9 or '.'.

'''

from collections import Counter, defaultdict
from typing import List


class Solution:
    def checkSet(self, s):
        is_partial = "." in s
        print(f"is partial: {is_partial}")
        if not is_partial:
            return len(set(s)) == 9
        else:
            counts = Counter(s)
            for k in counts:
                if k != ".":
                    val = counts[k]
                    if val > 1:
                        return False
            return True

    def checkRow(self, i, board):
        row = board[i]
        print(f"row #{i} => {row}")
        return self.checkSet(row)

    def checkCol(self, j, board):
        col = [row[j] for row in board]
        print(f"col #{j} => {col}")
        return self.checkSet(col)

    def checkBox(self, k, board):
        i, j = divmod(k, 3)
        box = []

        for l in range(3):
            box.extend(board[3 * i + l][3 * j: 3 * (j + 1)])

        print(f"box #{k} => {box}")
        return self.checkSet(box)

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # check all rows
        for i in range(9):
            if not self.checkRow(i, board):
                print(f"row #{i}, not valid!")
                return False

        # check all columns
        for j in range(9):
            if not self.checkCol(j, board):
                print(f"col #{j}, not valid!")
                return False

        # check all boxes
        for k in range(9):
            if not self.checkBox(k, board):
                print(f"box #{k}, not valid!")
                return False

        return True

    def isValidSudoku_neetcode(self, board: List[List[str]]) -> bool:
        cols = defaultdict(set)
        rows = defaultdict(set)
        squares = defaultdict(set)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                if ( board[r][c] in rows[r]
                    or board[r][c] in cols[c]
                    or board[r][c] in squares[(r // 3, c // 3)]):
                    return False

                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                squares[(r // 3, c // 3)].add(board[r][c])

        return True