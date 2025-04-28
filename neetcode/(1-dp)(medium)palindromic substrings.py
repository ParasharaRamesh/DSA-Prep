'''
Given a string s, return the number of substrings within s that are palindromes.

A palindrome is a string that reads the same forward and backward.

Example 1:

Input: s = "abc"

Output: 3
Explanation: "a", "b", "c".

Example 2:

Input: s = "aaa"

Output: 6
Explanation: "a", "a", "a", "aa", "aa", "aaa". Note that different substrings are counted as different palindromes even if the string contents are the same.

Constraints:

1 <= s.length <= 1000
s consists of lowercase English letters.
'''


class Solution:
    #with center at one of the indexes, do two pointer and keep counting
    def countSubstrings(self, s: str) -> int:
        count = 0
        for i in range(len(s)):
            odd_count = self.count_palindromes(i,i,s)
            even_count = self.count_palindromes(i,i+1,s)
            count += odd_count + even_count
        return count

    def count_palindromes(self, l, r, s):
        m = len(s)
        count = 0
        while l >= 0 and r < m and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
        return count