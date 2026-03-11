'''
You are given a 2D matrix matrix, handle multiple queries of the following type:

Calculate the sum of the elements of matrix inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).
Implement the NumMatrix class:

NumMatrix(int[][] matrix) Initializes the object with the integer matrix matrix.
int sumRegion(int row1, int col1, int row2, int col2) Returns the sum of the elements of matrix inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).
You must design an algorithm where sumRegion works on O(1) time complexity.
Example 1:

Input: ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]

Output: [null, 8, 11, 12]
Explanation:
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)

Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 200
-10,000 <= matrix[i][j] <= 10,000
0 <= row1 <= row2 < m
0 <= col1 <= col2 < n
At most 10,000 calls will be made to sumRegion.
'''
from collections import defaultdict

class NumMatrix_defaultdict_hack:
    def __init__(self, matrix: List[List[int]]):
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.ps = defaultdict(int)

        for i in range(self.m):
            for j in range(self.n):
                self.ps[(i,j)] = matrix[i][j] + self.ps[(i-1, j)] + self.ps[(i, j-1)] - self.ps[(i-1,j-1)]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.ps[(row2, col2)] - self.ps[(row2, col1 - 1)] - self.ps[(row1-1,col2)] + self.ps[(row1 - 1, col1 - 1)]

class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]: return
        
        M, N = len(matrix), len(matrix[0])
        # Initialize with 0s - handles the 'out of bounds' cases automatically
        self.ps = [[0] * (N + 1) for _ in range(M + 1)]
        
        for r in range(M):
            for c in range(N):
                # We fill ps[r+1][c+1] using matrix[r][c]
                self.ps[r+1][c+1] = matrix[r][c] + self.ps[r][c+1] + \
                                    self.ps[r+1][c] - self.ps[r][c]

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        # The +1 shift is applied here to map 0-indexed input to 1-indexed prefix sum
        return self.ps[r2+1][c2+1] - self.ps[r2+1][c1] - \
               self.ps[r1][c2+1] + self.ps[r1][c1]
