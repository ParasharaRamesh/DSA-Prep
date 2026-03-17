'''
You are given a binary matrix matrix of size m x n, and you are allowed to rearrange the columns of the matrix in any order.
Return the area of the largest submatrix within matrix where every element of the submatrix is 1 after reordering the columns optimally.
 
Example 1:

Input: matrix = [[0,0,1],[1,1,1],[1,0,1]]
Output: 4
Explanation: You can rearrange the columns as shown above.
The largest submatrix of 1s, in bold, has an area of 4.

Example 2:

Input: matrix = [[1,0,1,0,1]]
Output: 3
Explanation: You can rearrange the columns as shown above.
The largest submatrix of 1s, in bold, has an area of 3.

Example 3:

Input: matrix = [[1,1,0],[1,0,1]]
Output: 2
Explanation: Notice that you must rearrange entire columns, and there is no way to make a submatrix of 1s larger than an area of 2.

 
Constraints:
• m == matrix.length
• n == matrix[i].length
• 1 <= m * n <= 105
• matrix[i][j] is either 0 or 1.
'''
'''
similar idea from the maximal rectangle problem where for each row figure out the histoagram of heights starting from there 

sort that row and find the max area  because rearrangements are possible
'''
from copy import deepcopy

class Solution:
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        prev_row = matrix[0]
        max_area = prev_row.count(1)

        for row in matrix[1:]:
            # print("\n" + "_"* 70)
            # print(f"{max_area=} | {prev_row=} |{row=}")

            row_heights = []
            for val, prev_val in zip(row, prev_row):
                if val == 1:
                    row_heights.append(val + prev_val)
                else:
                    row_heights.append(0)

            prev_row = row_heights.copy()
            # print(f"{row_heights=}")

            # find max area based on this [0,1,2,3,4]
            row_heights.sort()
            # print(f"sorted {row_heights=}")

            for i, h in enumerate(row_heights):
                area = h * (n - i)
                max_area = max(max_area, area)
                # print(f"  {h=} | {area=} | {max_area=}")

        return max_area
