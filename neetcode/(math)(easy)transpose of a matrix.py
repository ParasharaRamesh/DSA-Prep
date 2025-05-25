from typing import List


class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        ans = [[None] * m] * n
        for i in range(m):
            for j in range(n):
                ans[j][i] = matrix[i][j]

        return ans

if __name__ == '__main__':
    s = Solution()

    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    expected = [[1,4,7],[2,5,8],[3,6,9]]
    ans = s.transpose(matrix)
    assert expected == ans, f"{expected = } {ans = }"

    matrix = [[1,2,3],[4,5,6]]
    expected = [[1,4],[2,5],[3,6]]
    ans = s.transpose(matrix)
    assert expected == ans, f"{expected = } {ans = }"