'''
Given an m x n matrix of integers matrix, return a list of all elements within the matrix in spiral order.

Example 1:



Input: matrix = [[1,2],[3,4]]

Output: [1,2,4,3]
Example 2:



Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]

Output: [1,2,3,6,9,8,7,4,5]
Example 3:

Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]

Output: [1,2,3,4,8,12,11,10,9,5,6,7]
Constraints:

1 <= matrix.length, matrix[i].length <= 10
-100 <= matrix[i][j] <= 100
'''
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        visited = set()
        spiral = []

        is_valid_pos = lambda i, j: 0 <= i < m and 0 <= j < n

        get_left_pos = lambda i, j: (i, j - 1) if is_valid_pos(i, j - 1) and (i, j - 1) not in visited else None
        get_right_pos = lambda i, j: (i, j + 1) if is_valid_pos(i, j + 1) and (i, j + 1) not in visited else None
        get_up_pos = lambda i, j: (i - 1, j) if is_valid_pos(i - 1, j) and (i - 1, j) not in visited else None
        get_down_pos = lambda i, j: (i + 1, j) if is_valid_pos(i + 1, j) and (i + 1, j) not in visited else None

        '''
        go as right as possible -> as down as possible -> as left as possible -> as up as possible -> repeat
        '''

        # start positions
        i, j = 0, 0
        visited.add((i, j))
        spiral.append(matrix[i][j])

        while len(spiral) < m * n:
            while get_right_pos(i, j) != None:
                i, j = get_right_pos(i, j)
                spiral.append(matrix[i][j])
                visited.add((i, j))

            while get_down_pos(i, j) != None:
                i, j = get_down_pos(i, j)
                spiral.append(matrix[i][j])
                visited.add((i, j))

            while get_left_pos(i, j) != None:
                i, j = get_left_pos(i, j)
                spiral.append(matrix[i][j])
                visited.add((i, j))

            while get_up_pos(i, j) != None:
                i, j = get_up_pos(i, j)
                spiral.append(matrix[i][j])
                visited.add((i, j))

        return spiral

    # define boundaries and shrink those
    def spiralOrder_bondaryshrinking(matrix: List[List[int]]) -> List[int]:
        res = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Move right
            for j in range(left, right + 1):
                res.append(matrix[top][j])
            top += 1

            # Move down
            for i in range(top, bottom + 1):
                res.append(matrix[i][right])
            right -= 1

            # Move left
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    res.append(matrix[bottom][j])
                bottom -= 1

            # Move up
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    res.append(matrix[i][left])
                left += 1

        return res

if __name__ == '__main__':
    s = Solution()

    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    expected = [1,2,3,6,9,8,7,4,5]
    res = s.spiralOrder(matrix)
    assert expected == res, f"expected {expected}, got {res}"

    matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    expected = [1,2,3,4,8,12,11,10,9,5,6,7]
    res = s.spiralOrder(matrix)
    assert expected == res, f"expected {expected}, got {res}"