'''
You are given an m x n 2-D integer array matrix and an integer target.

Each row in matrix is sorted in non-decreasing order.
The first integer of every row is greater than the last integer of the previous row.
Return true if target exists within matrix or false otherwise.

Can you write a solution that runs in O(log(m * n)) time?

Insights:

- flatten approach
- one pass approach
- two pass approach

'''
from bisect import *
from functools import reduce
from typing import List


class Solution:
    def searchMatrix_my_soln(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])

        # find row
        i_l, i_r = 0, m - 1

        while i_l < i_r:
            m_i = (i_l + i_r) // 2

            if matrix[m_i][0] == target or matrix[m_i][-1] == target:
                return True
            elif matrix[m_i][0] < target < matrix[m_i][-1]:
                i_l = m_i
                i_r = m_i
            elif target < matrix[m_i][0]:
                i_r = m_i - 1 if m_i >= 1 else m_i
            elif target > matrix[m_i][-1]:
                i_l = m_i + 1 if m_i < m - 1 else m_i

        assert i_l == i_r, "couldnt find row!"
        i = i_l
        row = matrix[i]

        # find column
        j_l = 0
        j_r = n - 1

        while j_l < j_r:
            m_j = (j_l + j_r) // 2

            if matrix[i][m_j] == target:
                return True
            elif matrix[i][m_j] < target:
                j_l = m_j + 1 if m_j < n - 1 else m_j
            else:
                j_r = m_j - 1 if m_j >= 1 else m_j

        return matrix[i][j_l] == target

    def searchMatrix_bs_for_row_then_column(self, matrix: List[List[int]], target: int) -> bool:
        ROWS, COLS = len(matrix), len(matrix[0])

        top, bot = 0, ROWS - 1
        while top <= bot:
            row = (top + bot) // 2
            if target > matrix[row][-1]:
                top = row + 1
            elif target < matrix[row][0]:
                bot = row - 1
            else:
                break

        if not (top <= bot):
            return False
        row = (top + bot) // 2
        l, r = 0, COLS - 1
        while l <= r:
            m = (l + r) // 2
            if target > matrix[row][m]:
                l = m + 1
            elif target < matrix[row][m]:
                r = m - 1
            else:
                return True
        return False
    def searchMatrix_flatten(self, matrix: List[List[int]], target: int) -> bool:
        flattened = []

        for row in matrix:
            flattened.extend(row)

        # print(f"flattened is {flattened}")
        i = bisect(flattened, target)
        return flattened[i - 1] == target

    #one pass most optimal
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        ROWS, COLS = len(matrix), len(matrix[0])

        l, r = 0, ROWS * COLS - 1
        while l <= r:
            m = l + (r - l) // 2
            row, col = m // COLS, m % COLS
            if target > matrix[row][col]:
                l = m + 1
            elif target < matrix[row][col]:
                r = m - 1
            else:
                return True
        return False