'''
Given a string s, split s into substrings where every substring is a palindrome. Return all possible lists of palindromic substrings.

You may return the solution in any order.

Example 1:

Input: s = "aab"

Output: [["a","a","b"],["aa","b"]]
Example 2:

Input: s = "a"

Output: [["a"]]
Constraints:

1 <= s.length <= 20
s contains only lowercase English letters.

'''
from typing import List


class Solution:
    def is_palindrome(self, s):
        start = 0
        end = len(s) - 1

        while start <= end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1

        return True

    def partition(self, s: str) -> List[List[str]]:
        res = []

        def helper(s, splits=[]):
            if len(s) == 0:
                if len(splits) > 0:
                    res.append(splits)
                return

            if len(s) == 1:
                res.append(splits + [s])
                return

            for i in range(1, len(s) + 1):
                part = s[:i]
                rest = s[i:]

                # print(f"part {part}, rest {rest}")

                if self.is_palindrome(part):
                    helper(rest, splits + [part])

        helper(s, [])
        return res
