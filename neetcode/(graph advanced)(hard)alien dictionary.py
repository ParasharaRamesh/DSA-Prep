'''
There is a foreign language which uses the latin alphabet, but the order among letters is not "a", "b", "c" ... "z" as in English.

You receive a list of non-empty strings words from the dictionary, where the words are sorted lexicographically based on the rules of this new language.

Derive the order of letters in this language. If the order is invalid, return an empty string. If there are multiple valid order of letters, return any of them.

A string a is lexicographically smaller than a string b if either of the following is true:

The first letter where they differ is smaller in a than in b.
There is no index i such that a[i] != b[i] and a.length < b.length.
Example 1:

Input: ["z","o"]

Output: "zo"
Explanation:
From "z" and "o", we know 'z' < 'o', so return "zo".

Example 2:

Input: ["hrn","hrf","er","enn","rfnn"]

Output: "hernf"
Explanation:

from "hrn" and "hrf", we know 'n' < 'f'
from "hrf" and "er", we know 'h' < 'e'
from "er" and "enn", we know get 'r' < 'n'
from "enn" and "rfnn" we know 'e'<'r'
so one possibile solution is "hernf"
Constraints:

The input words will contain characters only from lowercase 'a' to 'z'.
1 <= words.length <= 100
1 <= words[i].length <= 100
'''
from itertools import zip_longest
from typing import List


class Solution:
    def foreignDictionary(self, words: List[str]) -> str:
        # find all unique chars first
        all_chars = set()
        for word in words:
            all_chars = all_chars.union(set(word))

        # use unique chars to form nodes of graph
        graph = {char: set() for char in all_chars}

        for i in range(1, len(words)):
            w1 = words[i - 1]
            w2 = words[i]

            # only goes till lower of two lengths
            for c1, c2 in zip_longest(w1, w2):
                if c1 != c2:
                    #invalid case since the provided lexographically ordered string itself is not valid
                    if c1 != None and c2 == None:
                        return ""
                    elif c1 != None and c2 != None:
                        graph[c1].add(c2)
                    break

        # do topological sort of graph
        return self.toposort(graph, all_chars)

    def toposort(self, graph, all_chars) -> str:
        topo = ""
        indegree = {char: 0 for char in all_chars}

        # build indegree
        for k, vs in graph.items():
            for v in vs:
                indegree[v] += 1

        # helper nested function
        def dfs(node):
            nonlocal topo, indegree

            # add to topo first
            topo += node

            # decrement indegree
            indegree[node] -= 1

            # for each neighbour
            for neighbor in graph[node]:
                # decrement indegree first since its parent was removed
                indegree[neighbor] -= 1

                # if the indegree is 0 then you dfs from there and do topo sort
                if indegree[neighbor] == 0:
                    dfs(neighbor)

        # for all zero nodes
        for c in indegree:
            if indegree[c] == 0:
                dfs(c)

        if len(topo) == len(all_chars):
            return topo
        else:
            # illegal / unable to topo sort
            return ""


if __name__ == '__main__':
    s = Solution()

    words = ["abc", "ab"]
    res = s.foreignDictionary(words)
    expected = ""
    assert res == expected, f"expected {expected}, got {res}"

    words = ["wrtkj", "wrt"]
    res = s.foreignDictionary(words)
    expected = ""
    assert res == expected, f"expected {expected}, got {res}"

    words = ["wrt", "wrf", "er", "ett", "rftt"]
    res = s.foreignDictionary(words)
    expected = "wertf"
    assert res == expected, f"expected {expected}, got {res}"

    words = ["z", "x", "z"]
    res = s.foreignDictionary(words)
    expected = ""
    assert res == expected, f"expected {expected}, got {res}"

    words = ["hrn", "hrf", "er", "enn", "rfnn"]
    res = s.foreignDictionary(words)
    expected = "hernf"
    assert res == expected, f"expected {expected}, got {res}"
