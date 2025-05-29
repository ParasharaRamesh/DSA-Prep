'''
Given a square n x n matrix of integers matrix, rotate it by 90 degrees clockwise.

You must rotate the matrix in-place. Do not allocate another 2D matrix and do the rotation.

Example 1:



Input: matrix = [
  [1,2],
  [3,4]
]

Output: [
  [3,1],
  [4,2]
]
Example 2:



Input: matrix = [
  [1,2,3],
  [4,5,6],
  [7,8,9]
]

Output: [
  [7,4,1],
  [8,5,2],
  [9,6,3]
]
Constraints:

n == matrix.length == matrix[i].length
1 <= n <= 20
-1000 <= matrix[i][j] <= 1000
'''
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)

        # reverse everything in place, go through each row
        for i in range(n):
            matrix[i] = matrix[i][::-1]

        # swap all the ones on the other side of the secondary diagonal
        for i in range(n):
            for j in range(n):
                if i + j < n - 1:
                    o_i, o_j = n - 1 - j, n - 1 - i
                    matrix[i][j], matrix[o_i][o_j] = matrix[o_i][o_j], matrix[i][j]

        print(matrix)

    # can also reverse columns and then swap with transposed element on the other side of the primary diagonal
    def rotate_cols(self, matrix: List[List[int]]) -> None:
        # Reverse the matrix vertically
        matrix.reverse()

        # Transpose the matrix
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

if __name__ == '__main__':
    s = Solution()

    matrix = [
        [1, 2],
        [3, 4]
    ]
    expected = [
        [3, 1],
        [4, 2]
    ]
    s.rotate(matrix)

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    Output: [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    s.rotate(matrix)

    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    s.rotate(matrix)