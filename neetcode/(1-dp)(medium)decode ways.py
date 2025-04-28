'''
A string consisting of uppercase english characters can be encoded to a number using the following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
To decode a message, digits must be grouped and then mapped back into letters using the reverse of the mapping above. There may be multiple ways to decode a message. For example, "1012" can be mapped into:

"JAB" with the grouping (10 1 2)
"JL" with the grouping (10 12)
The grouping (1 01 2) is invalid because 01 cannot be mapped into a letter since it contains a leading zero.

Given a string s containing only digits, return the number of ways to decode it. You can assume that the answer fits in a 32-bit integer.

Example 1:

Input: s = "12"

Output: 2

Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).
Example 2:

Input: s = "01"

Output: 0
Explanation: "01" cannot be decoded because "01" cannot be mapped into a letter.

Constraints:

1 <= s.length <= 100
s consists of digits

'''


class Solution:
    def numDecodings_topdown(self, s: str) -> int:
        # trvial cases
        if s[0] == "0":
            return 0

        cache = dict()

        # tail recursion
        def helper(i):
            if i in cache:
                return cache[i]

            #valid case to count
            if i == len(s) - 1:
                ans = 1 if s[i] != "0" else 0
                cache[i] = ans

            # valid case to count
            if i >= len(s):
                cache[i] = 1
                return cache[i]

            # trivial case
            if s[i] == "0":
                cache[i] = 0
                return cache[i]

            res = 0

            # can group by one
            res += helper(i + 1)

            # can group by two as long as s[i] is 1 and s[i] is 2 with s[i+1] E [0,6]
            if i + 1 < len(s):  # as long as the next character is in bounds
                if s[i] == "1":
                    res += helper(i + 2)
                elif s[i] == "2" and 0 <= int(s[i + 1]) <= 6:
                    res += helper(i + 2)

            cache[i] = res
            return res

        return helper(0)

    #bottom up
    def numDecodings(self, s: str) -> int:
        # trvial cases
        if s[0] == "0":
            return 0

        cache = dict()
        n = len(s)

        #base cases
        cache[n-1] = 1 if s[n-1] != "0" else 0
        cache[n] = 1

        #traverse
        for i in range(n-2, -1, -1):
            if s[i] == "0":
                cache[i] = 0
                continue

            res = 0

            #group by 1
            res += cache[i + 1]

            #group by 2
            if s[i] == "1":
                res += cache[i + 2]
            elif s[i] == "2" and 0 <= int(s[i + 1]) <= 6:
                res += cache[i + 2]

            cache[i] = res

        return cache[0]


if __name__ == '__main__':
    s = Solution()

    st = "226"
    expected = 3
    ans = s.numDecodings(st)
    assert ans == expected, f"expected: {expected}, got {ans}"

    st = "12"
    expected = 2
    ans = s.numDecodings(st)
    assert ans == expected, f"expected: {expected}, got {ans}"

    st = "10"
    expected = 1
    ans = s.numDecodings(st)
    assert ans == expected, f"expected: {expected}, got {ans}"
