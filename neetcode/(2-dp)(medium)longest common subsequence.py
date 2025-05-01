'''
Given two strings text1 and text2, return the length of the longest common subsequence between the two strings if one exists, otherwise return 0.

A subsequence is a sequence that can be derived from the given sequence by deleting some or no elements without changing the relative order of the remaining characters.

For example, "cat" is a subsequence of "crabt".
A common subsequence of two strings is a subsequence that exists in both strings.

Example 1:

Input: text1 = "cat", text2 = "crabt"

Output: 3
Explanation: The longest common subsequence is "cat" which has a length of 3.

Example 2:

Input: text1 = "abcd", text2 = "abcd"

Output: 4
Example 3:

Input: text1 = "abcd", text2 = "efgh"

Output: 0
Constraints:

1 <= text1.length, text2.length <= 1000
text1 and text2 consist of only lowercase English characters.
'''


class Solution:
    def longestCommonSubsequence_memo(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        cache = dict()
        def helper(i, j):
            key = (i,j)

            if key in cache:
                return cache[key]

            if i >= m or j >= n:
                cache[key] = 0
                return 0

            equal = 0
            if text1[i] == text2[j]:
                equal = 1 + helper(i + 1, j + 1)

            exc_i = helper(i, j + 1)
            exc_j = helper(i + 1, j)
            cache[key] = max(equal, exc_i, exc_j)

            return cache[key]


        return helper(0, 0)

    #bottom up
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        cache = dict()

        # base cases
        for j in range(n):
            cache[(m, j)] = 0

        for i in range(m):
            cache[(i, n)] = 0

        cache[(m, n)] = 0

        # all states
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                key = (i, j)

                equal = 0
                if text1[i] == text2[j]:
                    equal = 1 + cache[(i + 1, j + 1)]

                exc_i = cache[(i, j + 1)]
                exc_j = cache[(i + 1, j)]

                cache[key] = max(equal, exc_i, exc_j)

        return cache[(0, 0)]