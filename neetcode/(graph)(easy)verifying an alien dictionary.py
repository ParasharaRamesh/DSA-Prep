'''
In an alien language, surprisingly, they also use English lowercase letters, but possibly in a different order. The order of the alphabet is some permutation of lowercase letters.

Given a sequence of words written in the alien language, and the order of the alphabets, return true if and only if the given words are sorted lexicographically in this alien language.

Example 1:

Input: words = ["dag","disk","dog"], order = "hlabcdefgijkmnopqrstuvwxyz"

Output: true
Explanation: The first character of the strings are same ('d'). 'a', 'i', 'o' follows the given ordering, which makes the given strings follow the sorted lexicographical order.

Example 2:

Input: words = ["neetcode","neet"], order = "worldabcefghijkmnpqstuvxyz"

Output: false
Explanation: The first 4 characters of both the strings match. But size of "neet" is less than that of "neetcode", so "neet" should come before "neetcode".

Constraints:

1 <= words.length <= 100
1 <= words[i].length <= 20
order.length == 26
All characters in words[i] and order are English lowercase letters.
'''
from itertools import zip_longest
from typing import List


class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        for i in range(1, len(words)):
            if not self.check(words[i-1], words[i], order):
                return False

        return True

    def check(self, word1, word2, order):
        for c1, c2 in zip_longest(word1, word2, fillvalue=None):
            if not c1 and c2:
                return True
            elif c1 and not c2:
                return False

            i1 = order.index(c1)
            i2 = order.index(c2)

            if i1 > i2:
                return False
            elif i1 < i2:
                return True

        return True


if __name__ == '__main__':
    s = Solution()

    expected = True
    words = ["hello", "leetcode"]
    order = "hlabcdefgijkmnopqrstuvwxyz"
    actual = s.isAlienSorted(words, order)
    assert expected == actual, f"{expected = }, {actual = }"

    expected = True
    words = ["dag", "disk", "dog"]
    order = "hlabcdefgijkmnopqrstuvwxyz"
    actual = s.isAlienSorted(words, order)
    assert expected == actual, f"{expected = }, {actual = }"

    expected = False
    words = ["neetcode", "neet"]
    order = "worldabcefghijkmnpqstuvxyz"
    actual = s.isAlienSorted(words, order)
    assert expected == actual, f"{expected = }, {actual = }"

    expected = False
    words = ["word", "world", "row"]
    order = "worldabcefghijkmnpqstuvxyz"
    actual = s.isAlienSorted(words, order)
    assert expected == actual, f"{expected = }, {actual = }"

    expected = False
    words = ["word", "world", "row"]
    order = "worldabcefghijkmnpqstuvxyz"
    actual = s.isAlienSorted(words, order)
    assert expected == actual, f"{expected = }, {actual = }"
