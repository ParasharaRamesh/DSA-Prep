'''
Given a 2-D grid of characters board and a list of strings words, return all words that are present in the grid.

For a word to be present it must be possible to form the word with a path in the board with horizontally or vertically neighboring cells. The same cell may not be used more than once in a word.

Example 1:



Input:
board = [
  ["a","b","c","d"],
  ["s","a","a","t"],
  ["a","c","k","e"],
  ["a","c","d","n"]
],
words = ["bat","cat","back","backend","stack"]

Output: ["cat","back","backend"]
Example 2:



Input:
board = [
  ["x","o"],
  ["x","o"]
],
words = ["xoxo"]

Output: []
Constraints:

1 <= board.length, board[i].length <= 10
board[i] consists only of lowercase English letter.
1 <= words.length <= 100
1 <= words[i].length <= 10
words[i] consists only of lowercase English letters.
All strings within words are distinct.

Insights:
* make a trie of all the words
* find out all starting indices of all starting chars
* do dfs + trie traversal

'''
from typing import List
from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = dict()
        self.is_end = False


class Solution:
    # helper method
    def create_trie_from_words(self, words):
        root = TrieNode()

        for word in words:
            curr = root
            for ch in word:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
            curr.is_end = True

        return root

    # main method
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # 1. find all the places where the starting chars start in the board
        starting_chars = set([word[0] for word in words])
        root_char_inds = defaultdict(list)

        m = len(board)
        n = len(board[0])

        for i in range(m):
            for j in range(n):
                ch = board[i][j]
                if ch in starting_chars:
                    root_char_inds[ch].append((i, j))

        # 2. create trie with all of the words
        root = self.create_trie_from_words(words)

        # 3. do multi source dfs
        res = set()

        '''
        do dfs from the starting position based on whatever is present in the trie, return early if nothing is there
        '''

        def get_valid_neighbour_positions(x, y, visited):
            is_valid_position = lambda i, j: 0 <= i < m and 0 <= j < n
            is_visited = lambda i, j: (i, j) in visited

            delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            positions = []

            for dx, dy in delta:
                nx, ny = x + dx, y + dy
                if not is_visited(nx, ny) and is_valid_position(nx, ny):
                    positions.append((nx, ny))

            return positions

        def dfs(pos, node, word, visited):
            i, j = pos
            ch = board[i][j]

            if ch not in node.children:
                # early stop
                return

            word += ch
            node = node.children[ch]

            if node.is_end:
                res.add(word)

            neighbour_pos = get_valid_neighbour_positions(i, j, visited)
            for ni, nj in neighbour_pos:
                n_ch = board[ni][nj]

                if n_ch in node.children:
                    # only for this path is this position added
                    visited_copy = visited.copy()
                    visited_copy.add(pos)

                    dfs((ni, nj), node, word, visited_copy)

                    # calling the dfs

        for positions in root_char_inds.values():
            for start_position in positions:
                # early stop since we found out all the words
                if len(res) == len(words):
                    return words

                dfs(start_position, root, "", set())

        return list(res)

if __name__ == '__main__':
    s = Solution()

    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"]
    ]
    words = ["oath","pea","eat","rain","oathi","oathk","oathf","oate","oathii","oathfi","oathfii"]
    res = s.findWords(board, words)
    expected = set(["oath","oathk","oathf","oathfi","oathfii","oathi","oathii","oate","eat"])
    print(res)
    assert set(res) == expected, f"{res} != {expected}"


    board = [
        ["a", "b", "c", "d"],
        ["s", "a", "a", "t"],
        ["a", "c", "k", "e"],
        ["a", "c", "d", "n"]
    ]
    words = ["bat", "cat", "back", "backend", "stack"]
    res = s.findWords(board, words) # Output: ["cat", "back", "backend"]
    print(res)
