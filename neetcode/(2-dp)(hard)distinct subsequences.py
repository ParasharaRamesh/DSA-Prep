'''
You are given two strings s and t, both consisting of english letters.

Return the number of distinct subsequences of s which are equal to t.

Example 1:

Input: s = "caaat", t = "cat"

Output: 3
Explanation: There are 3 ways you can generate "cat" from s.

(c)aa(at)
(c)a(a)a(t)
(ca)aa(t)

Example 2:

Input: s = "xxyxy", t = "xy"

Output: 5
Explanation: There are 5 ways you can generate "xy" from s.

(x)x(y)xy
(x)xyx(y)
x(x)(y)xy
x(x)yx(y)
xxy(x)(y)
Constraints:

1 <= s.length, t.length <= 1000
s and t consist of English letters.


'''


class Solution:
    def numDistinct_memo(self, s: str, t: str) -> int:
        # trivial cases
        if len(s) < len(t):
            return 0

        if len(s) == len(t):
            return 1 if s == t else 0

        m = len(s)
        n = len(t)

        cache = dict()

        def helper(i, j):
            key = (i, j)

            if key in cache:
                return cache[key]

            # all chars in t matched!
            if j == n:
                cache[key] = 1
                return 1

            # exhausted i
            if i == m:
                cache[key] = 0
                return 0

            total = 0

            # include
            if s[i] == t[j]:
                total += helper(i + 1, j + 1)

            # exclude
            total += helper(i + 1, j)

            cache[key] = total
            return total

        return helper(0, 0)

    def numDistinct_tab(self, s: str, t: str) -> int:
        # trivial cases
        if len(s) < len(t):
            return 0

        if len(s) == len(t):
            return 1 if s == t else 0

        m = len(s)
        n = len(t)

        cache = dict()

        # base cases ?
        # exhausted i
        # if i == m:
        #     cache[key] = 0
        #     return 0

        for j in range(n):
            cache[(m, j)] = 0

        # all chars in t matched!
        # if j == n:
        #     cache[key] = 1
        #     return 1
        for i in range(m + 1):
            cache[(i, n)] = 1

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                key = (i, j)

                total = 0

                # include
                if s[i] == t[j]:
                    total += cache[(i + 1, j + 1)]

                # exclude
                total += cache[(i + 1, j)]

                cache[key] = total

        return cache[(0, 0)]