class UnionFind:
    """
    Disjoint Set Union (Union-Find) with the baseline (no optimizations).

    - create_set(x): adds a new singleton set containing x
    - find(x): returns the representative (root) of x's set
    - union(a, b): merges the sets containing a and b (if distinct)
    - connected(a, b): True if a and b are in the same set
    """

    def __init__(self):
        self.parent = {}

    def create_set(self, value):
        """
        Create a standalone set for value if it does not exist yet.
        * Make all values point to None initially -> topmost nodes
        """
        if value not in self.parent:
            self.parent[value] = None

    def find(self, value):
        """
        Find the root representative without path compression.
        * Traverse up the tree until we reach the topmost node (None)
        * Return the parent/root. Which is that node which has a parent pointer as None (almost like linked list traversal)
        """
        if value not in self.parent:
            return None
        curr = value
        while self.parent[curr] is not None:
            curr = self.parent[curr]
        return curr

    def union(self, a, b):
        """Merge two sets (naive attach)."""
        root_a = self.find(a)
        root_b = self.find(b)
        # If either of the values are not in the set, then return
        if root_a is None or root_b is None:
            return
        if root_a != root_b:
            # Naively make root_b point to root_a -> basically make the parent of root_b point to root_a
            self.parent[root_b] = root_a

    def connected(self, a, b):
        """Return True if a and b belong to the same set."""
        root_a = self.find(a)
        root_b = self.find(b)
        return root_a is not None and root_a == root_b


class PathCompressionUnionFind(UnionFind):
    """
    Union-Find optimized with path compression.
    Path compression is applied in find(), flattening the tree for future queries.
    """

    def find(self, value):
        """Find with path compression (recursive)."""
        if value not in self.parent:
            return None
        
        # Find root similar to the normal baseline find function
        root = value
        while self.parent[root] is not None:
            root = self.parent[root]

        # Path compress -> make all the nodes point to the root
        curr = value
        while curr != root:
            parent_curr = self.parent[curr]
            self.parent[curr] = root
            curr = parent_curr if parent_curr is not None else root
        return root


class RankUnionFind(UnionFind):
    """
    Union-Find optimized with union by rank (approximate tree height).
    Does not apply path compression.
    """

    def __init__(self):
        super().__init__()
        self.rank = {}

    def create_set(self, value):
        """Create a standalone set and initialize rank to 0."""
        if value not in self.parent:
            self.parent[value] = None
            self.rank[value] = 0

    def union(self, a, b):
        """Merge by rank: attach smaller-rank tree under larger-rank tree."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a is None or root_b is None or root_a == root_b:
            return

        rank_a = self.rank.get(root_a, 0)
        rank_b = self.rank.get(root_b, 0)

        if rank_a < rank_b:
            self.parent[root_a] = root_b
        elif rank_a > rank_b:
            self.parent[root_b] = root_a
        else:
            # Same rank: pick one as new root and increase its rank
            self.parent[root_b] = root_a
            self.rank[root_a] = rank_a + 1

class SizeUnionFind(UnionFind):
    """
    Similar to UF by rank, instead of keeping track of the rank you can keep track of the size of components inside one connected component
    """
    def __init__(self):
        super().__init__()
        self.size = {}

    def create_set(self, value):
        """Create a standalone set and initialize rank to 0."""
        if value not in self.parent:
            self.parent[value] = None
            self.size[value] = 1 # there is one node in its own connected component so far

    def union(self, a, b):
        """Merge by size: attach smaller-size tree under larger-size tree."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a is None or root_b is None or root_a == root_b:
            return

        size_a = self.size.get(root_a, 0)
        size_b = self.size.get(root_b, 0)

        if size_a <= size_b:
            # make a's parent as b because a is smaller
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        elif size_a > size_b:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]

    def get_size(self, node) :
        """getting the size of the connected component node belongs to"""
        parent = self.find(node)
        return self.size[parent]

if __name__ == '__main__':
    # Demonstration of three variants with small, readable examples

    # 1) Baseline Union-Find (no optimizations)
    uf = UnionFind()
    for x in [1, 2, 3, 4, 5]:
        uf.create_set(x)
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(2, 3)
    # Expected: 1,2,3,4 connected; 5 separate
    print("Baseline connected(1,4):", uf.connected(1, 4))  # True
    print("Baseline connected(1,5):", uf.connected(1, 5))  # False

    # 2) Path Compression Union-Find
    uf_pc = PathCompressionUnionFind()
    for x in [1, 2, 3, 4, 5]:
        uf_pc.create_set(x)
    uf_pc.union(1, 2)
    uf_pc.union(3, 4)
    uf_pc.union(2, 3)
    # After a find, paths should be compressed
    _ = uf_pc.find(4)
    print("PathCompression connected(1,4):", uf_pc.connected(1, 4))  # True
    print("PathCompression connected(4,5):", uf_pc.connected(4, 5))  # False

    # 3) Rank-based Union-Find (no path compression)
    uf_rank = RankUnionFind()
    for x in [1, 2, 3, 4, 5]:
        uf_rank.create_set(x)
    uf_rank.union(1, 2)
    uf_rank.union(3, 4)
    uf_rank.union(2, 3)
    print("Rank connected(1,4):", uf_rank.connected(1, 4))  # True
    print("Rank connected(3,5):", uf_rank.connected(3, 5))  # False