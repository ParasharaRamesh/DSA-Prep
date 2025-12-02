'''
The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.



Example 1:


Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above
Example 2:

Input: n = 1
Output: [["Q"]]


Constraints:

1 <= n <= 9
'''
from typing import List
from collections import defaultdict
from copy import deepcopy

class Solution:
    # my old approach very ugly
    def solveNQueens(self, n: int) -> List[List[str]]:
        res = set()
        board = [["."] * n for i in range(n)]

        res = list(self.try_placing(0, board, res, 0))
        res = list(map(lambda x: list(x),res))
        return [["".join(row) for row in board] for board in res]

    #also check partial boards
    def is_valid_board(self, board, num_q) -> bool:
        n = len(board)

        q_positions = []

        diagonals = defaultdict(list)
        other_diagonals = defaultdict(list)

        for i in range(n):
            for j in range(n):
                char = board[i][j]

                diagonals[j-i].append(char)
                other_diagonals[i+j].append(char)

                if char == 'Q':
                    q_positions.append((i, j))

        if len(q_positions) != num_q:
            return False
        elif num_q == 0:
            return True

        for pos in q_positions:
            r, c = pos

            # check that row 'r'
            row = board[r]
            row_count = row.count('Q')
            if row_count > 1:
                return False

            # check that col 'c'
            col = ''
            for board_row in board:
                col += board_row[c]

            col_count = col.count('Q')
            if col_count > 1:
                return False

            # check primary diagonal
            diag = diagonals[c-r]
            dig_count = diag.count('Q')
            if dig_count > 1:
                return False

            #check other diagonal
            other_diag = other_diagonals[c+r]
            other_dig_count = other_diag.count('Q')
            if other_dig_count > 1:
                return False

        return True

    def try_placing(self, row, board, res, num_placed):
        if row == len(board) and self.is_valid_board(board, len(board)):
            board_copy = deepcopy(board)
            board_copy = tuple(map(lambda x: tuple(x), board_copy))
            res.add(board_copy)
            return res
        elif not self.is_valid_board(board, num_placed) or row == len(board):
            return res

        # try to place it in the jth column of that "row" and proceed from there.
        for j in range(len(board)):
            if board[row][j] == ".":
                #placed it
                board[row][j] = "Q"

                #go down the recursion hierarchy
                res = self.try_placing(row + 1, board, res, num_placed + 1)

                #remove it if it wasnt valid
                board[row][j] = "."

        return res

class NeetcodeSolution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col = set()
        posDiag = set()
        negDiag = set()

        res = []
        board = [["."] * n for i in range(n)]

        def backtrack(r):
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res

if __name__ == '__main__':
    s = Solution()
    n = NeetcodeSolution()
    print(s.solveNQueens(4))
    print(n.solveNQueens(4))