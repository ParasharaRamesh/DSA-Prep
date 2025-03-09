'''
Given two strings s and t, return true if the two strings are anagrams of each other, otherwise return false.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

'''

from collections import Counter
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sc = Counter(s)
        tc = Counter(t)

        if len(sc) != len(tc):
            print("not same length")
            return False

        for sk, sn in sc.items():
            if sk not in tc:
                print(f"{sk} is not in t {t}")
                return False

            if sn != tc[sk]:
                print(f"count is not the same")
                return False

        return True
