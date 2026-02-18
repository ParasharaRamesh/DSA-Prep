"""
Trie (Prefix Tree) - Interview reference implementation.
Supports duplicate words via end_count per node.
"""


class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.is_end = False  # True if at least one word ends here
        self.end_count = 0   # Number of words ending at this node (handles duplicates)


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word. Duplicate inserts are counted (end_count)."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.end_count += 1

    def search(self, word: str) -> bool:
        """True if the exact word exists (inserted at least once)."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def count_word(self, word: str) -> int:
        """Return how many times this exact word was inserted. 0 if not a word."""
        node = self._find_node(word)
        return node.end_count if node else 0

    def starts_with(self, prefix: str) -> bool:
        """True if any word has the given prefix."""
        return self._find_node(prefix) is not None

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count all words that have the given prefix (prefix itself counts if it's a word)."""
        node = self._find_node(prefix)
        if node is None:
            return 0
        return self._count_words_from(node)

    def _count_words_from(self, node: TrieNode) -> int:
        """Sum end_count in this node and all descendants (DFS)."""
        total = node.end_count
        for child in node.children.values():
            total += self._count_words_from(child)
        return total

    def get_all_words_with_prefix(self, prefix: str) -> list[str]:
        """Return list of all words that start with the given prefix."""
        node = self._find_node(prefix)
        if node is None:
            return []
        result = []
        self._collect_words(node, prefix, result)
        return result

    def _collect_words(self, node: TrieNode, path: str, result: list[str]) -> None:
        if node.is_end:
            for _ in range(node.end_count):
                result.append(path)
        for char, child in sorted(node.children.items()):
            self._collect_words(child, path + char, result)

    def delete(self, word: str) -> bool:
        """
        Remove one occurrence of the word. Returns True if a word was removed.
        Does not prune nodes (keeps structure); only decrements end_count.
        """
        node = self._find_node(word)
        if node is None or node.end_count == 0:
            return False
        node.end_count -= 1
        if node.end_count == 0:
            node.is_end = False
        return True

    def delete_all(self, word: str) -> bool:
        """Remove all occurrences of the word. Returns True if any were removed."""
        node = self._find_node(word)
        if node is None or node.end_count == 0:
            return False
        node.end_count = 0
        node.is_end = False
        return True

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Return the node at the end of prefix, or None if prefix not in trie."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def total_word_count(self) -> int:
        """Total number of word insertions (counting duplicates)."""
        return self.count_words_with_prefix("")

    def longest_prefix_of(self, word: str) -> str:
        """Longest prefix of `word` that is a word in the trie. Empty string if none."""
        node = self.root
        last_end = 0
        for i, char in enumerate(word):
            if char not in node.children:
                break
            node = node.children[char]
            if node.is_end:
                last_end = i + 1
        return word[:last_end]


# --- Backward compatibility (common API) ---
Trie.startsWith = Trie.starts_with  # type: ignore


# --- Example / quick test ---
if __name__ == "__main__":
    t = Trie()
    t.insert("apple")
    t.insert("apple")
    t.insert("app")
    t.insert("apply")
    t.insert("app")

    assert t.search("apple") is True
    assert t.search("app") is True
    assert t.count_word("apple") == 2
    assert t.count_word("app") == 2
    assert t.count_word("apply") == 1
    assert t.starts_with("ap") is True
    assert t.count_words_with_prefix("app") == 5   # apple*2 + app*2 + apply
    assert t.count_words_with_prefix("appl") == 3  # apple*2 + apply
    assert set(t.get_all_words_with_prefix("app")) == {"apple", "app", "apply"}

    t.delete("app")
    assert t.count_word("app") == 1
    t.delete_all("apple")
    assert t.count_word("apple") == 0

    assert t.longest_prefix_of("application") == "app"
    assert t.longest_prefix_of("xyz") == ""

    print("Trie checks passed.")
