'''
You are given a string s consisting of only uppercase english characters and an integer k. You can choose up to k characters of the string and replace them with any other uppercase English character.

After performing at most k replacements, return the length of the longest substring which contains only one distinct character.

Example 1:

Input: s = "XYYX", k = 2

Output: 4
Explanation: Either replace the 'X's with 'Y's, or replace the 'Y's with 'X's.

Example 2:

Input: s = "AAABABB", k = 1

Output: 5
Constraints:

1 <= s.length <= 1000
0 <= k <= s.length

Insight:

* grow as much as possible until there are k replacable things in every window

'''




from collections import defaultdict


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_len = 0
        counts = defaultdict(int)
        start, end = 0, 0

        # init
        counts[s[end]] = 1

        while end < len(s):
            # print(f"out | start: {start}, end: {end}")
            while (end < len(s)) and ((end - start + 1) - max(counts.values()) <= k):
                max_len = max(max_len, end - start + 1)
                # print(f"in | max_len: {max_len}, start: {start}, end: {end}, window: {end-start+1}, counts: {counts}")
                end += 1
                if end < len(s):
                    counts[s[end]] += 1
            counts[s[start]] -= 1
            start += 1

        return max_len
