'''
You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.



Example 1:

Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
Example 2:

Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.


Constraints:

1 <= s.length <= 105
s consists of only uppercase English letters.
0 <= k <= s.length


'''

import string

class Solution:
    def findMaxCount(self, windowCounts):
        maxCount = float("-inf")
        bestChar = None
        for ch in windowCounts:
            if windowCounts[ch] >= maxCount:
                bestChar = ch
                maxCount = windowCounts[ch]
        return maxCount

    def characterReplacement(self, s: str, k: int) -> int:
        l = 0
        r = 0
        res = 0
        windowCounts = {ch: 0 for ch in string.ascii_uppercase}
        windowCounts[s[l]] = 1

        while l <= r and r < len(s):
            # find size of current window
            window = r - l + 1

            # this difference represents the no of remaining characters which are convertable
            convertableChars = window - self.findMaxCount(windowCounts)
            if convertableChars <= k:
                # we can still go ahead
                r += 1
                if 0 <= r < len(s):
                    windowCounts[s[r]] += 1
                res = max(res, window)
            else:
                if 0 <= l < len(s):
                    # decrement count of the left most by one as the window has now changed
                    windowCounts[s[l]] -= 1
                l += 1

        return res

if __name__ == '__main__':
    #case 1: ans 4
    # k = 2
    # s = "ABAB"

    #case 2: ans4
    s = "AABABBA"
    k = 1

    sol = Solution()
    print(sol.characterReplacement(s, k))