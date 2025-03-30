'''
You are given two strings s1 and s2.

Return true if s2 contains a permutation of s1, or false otherwise. That means if a permutation of s1 exists as a substring of s2, then return true.

Both strings only contain lowercase letters.

Example 1:

Input: s1 = "abc", s2 = "lecabee"

Output: true
Explanation: The substring "cab" is a permutation of "abc" and is present in "lecabee".

Example 2:

Input: s1 = "abc", s2 = "lecaabee"

Output: false
Constraints:

1 <= s1.length, s2.length <= 1000

Insights:

* static sliding window and check every window if there exists a permutation of s1

'''

from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        m = len(s1)
        n = len(s2)

        s1_counts = Counter(s1)
        s1_set = set(s1)

        start = 0
        end = m - 1

        while end < n:
            compare = s2[start: end + 1]
            if len(s1_set.intersection(set(compare))) == 0:
                start = end + 1
                end = start + (m - 1)
            elif s1_counts == Counter(compare):
                return True
            else:
                start += 1
                end += 1

        return False
