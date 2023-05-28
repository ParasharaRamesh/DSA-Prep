class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.links = {}

def searchTrie(root, string):
    #first char is always a match
    curr = root

    for ch in string[1:]:
        if ch in curr.links:
            curr = curr.links[ch]
        else:
            return False
    return True

def constructTrie(root, words):
    #its known that root has the first char
    root.value = words[0][0]

    for word in words:
        curr = root
        for ch in word[1:]:
            if ch not in curr.links:
                curr.links[ch] = TrieNode(ch)
            curr = curr.links[ch]

def multiStringSearch(bigString, smallStrings):
    tries = dict()

    startingCharsForSmallStrings = set()
    for smallString in smallStrings:
        startingCharsForSmallStrings.add(smallString[0])

    startingIndices = dict()
    for i, ch in enumerate(bigString):
        if ch in startingCharsForSmallStrings:
            tries[ch] = TrieNode()
            if ch not in startingIndices:
                startingIndices[ch] = [i]
            else:
                startingIndices[ch].append(i)

    for ch in startingIndices:
        words = [bigString[index:] for index in startingIndices[ch]]
        constructTrie(tries[ch], words)

    # search the correct trie and return
    results = []
    for smallString in smallStrings:
        ch = smallString[0]
        if ch not in tries:
            results.append(False)
        else:
            results.append(searchTrie(tries[ch], smallString))
    return results


if __name__ == '__main__':
    bigString = "this is a big string"
    smallStrings = ["this", "yo", "is", "a", "bigger", "string", "kappa"]
    print(multiStringSearch(bigString, smallStrings))
