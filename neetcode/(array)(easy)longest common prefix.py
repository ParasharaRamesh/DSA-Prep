'''
You are given an array of strings strs. Return the longest common prefix of all the strings.

If there is no longest common prefix, return an empty string "".

Example 1:

Input: strs = ["bat","bag","bank","band"]

Output: "ba"
Example 2:

Input: strs = ["dance","dag","danger","damage"]

Output: "da"
Example 3:

Input: strs = ["neet","feet"]

Output: ""
Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] is made up of lowercase English letters if it is non-empty.
'''

from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 1:
            return strs[0]

        res = ""
        all_chars = zip(*strs)

        for t in all_chars:
            if len(set(t)) == 1:
                res += t[0]
            else:
                break

        return res