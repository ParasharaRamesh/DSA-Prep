'''
Design a data structure that supports adding new words and searching for existing words.

Implement the WordDictionary class:

void addWord(word) Adds word to the data structure.
bool search(word) Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots '.' where dots can be matched with any letter.
Example 1:

Input:
["WordDictionary", "addWord", "day", "addWord", "bay", "addWord", "may", "search", "say", "search", "day", "search", ".ay", "search", "b.."]

Output:
[null, null, null, null, false, true, true, true]

Explanation:
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("day");
wordDictionary.addWord("bay");
wordDictionary.addWord("may");
wordDictionary.search("say"); // return false
wordDictionary.search("day"); // return true
wordDictionary.search(".ay"); // return true
wordDictionary.search("b.."); // return true
Constraints:

1 <= word.length <= 20
word in addWord consists of lowercase English letters.
word in search consist of '.' or lowercase English letters.

'''


class Node:
    def __init__(self, is_end=False):
        self.is_end = is_end
        self.chars = dict()


class WordDictionary:
    def __init__(self):
        self.root = Node()

    def addWord(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.chars:
                curr.chars[ch] = Node()
            curr = curr.chars[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root

        def helper(curr, word):
            if len(word) == 0:
                return curr.is_end

            ch = word[0]
            if ch != ".":
                if ch not in curr.chars:
                    return False

                return helper(curr.chars[ch], word[1:])

            for link in curr.chars:
                if helper(curr.chars[link], word[1:]):
                    return True

            return False

        return helper(curr, word)

