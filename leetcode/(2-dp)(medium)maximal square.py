'''
Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.

 

Example 1:


Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 4
Example 2:


Input: matrix = [["0","1"],["1","0"]]
Output: 1
Example 3:

Input: matrix = [["0"]]
Output: 0
 

Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 300
matrix[i][j] is '0' or '1'.

Thoughts:

. pretty standard, just check the squares to the right, down and diagonal below and make the decision
'''

from typing import List
from functools import *

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        R = len(matrix)
        C = len(matrix[0])

        # return the length of the square
        @cache
        def square(i,j):
            if i >= R or j >= C:
                return 0

            if matrix[i][j] == "0":
                return 0

            right = square(i, j+1)
            down = square(i+1, j)
            diag = square(i+1, j+1)
            
            return 1 + min(right, down, diag)

        res = 0
        for i in range(R):
            for j in range(C):
                if matrix[i][j] == "1":
                    side = square(i, j)
                    res = max(res, side ** 2)
        
        return res
