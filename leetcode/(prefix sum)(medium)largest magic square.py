'''
A k x k magic square is a k x k grid filled with integers such that every row sum, every column sum, and both diagonal sums are all equal. The integers in the magic square do not have to be distinct. Every 1 x 1 grid is trivially a magic square.

Given an m x n integer grid, return the size (i.e., the side length k) of the largest magic square that can be found within this grid.

 

Example 1:


Input: grid = [[7,1,4,5,6],[2,5,1,6,4],[1,5,4,3,2],[1,2,7,3,4]]
Output: 3
Explanation: The largest magic square has a size of 3.
Every row sum, column sum, and diagonal sum of this magic square is equal to 12.
- Row sums: 5+1+6 = 5+4+3 = 2+7+3 = 12
- Column sums: 5+5+2 = 1+4+7 = 6+3+3 = 12
- Diagonal sums: 5+4+3 = 6+4+2 = 12
Example 2:


Input: grid = [[5,1,3,1],[9,3,3,1],[1,3,3,8]]
Output: 2
 

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 50
1 <= grid[i][j] <= 106
'''
from typing import List
from bisect import *

class Solution:
    def largestMagicSquare(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        K = min(m, n)

        # prepare prefix_sums 
        self.prepare_prefix_sums(m, n, grid)

        # from side length K -> 2 
        for k in range(K, 1, -1):
            for i in range(m - k + 1):
                for j in range(n - k + 1):
                    # with (i,j) as top left check if it is a magic square
                    if self.is_magic_square(m, n, i, j, k):
                        return k

        # if not its just 1
        return 1
        
    def prepare_prefix_sums(self, m, n, grid):
        self.row_prefix_sums = [[None for _ in range(n)] for _ in range(m)]
        self.col_prefix_sums = [[None for _ in range(n)] for _ in range(m)]
        self.pos_diag_prefix_sums = dict()
        self.neg_diag_prefix_sums = dict()

        for i in range(m):
            for j in range(n):
                # populate row ps
                if j == 0:
                    self.row_prefix_sums[i][j] = grid[i][j]
                else:
                    self.row_prefix_sums[i][j] = self.row_prefix_sums[i][j-1] + grid[i][j] 

                # populate col ps
                if i == 0:
                    self.col_prefix_sums[i][j] = grid[i][j]
                else:
                    self.col_prefix_sums[i][j] = self.col_prefix_sums[i - 1][j] + grid[i][j] 

                pid = n*i + j

                # populate pos diag ps ( all same j - i )
                if j - i not in self.pos_diag_prefix_sums:
                    self.pos_diag_prefix_sums[j-i] = [(pid, (i,j), grid[i][j])]
                else:
                    res = self.pos_diag_prefix_sums[j-i][-1][-1] + grid[i][j]
                    self.pos_diag_prefix_sums[j-i].append((pid, (i,j), res))

                # populate neg diag ps ( all same j - i )
                if j + i not in self.neg_diag_prefix_sums:
                    self.neg_diag_prefix_sums[j+i] = [(pid, (i,j), grid[i][j])]
                else:
                    res = self.neg_diag_prefix_sums[j+i][-1][-1] + grid[i][j]
                    self.neg_diag_prefix_sums[j+i].append((pid, (i,j), res))

        return
    
    def is_magic_square(self, m, n, i, j, k):
        # square is (i, j) -> (i + k - 1, j + k - 1)
        # Falsify
        
        # use row ps to check all rows from [i -> i + k] if all have the same prefix sums
        row_sum = None

        for s in range(k):
            row_s_sum = self.row_prefix_sums[i+s][j + k - 1]
            if j > 0:
                row_s_sum = self.row_prefix_sums[i+s][j + k - 1] - self.row_prefix_sums[i+s][j-1]
            
            if row_sum == None:
                row_sum = row_s_sum
            elif row_sum != row_s_sum:
                return False


        # use col ps to check all cols from [j -> j + k] if all have the same prefix sums
        col_sum = None

        for s in range(k):
            col_s_sum = self.col_prefix_sums[i + k - 1][j + s]
            if i > 0:
                col_s_sum = self.col_prefix_sums[i + k - 1][j + s] - self.col_prefix_sums[i-1][j+s]
            
            if col_sum == None:
                col_sum = col_s_sum
            elif col_sum != col_s_sum:
                return False

        # check pos diag
        pid = n*i + j
        other_pid = n*(i + k - 1) + (j + k - 1)
        pos_diag_ps = self.pos_diag_prefix_sums[j-i]
        
        pos_other_ind = bisect_left(pos_diag_ps, other_pid, key=lambda item: item[0])
        pos_ind = bisect_left(pos_diag_ps, pid, key=lambda item: item[0])

        pos_diag_sum = pos_diag_ps[pos_other_ind][-1]
        if pos_ind > 0:
            pos_diag_sum = pos_diag_ps[pos_other_ind][-1] - pos_diag_ps[pos_ind - 1][-1]

        # check neg diag
        neg_pid = n*i + (j + k - 1)
        neg_other_pid = n*(i+ k-1) + j

        neg_diag_ps = self.neg_diag_prefix_sums[(j + k - 1) + i]

        neg_other_ind = bisect_left(neg_diag_ps, neg_other_pid, key=lambda item: item[0])
        neg_ind = bisect_left(neg_diag_ps, neg_pid, key=lambda item: item[0])

        neg_diag_sum = neg_diag_ps[neg_other_ind][-1]
        if neg_ind > 0:
            neg_diag_sum = neg_diag_ps[neg_other_ind][-1] - neg_diag_ps[neg_ind - 1][-1]

        if pos_diag_sum != neg_diag_sum:
            return False
        
        # all sums in a magic square should be the same!
        return pos_diag_sum == neg_diag_sum == row_sum == col_sum

if __name__ == "__main__":
    s = Solution()

    grid = [
        [5,1,3,1],
        [9,3,3,1],
        [1,3,3,8]
    ]
    expected = 2
    ans = s.largestMagicSquare(grid)
    assert expected == ans, f"{expected=} {ans=}"

    grid = [
        [7,1,4,5,6],
        [2,5,1,6,4],
        [1,5,4,3,2],
        [1,2,7,3,4]
    ]
    expected = 3
    ans = s.largestMagicSquare(grid)
    assert expected == ans, f"{expected=} {ans=}"