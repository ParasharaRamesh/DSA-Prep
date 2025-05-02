'''
You are given three strings s1, s2, and s3. Return true if s3 is formed by interleaving s1 and s2 together or false otherwise.

Interleaving two strings s and t is done by dividing s and t into n and m substrings respectively, where the following conditions are met

|n - m| <= 1, i.e. the difference between the number of substrings of s and t is at most 1.
s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
Interleaving s and t is s1 + t1 + s2 + t2 + ... or t1 + s1 + t2 + s2 + ...
You may assume that s1, s2 and s3 consist of lowercase English letters.

Example 1:



Input: s1 = "aaaa", s2 = "bbbb", s3 = "aabbbbaa"

Output: true
Explanation: We can split s1 into ["aa", "aa"], s2 can remain as "bbbb" and s3 is formed by interleaving ["aa", "aa"] and "bbbb".

Example 2:

Input: s1 = "", s2 = "", s3 = ""

Output: true
Example 3:

Input: s1 = "abc", s2 = "xyz", s3 = "abxzcy"

Output: false
Explanation: We can't split s3 into ["ab", "xz", "cy"] as the order of characters is not maintained.

Constraints:

0 <= s1.length, s2.length <= 50
0 <= s3.length <= 100
'''

class Solution:
    #my original solution
    def isInterleave_original(self, s1: str, s2: str, s3: str) -> bool:

        cache = dict()

        #left over s1, s2 and i which matches with s3, turn is either 1 or 2
        def helper(s1, s2, i, turn, n, m):
            key = (s1, s2, i, turn, n, m)
            if key in cache:
                return cache[(s1,s2,i,turn, n, m)]

            # base
            if s1 == "" and s2 == "":
                cache[key] = (abs(n - m) <= 1)
                return cache[key]

            # invalid cases
            if len(s1) == 0 and len(s2) > 0 and turn == 1:
                cache[key] = False
                return False

            if len(s1) > 0 and len(s2) == 0 and turn == 2:
                cache[key] = False
                return False

            # do something based on turn
            j = 0
            if turn == 1:
                # invalid cannot be formed
                if s1[0] != s3[i]:
                    cache[key] = False
                    return False

                all_poss = False
                while j < len(s1):
                    if s1[j] == s3[i+j]:
                        all_poss = all_poss or helper(s1[j+1:], s2, i + j + 1, 2, n+1, m)
                        j += 1
                    else:
                        break

                cache[key] = all_poss
                return all_poss
            elif turn == 2:
                if s2[0] != s3[i]:
                    cache[key] = False
                    return False

                all_poss = False
                while j < len(s2):
                    if s2[j] == s3[i+j]:
                        all_poss = all_poss or helper(s1, s2[j+1:], i + j + 1, 1, n, m+1)
                        j += 1
                    else:
                        break

                cache[key] = all_poss
                return all_poss

        n, m = 0,0
        return (len(s3) == len(s1) + len(s2)) and (helper(s1, s2, 0, 1, n, m) or helper(s1, s2, 0, 2, n, m))