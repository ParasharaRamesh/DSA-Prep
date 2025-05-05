'''
You are given an input string s consisting of lowercase english letters, and a pattern p consisting of lowercase english letters, as well as '.', and '*' characters.

Return true if the pattern matches the entire input string, otherwise return false.

'.' Matches any single character
'*' Matches zero or more of the preceding element.
Example 1:

Input: s = "aa", p = ".b"

Output: false
Explanation: Regardless of which character we choose for the '.' in the pattern, we cannot match the second character in the input string.

Example 2:

Input: s = "nnn", p = "n*"

Output: true
Explanation: '*' means zero or more of the preceding element, 'n'. We choose 'n' to repeat three times.

Example 3:

Input: s = "xyz", p = ".*z"

Output: true
Explanation: The pattern ".*" means zero or more of any character, so we choose ".." to match "xy" and "z" to match "z".

Constraints:

1 <= s.length <= 20
1 <= p.length <= 20
Each appearance of '*', will be preceded by a valid character or '.'.
'''

from functools import lru_cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        @lru_cache(None)
        def dp(i: int, j: int) -> bool:
            # Base case: pattern exhausted
            if j == len(p):
                return i == len(s)

            # Check if current characters match
            first_match = i < len(s) and (s[i] == p[j] or p[j] == '.')

            # Lookahead for '*'
            if j + 1 < len(p) and p[j + 1] == '*':
                # Two cases: zero occurrences OR one+ if first matches
                return dp(i, j + 2) or (first_match and dp(i + 1, j))
            else:
                return first_match and dp(i + 1, j + 1)

        return dp(0, 0)

    # topdown
    def isMatch_ugly(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        cache = dict()

        def helper(i, j):
            key = (i, j)

            if key in cache:
                return cache[key]

            # empty string for s, but p[j+1] = * (which means zero match)
            if i == m and j + 1 < n and p[j + 1] == "*":
                cache[key] = helper(i, j + 2)
                return cache[key]

            # out of bounds
            if i > m or j > n:
                cache[key] = False
                return False

            # match: both exhausted
            if i == m and j == n:
                cache[key] = True
                return True

            # only one exhausted
            if i == m or j == n:
                cache[key] = False
                return False

            # not same character (excluding .)
            if s[i] != p[j] and p[j] != ".":
                if j + 1 < n and p[j + 1] != "*":
                    # next one is not a star
                    cache[key] = False
                    return False
                else:
                    # next one is a star, means can do zero match. j + 2 skips the star
                    cache[key] = helper(i, j + 2)
                    return cache[key]

            # same character
            if s[i] == p[j]:
                if j == n - 1:
                    # p is in last character
                    cache[key] = helper(i + 1, j + 1)
                    return cache[key]
                elif j + 1 < n and p[j + 1] != "*":
                    # p is not in last character and next one is not *
                    cache[key] = helper(i + 1, j + 1)
                    return cache[key]
                else:
                    # else p[j+1] == *
                    _i = i
                    while _i < m and s[_i] == s[i]:
                        match = helper(_i, j + 2)
                        if match:
                            cache[key] = True
                            return True
                        _i += 1

                    # continue from next
                    cache[key] = helper(_i, j + 2)
                    return cache[key]

            # wildcard
            if p[j] == ".":
                if j == n - 1:
                    # p is in last character
                    cache[key] = helper(i + 1, j + 1)
                    return cache[key]
                elif j + 1 < n and p[j + 1] != "*":
                    # p is not in last character and next one is not *
                    cache[key] = helper(i + 1, j + 1)
                    return cache[key]
                else:
                    # else it is *
                    _i = i
                    while _i < m:
                        match = helper(_i, j + 2)
                        if match:
                            cache[key] = True
                            return True
                        _i += 1

                    # continue from next
                    cache[key] = helper(_i, j + 2)
                    return cache[key]

            # default case
            return False

        return helper(0, 0)


if __name__ == '__main__':
    sol = Solution()

    s = "a"
    p = "ab*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aab"
    p = "c*a*b"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "abcd"
    p = ".*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "abcd"
    p = ".*d"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "abcd"
    p = ".*d*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aab"
    p = "a*b"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "a"
    p = "a*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aa"
    p = "a*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aaa"
    p = "a*"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aab"
    p = "a*"
    ans = sol.isMatch(s, p)
    expected = False
    assert expected == ans, f"{expected = } , {ans = }"

    s = "bc"
    p = "bc"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "abc"
    p = "abc"
    ans = sol.isMatch(s, p)
    expected = True
    assert expected == ans, f"{expected = } , {ans = }"

    s = "abc"
    p = "ab"
    ans = sol.isMatch(s, p)
    expected = False
    assert expected == ans, f"{expected = } , {ans = }"

    s = "aa"
    p = "a"
    ans = sol.isMatch(s, p)
    expected = False
    assert expected == ans, f"{expected = } , {ans = }"
