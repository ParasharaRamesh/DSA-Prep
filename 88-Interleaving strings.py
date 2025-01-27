'''
Leetcode 97: Interleaving String

Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m
substrings
 respectively, such that:

s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
|n - m| <= 1
The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...
Note: a + b is the concatenation of strings a and b.


'''
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

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

if __name__ == '__main__':
    s1 = "aa"
    s2 = "bb"
    s3 = "abba"

    s = Solution()
    print(s.isInterleave(s1, s2, s3))
