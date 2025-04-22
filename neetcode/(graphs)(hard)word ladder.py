'''
You are given two words, beginWord and endWord, and also a list of words wordList. All of the given words are of the same length, consisting of lowercase English letters, and are all distinct.

Your goal is to transform beginWord into endWord by following the rules:

You may transform beginWord to any word within wordList, provided that at exactly one position the words have a different character, and the rest of the positions have the same characters.
You may repeat the previous step with the new word that you obtain, and you may do this as many times as needed.
Return the minimum number of words within the transformation sequence needed to obtain the endWord, or 0 if no such sequence exists.

Example 1:

Input: beginWord = "cat", endWord = "sag", wordList = ["bat","bag","sag","dag","dot"]

Output: 4
Explanation: The transformation sequence is "cat" -> "bat" -> "bag" -> "sag".

Example 2:

Input: beginWord = "cat", endWord = "sag", wordList = ["bat","bag","sat","dag","dot"]

Output: 0
Explanation: There is no possible transformation sequence from "cat" to "sag" since the word "sag" is not in the wordList.

Constraints:

1 <= beginWord.length <= 10
1 <= wordList.length <= 100

'''
from typing import List
from collections import deque


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # trivial case endWord not in wordList
        if endWord not in wordList:
            return 0

        # construct graph
        wordList.append(beginWord)
        graph = {word: [] for word in wordList}

        for i in range(len(wordList)-1):
            for j in range(i+1, len(wordList)):
                word1 = wordList[i]
                word2 = wordList[j]

                edit_distance = 0
                for c1, c2 in zip(word1, word2):
                    if c1 != c2:
                        edit_distance += 1

                if edit_distance == 1:
                    graph[word1].append(word2)
                    graph[word2].append(word1)

        # do bfs
        visited = set()

        frontier = deque([(beginWord, 1)])

        while frontier:
            curr_word, count = frontier.popleft()

            if curr_word not in visited:
                visited.add(curr_word)

            #found it: the first time we find it will be the shortest anyway because of bfs
            if curr_word == endWord:
                return count

            for neighbour in graph[curr_word]:
                if neighbour not in visited:
                    frontier.append((neighbour, count + 1))

        # if not found return 0
        return 0