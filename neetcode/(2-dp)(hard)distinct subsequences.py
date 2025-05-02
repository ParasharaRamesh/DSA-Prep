'''
You are given two strings s and t, both consisting of english letters.

Return the number of distinct subsequences of s which are equal to t.

Example 1:

Input: s = "caaat", t = "cat"

Output: 3
Explanation: Rhere are 3 ways you can generate "cat" from s.

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
    def numDistinct(self, s: str, t: str) -> int:
        pass