'''
Given an m x n matrix of integers matrix, if an element is 0, set its entire row and column to 0's.

You must update the matrix in-place.

Follow up: Could you solve it using O(1) space?

Example 1:



Input: matrix = [
  [0,1],
  [1,0]
]

Output: [
  [0,0],
  [0,0]
]
Example 2:



Input: matrix = [
  [1,2,3],
  [4,0,5],
  [6,7,8]
]

Output: [
  [1,0,3],
  [0,0,0],
  [6,0,8]
]
Constraints:

1 <= matrix.length, matrix[0].length <= 100
-2^31 <= matrix[i][j] <= (2^31) - 1

'''


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        rows = len(matrix)
        cols = len(matrix[0])

        first_row_has_zero = False
        first_col_has_zero = False

        # check if the first row contains zero
        for c in range(cols):
            if matrix[0][c] == 0:
                first_row_has_zero = True
                break

        # check if the first column contains zero
        for r in range(rows):
            if matrix[r][0] == 0:
                first_col_has_zero = True
                break

        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # set the marked rows to zero
        for r in range(1, rows):
            if matrix[r][0] == 0:
                for c in range(1, cols):
                    matrix[r][c] = 0

        # set the marked columns to zero
        for c in range(1, cols):
            if matrix[0][c] == 0:
                for r in range(1, rows):
                    matrix[r][c] = 0

        # set the first row to zero if needed
        if first_row_has_zero:
            for c in range(cols):
                matrix[0][c] = 0

        # set the first column to zero if needed
        if first_col_has_zero:
            for r in range(rows):
                matrix[r][0] = 0


