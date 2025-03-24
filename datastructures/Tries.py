class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary mapping characters to TrieNodes
        self.isEnd = False  # True if this node marks the end of a word


class Trie:
    def __init__(self):
        self.root = TrieNode()  # The Trie always starts with an empty root node

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # Create a new TrieNode if it doesn't exist
            node = node.children[char]  # Move to the next node
        node.isEnd = True  # Mark the end of the word

    def search(self, word: str) -> bool:
        """Returns True if the exact word exists in the Trie."""
        node = self._findNode(word)
        return node is not None and node.isEnd  # Check if the node exists and is the end of a word

    def startsWith(self, prefix: str) -> bool:
        """Returns True if there is any word in the Trie that starts with the given prefix."""
        return self._findNode(prefix) is not None  # Just check if the node exists

    def _findNode(self, prefix: str) -> TrieNode:
        """Helper function to traverse the Trie and return the last node of the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None  # Prefix doesn't exist
            node = node.children[char]  # Move to the next node
        return node  # Return the last node of the prefix


# Example Usage:
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))    # True
print(trie.search("app"))      # False (because "app" itself is not a complete word)
print(trie.startsWith("app"))  # True (because "apple" starts with "app")

trie.insert("app")
print(trie.search("app"))      # True (now "app" is explicitly inserted)
