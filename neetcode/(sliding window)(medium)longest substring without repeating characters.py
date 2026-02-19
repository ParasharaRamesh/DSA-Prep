'''
Given a string s, find the length of the longest substring without duplicate characters.



Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.


Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.

'''

from collections import defaultdict


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0

        if len(s) == len(set(s)):
            return len(s)

        start = 0
        end = 0
        longest = 0
        counts = defaultdict(int)

        while end < len(s):
            # grow
            while end < len(s) and counts[s[end]] == 0:
                counts[s[end]] += 1
                end += 1

            # assign
            longest = max(longest, end - start)

            # shrink
            counts[s[start]] -= 1
            start += 1

        return longest

    def lengthOfLongestSubstring_for_loop(self, s: str) -> int:
        """Sliding window with for-loop: grow (add s[r]), shrink until valid, then evaluate."""
        l = 0
        res = 0
        counts = defaultdict(int)

        for r in range(len(s)):
            # 1. GROW: Add the right element to state
            counts[s[r]] += 1

            # 2. SHRINK: While we have a duplicate, move l
            while counts[s[r]] > 1:
                counts[s[l]] -= 1
                l += 1

            # 3. EVALUATE: Window [l, r] has no duplicates
            res = max(res, r - l + 1)

        return res