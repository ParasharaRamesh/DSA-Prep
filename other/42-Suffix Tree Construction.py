class SuffixTrie:
    def __init__(self, string):
        self.root = {}
        self.endSymbol = "*"
        self.populateSuffixTrieFrom(string)

    def populateSuffixTrieFrom(self, string):
        suffixToBeInsertedStartingFromIndex = 0

        while suffixToBeInsertedStartingFromIndex < len(string):
            currNode = self.root
            for ch in string[suffixToBeInsertedStartingFromIndex:]:
                if ch not in currNode:
                    currNode[ch] = dict()
                currNode = currNode[ch]
            currNode[self.endSymbol] = True
            suffixToBeInsertedStartingFromIndex += 1

    def contains(self, string):
        currNode = self.root

        for i, ch in enumerate(string):
            if ch not in currNode:
                return False
            # traverse
            currNode = currNode[ch]

        # leaf node
        return self.endSymbol in currNode


if __name__ == '__main__':
    pass
