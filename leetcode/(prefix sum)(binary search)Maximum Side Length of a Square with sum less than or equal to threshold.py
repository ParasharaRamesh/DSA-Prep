'''
Given a m x n matrix mat and an integer threshold, return the maximum side-length of a square with a sum less than or equal to threshold or return 0 if there is no such square.

Example 1:


Input: mat = [
    [1,1,3,2,4,3,2],
    [1,1,3,2,4,3,2],
    [1,1,3,2,4,3,2]
], threshold = 4
Output: 2
Explanation: The maximum side length of square with sum less than 4 is 2 (i.e. the 2x2 squares with 1s)


Example 2:

Input: mat = [
    [2,2,2,2,2],
    [2,2,2,2,2],
    [2,2,2,2,2],
    [2,2,2,2,2],
    [2,2,2,2,2]
], threshold = 1
Output: 0
 
Constraints:

m == mat.length
n == mat[i].length
1 <= m, n <= 300
0 <= mat[i][j] <= 104
0 <= threshold <= 105
'''

from typing import List
from collections import defaultdict

class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        # get side lengths
        m, n = len(mat), len(mat[0])

        # construct a 2d prefix sum such that ps[(i,j)] = sum of all values in the rectangle (0, 0) as top left to (i,j) as bottom right point of the rectangle
        prefix_sums = self.construct_prefix_sum(mat)

        ''' 
        do binary search to find the answer of the lowest square side length:
        . answer lies in range (0, min(m, n))
        . at each square length:
            - do a sliding window of that square across the matrix and see if it is valid ( i.e. atleast one square sum exists <= threshold)
            - if valid:
                . we can find bigger ones so low = mid + 1
            - else:
                . we cannot find bigger ones so the answer must be smaller high = mid - 1
        '''

        l = 0
        r = min(m, n)

        ans = 0

        while l <= r:
            side = (l + r) // 2

            if self.is_valid(mat, side, prefix_sums, threshold):
                # square of side is valid, so we can try searching for bigger
                ans = max(ans, side)
                l = side + 1
            else:
                r = side - 1

        return ans        

    def construct_prefix_sum(self, mat: List[List[int]]) -> defaultdict:
       m, n = len(mat), len(mat[0])

       prefix_sums = defaultdict(int)

       for i in range(m):
           for j in range(n):
                # include current element
                # include sum of rectangle above
                # include sum of rectangle to the left
                # exclude sum of rectangle top-left (as it is included twice)
               prefix_sums[(i, j)] = mat[i][j] + prefix_sums[(i - 1, j)] + prefix_sums[(i, j - 1)] - prefix_sums[(i - 1, j - 1)]

       return prefix_sums

    def is_valid(self, mat: List[List[int]], side: int, prefix_sums: defaultdict, threshold: int) -> bool:
        m, n = len(mat), len(mat[0])

        for i in range(m - side + 1):
            for j in range(n - side + 1):
                # (i, j) is the top left of the corner -> bottom right is (i + side - 1, j + side - 1)
                bi = i + side - 1
                bj = j + side - 1

                '''
                check if the sum from (i, j) to (bi, bj) is <= threshold; same inclusion exclusion principle
                    . sum of rectangle with bottom right at (bi, bj)
                    . subtract sum of rectangle with bottom right at (i - 1, bj)
                    . subtract sum of rectangle with bottom right at (bi, j - 1)
                    . add sum of rectangle with bottom right at (i - 1, j - 1) because it was subtracted twice
                '''
                square_sum = prefix_sums[(bi, bj)] - prefix_sums[(i - 1, bj)] - prefix_sums[(bi, j - 1)] + prefix_sums[(i - 1, j - 1)]

                if square_sum <= threshold:
                    return True

        return False
                
if __name__ == "__main__":
    s = Solution()

    mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]]
    threshold = 4
    ans = s.maxSideLength(mat, threshold)
    expected = 2
    assert ans == expected, f"{expected=} {ans=}"

    mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]]
    threshold = 1
    ans = s.maxSideLength(mat, threshold)
    expected = 0
    assert ans == expected, f"{expected=} {ans=}"