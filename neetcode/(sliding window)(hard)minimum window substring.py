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

    def minWindow_for_loop(self, s: str, t: str) -> str:
        """Grow (add s[r]), shrink while valid (update best), one loop."""
        if not t:
            return ""
        t_counts = Counter(t)
        required = len(t_counts)  # distinct chars we must satisfy
        window = defaultdict(int)
        formed = 0
        res_start, res_len = 0, float("inf")
        l = 0

        for r in range(len(s)):
            # 1. GROW: add s[r]
            c = s[r]
            window[c] += 1
            if c in t_counts and window[c] == t_counts[c]:
                formed += 1

            # 2. SHRINK: while window [l, r] still contains t, update best and shrink
            while formed == required and l <= r:
                if r - l + 1 < res_len:
                    res_len = r - l + 1
                    res_start = l
                window[s[l]] -= 1
                if s[l] in t_counts and window[s[l]] < t_counts[s[l]]:
                    formed -= 1
                l += 1

        return s[res_start : res_start + res_len] if res_len != float("inf") else ""