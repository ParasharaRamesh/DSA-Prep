'''
You are given a 0-indexed string s and a dictionary of words dictionary. You have to break s into one or more non-overlapping substrings such that each substring is present in dictionary. There may be some extra characters in s which are not present in any of the substrings.

Return the minimum number of extra characters left over if you break up s optimally.


Example 1:

Input: s = "leetscode", dictionary = ["leet","code","leetcode"]
Output: 1
Explanation: We can break s in two substrings: "leet" from index 0 to 3 and "code" from index 5 to 8. There is only 1 unused character (at index 4), so we return 1.

Example 2:

Input: s = "sayhelloworld", dictionary = ["hello","world"]
Output: 3
Explanation: We can break s in two substrings: "hello" from index 3 to 7 and "world" from index 8 to 12. The characters at indices 0, 1, 2 are not used in any substring and thus are considered as extra characters. Hence, we return 3.
 

Constraints:

1 <= s.length <= 50
1 <= dictionary.length <= 50
1 <= dictionary[i].length <= 50
dictionary[i] and s consists of only lowercase English letters
dictionary contains distinct words

# Solution Insights:
# - Use DFS + memoization to find the minimum number of extra characters by either:
#   (a) skipping the current character (counting as extra),
#   (b) matching dictionary words starting at the current index.
# - Use a Trie for fast lookup of dictionary words as prefixes to optimize matching.
#
# Recurrence: For each index, try both skipping (add 1 to extra) and consuming any trie-matched words.
#
# Time Complexity:
#   O(N^2) with Trie optimization: For each position, search all possible substrings as prefixes (max word length L), leveraging Trie lookup and memoization (N = len(s)).


'''

from typing import List

class TrieNode:
    def __init__(self):
        self.children = dict()  # dictionary to store children nodes (character: TrieNode)
        self.is_end = False     # indicates if this node marks the end of a word

class Solution:
    # Build a Trie (prefix tree) from the list of dictionary words
    def create_trie(self, dictionary: List[str]) -> TrieNode:
        root = TrieNode()
        
        for word in dictionary:  # insert each word from dictionary into the trie
            node = root
            for c in word:
                if c not in node.children:
                    node.children[c] = TrieNode()  # create TrieNode if character path doesn't exist
                node = node.children[c]
            node.is_end = True  # mark the end of a word

        return root

    # Returns the minimum number of extra characters in s given a dictionary, using a Trie for optimization
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        trie = self.create_trie(dictionary)      # Build trie from dictionary
        cache = dict()                          # Memoization dict for dfs

        def dfs(i):
            if i in cache:                      # Return cached result if present
                return cache[i]

            if i == len(s):                     # Reached end of string
                cache[i] = 0
                return cache[i]

            curr = trie                         # Start from trie root for each position

            res = 1 + dfs(i + 1)                # Option 1: Treat current char as extra and skip

            for k in range(i, len(s)):
                if s[k] not in curr.children:   # If character not in current trie node, no valid word continues
                    break
                curr = curr.children[s[k]]      # Move to next trie node
                if curr.is_end:                 # If word ends here, try breaking and minimize extras
                    res = min(res, dfs(k+1))

            cache[i] = res                     # Store computed result
            return cache[i]

        return dfs(0)                          # Start DFS from beginning


    # Returns the minimum number of extra characters in s given a dictionary, using basic DP/recursion (without Trie)
    def minExtraChar_dp(self, s: str, dictionary: List[str]) -> int:
        words = set(dictionary)                # Use set for O(1) lookup
        cache = dict()                        # Memoization dict for dfs

        def dfs(i):
            if i in cache:                    # Return cached result if seen
                return cache[i]

            if i == len(s):                   # Base case: end of string
                cache[i] = 0
                return cache[i]

            res = 1 + dfs(i + 1)              # Option 1: skip current character (count as extra)

            for k in range(i, len(s)):
                word = s[i:k+1]               # Possible substring from i to k
                if word in words:             # If substring is a word, try breaking here
                    res = min(res, dfs(k+1))

            cache[i] = res                    # Memoize and return
            return cache[i]

        return dfs(0)                         # Start DFS from beginning

if __name__ == "__main__":

    tests = [
        ("abs", ["a", "ab"], 1),
        ("ab", ["abd"], 2),
        ("sab", ["a", "ab"], 1),
        ("ab", ["a", "ab"], 0),
        ("ab", ["a", "b", "ab"], 0),
        ("abd", ["abde", "bcdf"], 3),
        ("leetscode", ["leet","code","leetcode"], 1),
        ("sayhelloworld", ["hello","world"], 3)
    ]
    sol = Solution()

    for test in tests:
        s, dictionary, expected = test
        res = sol.minExtraChar(s, dictionary)
        assert res == expected, f"{s=} {dictionary=} {expected=} {res=}"
        print(f"passed {test=}")