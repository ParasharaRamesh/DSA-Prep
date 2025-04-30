'''
Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of dictionary words.

You are allowed to reuse words in the dictionary an unlimited number of times. You may assume all dictionary words are unique.

Example 1:

Input: s = "neetcode", wordDict = ["neet","code"]

Output: true
Explanation: Return true because "neetcode" can be split into "neet" and "code".

Example 2:

Input: s = "applepenapple", wordDict = ["apple","pen","ape"]

Output: true
Explanation: Return true because "applepenapple" can be split into "apple", "pen" and "apple". Notice that we can reuse words and also not use all the words.

Example 3:

Input: s = "catsincars", wordDict = ["cats","cat","sin","in","car"]

Output: false
'''
from builtins import str
from typing import List


class Solution:
    # topdown - space inefficient
    def wordBreak_memo_extra_space(self, s: str, wordDict: List[str]) -> bool:
        cache = dict()

        def helper(s):
            key = s

            if key in cache:
                return cache[key]

            if len(s) == 0:
                cache[key] = True
                return True

            can = False
            for word in wordDict:
                if s.startswith(word):
                    can = can or helper(s[len(word):])

            cache[key] = can
            return can

        return helper(s)

    # top down space efficient
    def wordBreak_memo(self, s, wordDict):
        cache = dict()

        def helper(i):
            if i in cache:
                return cache[i]

            if i >= len(s):
                cache[i] = True
                return True

            # go through every word
            res = False
            for word in wordDict:
                # if at all it starts with same starting char
                if word[0] == s[i]:
                    _i = i
                    while _i < len(s) and _i - i < len(word) and s[_i] == word[_i - i]:
                        _i += 1

                    # only if the whole word was traversed it is possible else it is false
                    if _i - i == len(word):
                        res = res or helper(_i)

            cache[i] = res
            return res

        return helper(0)

    # bottom up
    def wordBreak(self, s, wordDict):
        cache = dict()

        cache[len(s)] = True

        for i in range(len(s) - 1, -1, -1):
            res = False
            for word in wordDict:
                # if at all it starts with same starting char
                if word[0] == s[i]:
                    _i = i
                    while _i < len(s) and _i - i < len(word) and s[_i] == word[_i - i]:
                        _i += 1

                    # only if the whole word was traversed it is possible else it is false
                    if _i - i == len(word):
                        res = res or cache[_i]

            cache[i] = res

        return cache[0]


if __name__ == '__main__':
    s = Solution()

    str = "catsincars"
    wordDict = ["cats", "cat", "sin", "in", "car"]
    expected = False
    actual = s.wordBreak(str, wordDict)
    assert expected == actual, f"expected: {expected}, actual: {actual}"

    str = "neetcode"
    wordDict = ["neet", "code"]
    expected = True
    actual = s.wordBreak(str, wordDict)
    assert expected == actual, f"expected: {expected}, actual: {actual}"

    str = "neetcode"
    wordDict = ["neet", "cod"]
    expected = False
    actual = s.wordBreak(str, wordDict)
    assert expected == actual, f"expected: {expected}, actual: {actual}"

    str = "applepenapple"
    wordDict = ["apple", "pen", "ape"]
    expected = True
    actual = s.wordBreak(str, wordDict)
    assert expected == actual, f"expected: {expected}, actual: {actual}"
