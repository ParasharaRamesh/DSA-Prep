'''
Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

 

Example 1:

Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
Output: ["cats and dog","cat sand dog"]
Example 2:

Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
Explanation: Note that you are allowed to reuse a dictionary word.
Example 3:

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: []
 

Constraints:

1 <= s.length <= 20
1 <= wordDict.length <= 1000
1 <= wordDict[i].length <= 10
s and wordDict[i] consist of only lowercase English letters.
All the strings of wordDict are unique.
Input is generated in a way that the length of the answer doesn't exceed 105.
'''

from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

    def __repr__(self):
        return f"Node(children={self.children}, end={self.end})"

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        n = len(s)

        # trie construction
        root = TrieNode()

        for word in wordDict:
            curr = root
            for ch in word:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
            curr.end = True

        res = []

        def f(i, parts):
            nonlocal res

            if i == n:
                parts = " ".join(parts)
                res.append(parts)
                return 

            # traverse from root together
            checkpoints = [] #[(j, word[i:j+1]),..]

            j = i
            curr = root
            acc = ""

            while j < n and s[j] in curr.children:
                curr = curr.children[s[j]]
                acc += s[j]
                j += 1
                
                if curr.end:
                    checkpoints.append((j, acc))

            for checkpoint in checkpoints:
                new_i, acc_word = checkpoint
                f(new_i, parts + [acc_word])

        f(0, [])
        return res

if __name__ == "__main__":
    sol = Solution()

    s = "catsandog"
    wordDict = ["cats","dog","sand","and","cat"]
    expected = []
    res = sol.wordBreak(s, wordDict)
    assert set(res) == set(expected), f"{s=} {wordDict=} | {res=} {expected=}"

    s = "catsanddog"
    wordDict = ["cat","cats","and","sand","dog"]
    expected = ["cats and dog","cat sand dog"]
    res = sol.wordBreak(s, wordDict)
    assert set(res) == set(expected), f"{s=} {wordDict=} | {res=} {expected=}"

    s = "pineapplepenapple"
    wordDict = ["apple","pen","applepen","pine","pineapple"]
    expected = ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
    res = sol.wordBreak(s, wordDict)
    assert set(res) == set(expected), f"{s=} {wordDict=} | {res=} {expected=}"

