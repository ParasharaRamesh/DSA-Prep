'''
You are given two strings word1 and word2, each consisting of lowercase English letters.

You are allowed to perform three operations on word1 an unlimited number of times:

Insert a character at any position
Delete a character at any position
Replace a character at any position
Return the minimum number of operations to make word1 equal word2.

Example 1:

Input: word1 = "monkeys", word2 = "money"

Output: 2
Explanation:
monkeys -> monkey (remove s)
monkey -> monkey (remove k)

Example 2:

Input: word1 = "neatcdee", word2 = "neetcode"

Output: 3
Explanation:
neatcdee -> neetcdee (replace a with e)
neetcdee -> neetcde (remove last e)
neetcde -> neetcode (insert o)

Constraints:

0 <= word1.length, word2.length <= 100
word1 and word2 consist of lowercase English letters.

'''


class Solution:
    def minDistance_memo(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        cache = dict()

        def helper(i, j):
            key = (i, j)

            if key in cache:
                return cache[key]

            # base cases
            if i == m and j < n:
                # insert
                cache[key] = n - j
                return n - j

            if i < m and j == n:
                # delete
                cache[key] = m - i
                return m - i

            if i == m and j == n:
                cache[key] = 0
                return 0

            # actual logic
            if word1[i] == word2[j]:
                cache[key] = helper(i + 1, j + 1)
                return cache[key]

            # try everything
            subs = 1 + helper(i + 1, j + 1)
            ins = 1 + helper(i, j + 1)
            rem = 1 + helper(i + 1, j)

            cache[key] = min(subs, ins, rem)
            return cache[key]

        return helper(0, 0)

    def minDistance_tab(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        cache = dict()

        cache[(m, n)] = 0

        for i in range(m):
            cache[(i , n)] = m - i

        for j in range(n):
            cache[(m, j)] = n - j

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                key = (i, j)

                # actual logic
                if word1[i] == word2[j]:
                    cache[key] = cache[(i + 1, j + 1)]
                    continue

                # try everything
                subs = 1 + cache[(i + 1, j + 1)]
                ins = 1 + cache[(i, j + 1)]
                rem = 1 + cache[(i + 1, j)]

                cache[key] = min(subs, ins, rem)

        return cache[(0, 0)]

if __name__ == '__main__':
    s = Solution()

    word1 = "a"
    word2 = "ab"
    expected = 1
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"

    word1 = "ab"
    word2 = "a"
    expected = 1
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"

    word1 = "a"
    word2 = "b"
    expected = 1
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"

    word1 = "ab"
    word2 = "ab"
    expected = 0
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"

    word1 = "neatcdee"
    word2 = "neetcode"
    expected = 3
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"

    word1 = "monkeys"
    word2 = "money"
    expected = 2
    ans = s.minDistance(word1, word2)
    assert expected == ans, f"{expected = }, {ans = }"


