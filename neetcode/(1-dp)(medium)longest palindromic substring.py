'''
Given a string s, return the longest substring of s that is a palindrome.

A palindrome is a string that reads the same forward and backward.

If there are multiple palindromic substrings that have the same length, return any one of them.

Example 1:

Input: s = "ababd"

Output: "bab"
Explanation: Both "aba" and "bab" are valid answers.

Example 2:

Input: s = "abbc"

Output: "bb"
Constraints:

1 <= s.length <= 1000
s contains only digits and English letters.

'''


class Solution:

    # N2 solution starting each center, for O(N) solution refer to manachers algorithm
    def longestPalindrome_n2_sol(self, s):
        # consider each char as the centre and check outwards
        best = ""

        for i in range(len(s)):
            #odd length palindrome case with center at i
            odd = self.bestPalindromeWithStartingIndices(i, i, s)
            #even length palindrome case with center at i, i+1
            even = self.bestPalindromeWithStartingIndices(i, i + 1, s)
            best = max([best, odd, even], key=lambda x: len(x))

        return best

    def bestPalindromeWithStartingIndices(self, l, r, s):
        m = len(s)
        palindrome = ""
        while l >= 0 and r < m:
            #no match
            if s[l] != s[r]:
                break

            #if they match
            if l == r:
                #odd case
                palindrome = s[l]
            else:
                #even case
                palindrome = s[l] + palindrome + s[r]

            #move it
            l -= 1
            r += 1
        return palindrome