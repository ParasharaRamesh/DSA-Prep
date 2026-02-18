'''
A disjoint set refers to a collection of sets where no two sets share any common elements—meaning the intersection of any two sets is the empty set (ϕ).  In the context of the Union-Find data structure, this concept is operationalized to manage a partition of elements into non-overlapping subsets, where each subset has a representative (often its root) that identifies the group. 

Philosophically, a disjoint set embodies the idea of mutual exclusivity and identity: each element belongs to exactly one group, and the structure maintains this separation while allowing efficient merging (union) and identification (find) of group membership. It reflects a dynamic system where relationships evolve—elements start isolated, then are connected through union operations—yet the core principle remains: no element can belong to more than one set at a time.  This mirrors real-world scenarios like connected components in networks, where connectivity is binary (either connected or not), and the system must track these relationships efficiently
'''
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
    # Demonstration of four variants with small, readable examples

    # 1) Baseline Union-Find (no optimizations)
    print("\n" + "="*50)
    print("1) Baseline Union-Find Demonstration (No Optimizations)")
    print("="*50)
    uf = UnionFind()
    print("\n--- Creating sets ---")
    for x in [1, 2, 3, 4, 5]:
        uf.create_set(x)
        print(f"Created set for {x}, root: {uf.find(x)}")
    
    print("\n--- Performing unions ---")
    uf.union(1, 2)
    print(f"Union(1, 2): Root of 1: {uf.find(1)}, Root of 2: {uf.find(2)}")
    
    uf.union(3, 4)
    print(f"Union(3, 4): Root of 3: {uf.find(3)}, Root of 4: {uf.find(4)}")
    
    uf.union(2, 3)
    print(f"Union(2, 3): Root of 2: {uf.find(2)}, Root of 3: {uf.find(3)}")
    print(f"After Union(2, 3): Root of 1: {uf.find(1)}, Root of 4: {uf.find(4)}")
    
    print("\n--- Connection checks ---")
    print("Baseline connected(1, 4):", uf.connected(1, 4))  # True
    print("Baseline connected(1, 5):", uf.connected(1, 5))  # False
    print("Baseline connected(2, 3):", uf.connected(2, 3))  # True
    
    print("\n--- Final roots ---")
    for x in [1, 2, 3, 4, 5]:
        print(f"Root of {x}: {uf.find(x)}")

    # 2) Path Compression Union-Find
    print("\n" + "="*50)
    print("2) Path Compression Union-Find Demonstration")
    print("="*50)
    uf_pc = PathCompressionUnionFind()
    print("\n--- Creating sets ---")
    for x in [1, 2, 3, 4, 5]:
        uf_pc.create_set(x)
        print(f"Created set for {x}, root: {uf_pc.find(x)}")
    
    print("\n--- Performing unions ---")
    uf_pc.union(1, 2)
    print(f"Union(1, 2): Root of 1: {uf_pc.find(1)}, Root of 2: {uf_pc.find(2)}")
    
    uf_pc.union(3, 4)
    print(f"Union(3, 4): Root of 3: {uf_pc.find(3)}, Root of 4: {uf_pc.find(4)}")
    
    uf_pc.union(2, 3)
    print(f"Union(2, 3): Root of 2: {uf_pc.find(2)}, Root of 3: {uf_pc.find(3)}")
    
    print("\n--- Before path compression ---")
    print(f"Root of 4 before find: {uf_pc.find(4)}")
    print("Calling find(4) to trigger path compression...")
    root_4 = uf_pc.find(4)
    print(f"Root of 4 after path compression: {root_4}")
    
    print("\n--- After path compression ---")
    print(f"Root of 1: {uf_pc.find(1)}, Root of 2: {uf_pc.find(2)}")
    print(f"Root of 3: {uf_pc.find(3)}, Root of 4: {uf_pc.find(4)}")
    
    print("\n--- Connection checks ---")
    print("PathCompression connected(1, 4):", uf_pc.connected(1, 4))  # True
    print("PathCompression connected(4, 5):", uf_pc.connected(4, 5))  # False
    print("PathCompression connected(2, 3):", uf_pc.connected(2, 3))  # True
    
    print("\n--- Final roots (all paths compressed) ---")
    for x in [1, 2, 3, 4, 5]:
        print(f"Root of {x}: {uf_pc.find(x)}")

    # 3) Rank-based Union-Find (no path compression)
    print("\n" + "="*50)
    print("3) Rank-based Union-Find Demonstration")
    print("="*50)
    uf_rank = RankUnionFind()
    print("\n--- Creating sets ---")
    for x in [1, 2, 3, 4, 5]:
        uf_rank.create_set(x)
        print(f"Created set for {x}, root: {uf_rank.find(x)}, rank: {uf_rank.rank.get(x, 0)}")
    
    print("\n--- Performing unions ---")
    uf_rank.union(1, 2)
    root_1 = uf_rank.find(1)
    root_2 = uf_rank.find(2)
    print(f"Union(1, 2): Root of 1: {root_1}, rank: {uf_rank.rank.get(root_1, 0)}")
    print(f"Union(1, 2): Root of 2: {root_2}, rank: {uf_rank.rank.get(root_2, 0)}")
    
    uf_rank.union(3, 4)
    root_3 = uf_rank.find(3)
    root_4 = uf_rank.find(4)
    print(f"Union(3, 4): Root of 3: {root_3}, rank: {uf_rank.rank.get(root_3, 0)}")
    print(f"Union(3, 4): Root of 4: {root_4}, rank: {uf_rank.rank.get(root_4, 0)}")
    
    uf_rank.union(2, 3)
    root_1_final = uf_rank.find(1)
    root_3_final = uf_rank.find(3)
    print(f"Union(2, 3): Root of 1: {root_1_final}, rank: {uf_rank.rank.get(root_1_final, 0)}")
    print(f"Union(2, 3): Root of 3: {root_3_final}, rank: {uf_rank.rank.get(root_3_final, 0)}")
    print(f"Union(2, 3): Root of 2: {uf_rank.find(2)}, Root of 4: {uf_rank.find(4)}")
    
    print("\n--- Connection checks ---")
    print("Rank connected(1, 4):", uf_rank.connected(1, 4))  # True
    print("Rank connected(3, 5):", uf_rank.connected(3, 5))  # False
    print("Rank connected(2, 3):", uf_rank.connected(2, 3))  # True
    
    print("\n--- Final roots and ranks ---")
    for x in [1, 2, 3, 4, 5]:
        root = uf_rank.find(x)
        print(f"Node {x}: Root = {root}, Rank of root = {uf_rank.rank.get(root, 0)}")

    # 4) Size-based Union-Find (union by size)
    print("\n" + "="*50)
    print("4) Size-based Union-Find Demonstration")
    print("="*50)
    uf_size = SizeUnionFind()
    for x in [1, 2, 3, 4, 5, 6]:
        uf_size.create_set(x)
        print(f"Created set for {x}, size: {uf_size.get_size(x)}")
    
    print("\n--- Performing unions ---")
    uf_size.union(1, 2)
    print(f"Union(1, 2): Size of component containing 1: {uf_size.get_size(1)}")
    print(f"Union(1, 2): Size of component containing 2: {uf_size.get_size(2)}")
    
    uf_size.union(3, 4)
    print(f"Union(3, 4): Size of component containing 3: {uf_size.get_size(3)}")
    print(f"Union(3, 4): Size of component containing 4: {uf_size.get_size(4)}")
    
    uf_size.union(2, 3)
    print(f"Union(2, 3): Size of component containing 1: {uf_size.get_size(1)}")
    print(f"Union(2, 3): Size of component containing 2: {uf_size.get_size(2)}")
    print(f"Union(2, 3): Size of component containing 3: {uf_size.get_size(3)}")
    print(f"Union(2, 3): Size of component containing 4: {uf_size.get_size(4)}")
    
    uf_size.union(5, 6)
    print(f"Union(5, 6): Size of component containing 5: {uf_size.get_size(5)}")
    print(f"Union(5, 6): Size of component containing 6: {uf_size.get_size(6)}")
    
    print("\n--- Connection checks ---")
    print("Size connected(1, 4):", uf_size.connected(1, 4))  # True
    print("Size connected(1, 5):", uf_size.connected(1, 5))  # False
    print("Size connected(3, 5):", uf_size.connected(3, 5))  # False
    print("Size connected(5, 6):", uf_size.connected(5, 6))  # True
    
    print("\n--- Final component sizes ---")
    print(f"Component containing 1 has size: {uf_size.get_size(1)}")  # Should be 4
    print(f"Component containing 5 has size: {uf_size.get_size(5)}")  # Should be 2
    print(f"Component containing 6 has size: {uf_size.get_size(6)}")  # Should be 2