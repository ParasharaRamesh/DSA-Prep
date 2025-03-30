'''
Given two strings s and t, return the shortest substring of s such that every character in t, including duplicates, is present in the substring. If such a substring does not exist, return an empty string "".

You may assume that the correct output is always unique.

Example 1:

Input: s = "OUZODYXAZV", t = "XYZ"

Output: "YXAZ"
Explanation: "YXAZ" is the shortest substring that includes "X", "Y", and "Z" from string t.

Example 2:

Input: s = "xyz", t = "xyz"

Output: "xyz"
Example 3:

Input: s = "x", t = "xy"

Output: ""
Constraints:

1 <= s.length <= 1000
1 <= t.length <= 1000
s and t consist of uppercase and lowercase English letters.

Insight:
* dynamic sliding window with grow phase and shrink phase

'''

from collections import Counter, defaultdict


class Solution:
    def doesContain(self, window_counts, t_counts):
        contains = True
        for ch, ch_count in t_counts.items():
            if ch not in window_counts:
                contains = False
                break
            elif ch_count > window_counts[ch]:
                contains = False
                break
        return contains

    def minWindow(self, s: str, t: str) -> str:
        n = len(s)
        m = len(t)

        t_counts = Counter(t)
        s_counts = Counter(s)

        if not self.doesContain(s_counts, t_counts):
            return ""

        min_window = s[:]

        start, end = 0, -1
        window_counts = defaultdict(int)

        while end < n:
            # grow until contains
            contains = False
            while end < n:
                end += 1
                if end < n:
                    window_counts[s[end]] += 1

                    contains = self.doesContain(window_counts, t_counts)
                    if contains:
                        break

            if contains:
                window = s[start: end + 1]
                if len(window) <= len(min_window):
                    min_window = window
            elif end == n:
                break

            # shrink as far as possible
            while 0 <= start <= end < n and self.doesContain(window_counts, t_counts):
                window = s[start: end + 1]
                if len(window) <= len(min_window):
                    min_window = window

                window_counts[s[start]] -= 1
                start += 1

        return min_window