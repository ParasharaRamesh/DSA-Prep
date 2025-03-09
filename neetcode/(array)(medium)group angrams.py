'''
Given an array of strings strs, group the anagrams together. You can return the answer in any order.


Example 1:

Input: strs = ["eat","tea","tan","ate","nat","bat"]

Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
'''

from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = defaultdict(list)

        for s in strs:
            ch_str = [0] * 26
            for ch in s:
                ch_str[ord(ch) - ord('a')] += 1

            anagrams[tuple(ch_str)].append(s)

        return list(anagrams.values())

