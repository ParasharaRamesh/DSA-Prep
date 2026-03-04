'''
Write an efficient algorithm that searches for a value target in an m x n integer matrix matrix. This matrix has the following properties:

Integers in each row are sorted in ascending from left to right.
Integers in each column are sorted in ascending from top to bottom.
 

Example 1:


Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
Output: true
Example 2:


Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
Output: false
 

Constraints:

m == matrix.length
n == matrix[i].length
1 <= n, m <= 300
-109 <= matrix[i][j] <= 109
All the integers in each row are sorted in ascending order.
All the integers in each column are sorted in ascending order.
-10^9 <= target <= 10^9

'''
from typing import List
from bisect import *

class Solution:
    '''
    Time complexity: O(m + n)
    This solution starts from bottom left and moves up or right depending on the target and the current value.
    at any cell, to the right and down is all greater and to the top and left is all smaller
    '''
    def searchMatrix_linear(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])

        is_valid = lambda i, j: 0 <= i < m and 0 <= j < n
        
        def up(i, j):
            return (i-1,j) if is_valid(i-1, j) else None

        def right(i, j):
            return (i,j+1) if is_valid(i, j+1) else None

                
        pos = (m-1, 0)

        while True:
            i, j = pos

            if matrix[i][j] == target:
                return True

            if matrix[i][j] < target:
                pos = right(i,j)
                if pos == None:
                    return False
            else:
                pos = up(i,j)
                if pos == None:
                    return False

    '''
    O(m*log(n)) -> in each row do a binary search
    '''
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])

        for row in matrix:
            j = bisect_left(row, target)

            if j == n:
                continue

            if row[j] == target:
                return True

        return False