'''
================================================================================
                    CYCLE DETECTION IN GRAPHS - COMPREHENSIVE GUIDE
================================================================================

This file contains all major approaches for detecting cycles in both directed
and undirected graphs. Each method is implemented with clear comments for
interview preparation.

================================================================================
                            UNDIRECTED GRAPHS
================================================================================

For undirected graphs, a cycle exists if we encounter an edge that connects
to an already-visited node that is NOT the immediate parent (i.e., a back edge).

METHOD 1: UNION-FIND (DISJOINT SET UNION)
------------------------------------------
Time: O(V * α(V)) where α is inverse Ackermann (practically O(V))
Space: O(V)

Approach:
- Initialize each node as its own set
- For each edge, check if both endpoints belong to the same set
- If they do, we found a cycle (edge connects nodes already connected)
- Otherwise, union the two sets
- Works well for sparse graphs and when you need to process edges incrementally

METHOD 2: DFS WITH PARENT TRACKING (Recursive)
-----------------------------------------------
Time: O(V + E)
Space: O(V) for recursion stack

Approach:
- Perform DFS traversal, tracking the parent of each node
- Mark nodes as visited
- If we encounter a visited neighbor that is NOT the parent, we found a cycle
- This is the most intuitive and commonly used method in interviews

METHOD 3: DFS WITH PARENT TRACKING (Iterative)
-----------------------------------------------
Time: O(V + E)
Space: O(V) for explicit stack

Approach:
- Same logic as recursive version but uses explicit stack
- Useful when recursion depth might be an issue or for iterative preference
- Maintains (node, parent) pairs in the stack

================================================================================
                            DIRECTED GRAPHS
================================================================================

For directed graphs, a cycle exists if we encounter a back edge (edge pointing
to a node that is currently in our recursion path/stack).

METHOD 1: TOPOLOGICAL SORT (Kahn's Algorithm)
-----------------------------------------------
Time: O(V + E)
Space: O(V)

Approach:
- Kahn's Algorithm: Process nodes with in-degree 0 (no dependencies)
- Remove processed nodes and decrement in-degrees of neighbors
- If all nodes are processed → no cycle (valid topological order exists)
- If some nodes remain with in-degree > 0 → cycle exists (circular dependencies)
- Key insight: In a DAG, there's always at least one node with in-degree 0
- If we can't find any such node but nodes remain → cycle!

METHOD 2: DFS WITH RECURSION STACK (Recursive)
-----------------------------------------------
Time: O(V + E)
Space: O(V) for recursion stack

Approach:
- Maintain TWO separate trackers:
  * visited: Tracks ALL nodes we've ever seen (persists across all DFS paths)
  * recursion_stack: Tracks ONLY nodes in the CURRENT DFS path (cleared on backtrack)
- Why both? In directed graphs, we can revisit a visited node from a different path
  without it being a cycle. But if a node is in recursion_stack, it means we're still
  processing it in the current path → encountering it again = back edge = cycle!
- When backtracking, remove node from recursion_stack (but keep in visited)
- Most common interview approach for directed graphs

METHOD 3: DFS WITH RECURSION STACK (Iterative)
-----------------------------------------------
Time: O(V + E)
Space: O(V) for explicit stack

Approach:
- Same logic as recursive but uses explicit stack with ENTER/EXIT phases
- Simulates recursion by tracking when we enter and exit nodes
- Useful when recursion depth is a concern

METHOD 4: 3-COLOR ALGORITHM (Alternative View)
-----------------------------------------------
Time: O(V + E)
Space: O(V)

Approach:
- Uses three states/colors instead of two boolean arrays:
  * WHITE (0): Unvisited node (like not in visited)
  * GRAY (1): Currently being processed (like in recursion_stack)
  * BLACK (2): Fully processed (like in visited but NOT in recursion_stack)
- If we encounter a GRAY node during DFS → cycle detected
- Conceptually IDENTICAL to recursion stack method, just different representation:
  * visited + recursion_stack = color array (WHITE/GRAY/BLACK)
  * More intuitive for some people: "if we see gray, we're in a cycle"

METHOD 5: TORTOISE AND HARE (Floyd's Cycle Detection)
-------------------------------------------------------
Time: O(V)
Space: O(1)

Approach:
- Only applicable to linked lists (graphs with exactly one outgoing edge per node)
- Use two pointers moving at different speeds
- If they meet, cycle exists
- Note: See linked list implementations for details

================================================================================
                            GENERAL NOTES
================================================================================

- The inefficient path-tracking method (Method 0) is included for educational
  purposes but should not be used in interviews

UNDIRECTED GRAPHS:
- Parent tracking is key (can't use recursion stack alone)
- A visited node that's NOT the parent = back edge = cycle
- Parent tracking distinguishes between parent-child edge (valid) and back edge (cycle)

DIRECTED GRAPHS:
- Recursion stack tracking is key (parent tracking won't work)
- Need TWO trackers: visited (all seen nodes) + recursion_stack (current path)
- Why both? In directed graphs, you can revisit a visited node from a different
  path without it being a cycle. Only if it's in the current recursion stack = cycle
- 3-color algorithm is identical to recursion stack, just uses colors instead

ALWAYS:
- Handle disconnected components by checking all unvisited nodes
- Consider edge cases: empty graph, single node, self-loops
'''

# ============================================================================
# METHOD 0: INEFFICIENT PATH TRACKING (Educational Purpose Only)
# ============================================================================
# This method tracks the entire path/ancestry to each node, which is memory
# intensive and inefficient. Included for educational understanding only.
# Time: O(V * E) worst case, Space: O(V * E) for storing paths

def cycleInGraph(edges):
    """
    Detects cycle by tracking full path to each node.
    
    Args:
        edges: Adjacency list representation of graph
        
    Returns:
        True if cycle exists, False otherwise
    """
    visited = set()
    unvisited = set(list(range(len(edges))))
    frontier = [(0, [0])]  # (current_node, path_to_reach_this_node)

    while unvisited:
        curr = None
        ancestor = []

        if frontier:
            curr, ancestor = frontier.pop()
        else:
            # Remove visited nodes and pick next unvisited component
            unvisited = unvisited - visited

            if unvisited:
                # Start new DFS from unvisited node
                curr = unvisited.pop()
                ancestor = [curr]
            else:
                continue

        visited.add(curr)

        for neighbour in edges[curr]:
            # If neighbour is in our path, we found a cycle
            if neighbour in ancestor:
                return True

            # Continue DFS if not visited
            if neighbour not in visited:
                frontier.append((neighbour, ancestor + [neighbour]))

    return False


# ============================================================================
# UNDIRECTED GRAPHS - METHOD 1: UNION-FIND (DISJOINT SET UNION)
# ============================================================================

class UnionFind:
    """
    Union-Find data structure for efficient connectivity queries.
    Used to detect cycles by checking if two nodes are already connected.
    """
    def __init__(self):
        self.parent = dict()

    def createSet(self, value):
        """Initialize a node as its own parent (separate set)."""
        self.parent[value] = None

    def find(self, value):
        """
        Find the root parent of a value (with path compression).
        
        Returns:
            Root parent if value exists, None otherwise
        """
        if value not in self.parent:
            return None

        curr = value
        # Traverse up to find root (parent is None)
        while self.parent[curr] is not None:
            curr = self.parent[curr]

        return curr

    def union(self, valueOne, valueTwo):
        """
        Union two sets. If they're already in the same set, returns False.
        
        Returns:
            True if union was successful (different sets)
            False if already in same set (indicates cycle in undirected graph)
        """
        parent1 = self.find(valueOne)
        parent2 = self.find(valueTwo)

        if parent1 != parent2:
            # Merge sets by making parent2's root point to parent1's root
            self.parent[parent2] = parent1
            return True
        # Already in same set - this edge creates a cycle!
        return False


def cycleInUndirectedGraph(edges):
    """
    Detect cycle in undirected graph using Union-Find.
    
    Key Insight: If an edge connects two nodes already in the same set,
    that edge creates a cycle.
    
    Args:
        edges: Adjacency list representation of undirected graph
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V * α(V)) where α is inverse Ackermann function
    Space: O(V)
    """
    # Initialize: each node is its own set
    disjointNodeSet = UnionFind()
    for i in range(len(edges)):
        disjointNodeSet.createSet(i)

    # Process each edge
    for i, edge in enumerate(edges):
        for j in edge:
            # If union returns False, nodes were already connected → cycle!
            if not disjointNodeSet.union(i, j):
                return True

    return False


# ============================================================================
# UNDIRECTED GRAPHS - METHOD 2: DFS WITH PARENT TRACKING (Recursive)
# ============================================================================

def has_cycle_undirected(graph, node, parent, visited):
    """
    Helper function for recursive DFS cycle detection in undirected graph.
    
    Key Insight: In undirected graph, if we visit a node that's already visited
    AND it's not our immediate parent, we found a back edge → cycle exists.
    
    Args:
        graph: Adjacency list representation
        node: Current node being processed
        parent: Parent node that led us here (to avoid false positives)
        visited: Boolean array tracking visited nodes
        
    Returns:
        True if cycle found in subtree, False otherwise
    """
    visited[node] = True

    for neighbor in graph[node]:
        if not visited[neighbor]:
            # Continue DFS - if cycle found in subtree, propagate up
            if has_cycle_undirected(graph, neighbor, node, visited):
                return True
        elif neighbor != parent:
            # Found visited node that's NOT parent → back edge → cycle!
            return True

    return False


def is_cyclic_undirected_recursive(graph, n):
    """
    Detect cycle in undirected graph using recursive DFS with parent tracking.
    
    Args:
        graph: Adjacency list representation of undirected graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V) for recursion stack
    """
    visited = [False] * n

    # Check all components (handle disconnected graph)
    for node in range(n):
        if not visited[node]:
            # Start DFS with no parent (-1 indicates root)
            if has_cycle_undirected(graph, node, -1, visited):
                return True
    return False


# ============================================================================
# UNDIRECTED GRAPHS - METHOD 3: DFS WITH PARENT TRACKING (Iterative)
# ============================================================================

def is_cyclic_undirected_iterative(graph, n):
    """
    Detect cycle in undirected graph using iterative DFS with parent tracking.
    
    Same logic as recursive version but uses explicit stack.
    Useful when recursion depth might be an issue.
    
    Args:
        graph: Adjacency list representation of undirected graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V) for explicit stack
    """
    visited = [False] * n

    for start in range(n):
        if not visited[start]:
            stack = [(start, -1)]
            visited[start] = True  # mark on DISCOVERY

            while stack:
                node, parent = stack.pop()

                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True  # mark on DISCOVERY
                        stack.append((neighbor, node))
                    elif neighbor != parent:
                        return True

    return False

# ============================================================================
# DIRECTED GRAPHS - METHOD 1: TOPOLOGICAL SORT (Kahn's Algorithm)
# ============================================================================

def is_cyclic_directed_topological(graph, n):
    """
    Detect cycle in directed graph using topological sort (Kahn's algorithm).
    
    Key Insight: If we can process all nodes (topological sort succeeds), no cycle.
    If some nodes remain unprocessed (still have dependencies), cycle exists.
    
    Algorithm:
    1. Count in-degrees (incoming edges) for each node
    2. Start with nodes having in-degree 0 (no dependencies)
    3. Process these nodes and decrement in-degrees of their neighbors
    4. If a neighbor's in-degree becomes 0, add it to processing queue
    5. If all nodes are processed → no cycle
    6. If some nodes remain → cycle exists (circular dependencies)
    
    Args:
        graph: Adjacency list representation of directed graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V)
    """
    from collections import deque
    
    # Step 1: Build in-degree array - count incoming edges for each node
    indegree = [0] * n
    for node in range(n):
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    
    # Step 2: Initialize queue with nodes having zero in-degree (no dependencies)
    queue = deque()
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)
    
    # Step 3: Process nodes with zero in-degree
    processed_count = 0
    
    while queue:
        node = queue.popleft()
        processed_count += 1
        
        # Step 4: Remove this node - decrement in-degree of all neighbors
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            # If neighbor now has zero in-degree, it's ready to process
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 5: Cycle detection
    # If we processed all nodes, no cycle exists (valid topological order)
    # If some nodes remain unprocessed, they're in a cycle (circular dependencies)
    return processed_count != n


# ============================================================================
# DEMONSTRATION: Why Parent Tracking Fails in Directed Graphs
# ============================================================================

def is_cyclic_directed_wrong_parent_tracking(graph, n):
    """
    WRONG IMPLEMENTATION - Demonstrates why parent tracking doesn't work for directed graphs.
    
    This function shows what happens if we try to use parent tracking (like undirected graphs)
    on a directed graph. It will give FALSE POSITIVES!
    
    Example where it fails:
    Graph: A(0) -> B(1) -> C(2), A(0) -> C(2)  (NO cycle, just two paths to C)
    - DFS path 1: A -> B -> C (C visited, parent is B)
    - DFS path 2: A -> C (C visited, parent is A, not B)
    - This function would say: "C is visited and A != B" → cycle detected (WRONG!)
    
    DO NOT USE THIS IN INTERVIEWS - it's incorrect!
    """
    visited = [False] * n
    
    def dfs(node, parent):
        visited[node] = True
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # This logic works for UNDIRECTED graphs but fails for DIRECTED!
                # In directed graphs, reaching a visited node from different path
                # doesn't necessarily mean cycle
                return True  # FALSE POSITIVE!
        
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False


# ============================================================================
# DIRECTED GRAPHS - METHOD 2: DFS WITH RECURSION STACK (Recursive)
# ============================================================================

def has_cycle_directed(graph, node, visited, on_stack):
    """
    Helper function for recursive DFS cycle detection in directed graph.
    
    Key Insight: In directed graph, if we encounter a node that's currently
    in our recursion stack (being processed), we found a back edge → cycle.
    
    WHY TWO TRACKERS? (Why not just use parent tracking like undirected graphs?)
    - visited: Tracks ALL nodes we've ever seen (persists across all DFS paths)
    - recursion_stack: Tracks ONLY nodes in CURRENT DFS path (cleared on backtrack)
    
    WHY PARENT TRACKING FAILS IN DIRECTED GRAPHS:
    Consider graph: A -> B -> C, A -> C (two paths to C, NO cycle)
    - Path 1: A -> B -> C (C is visited, parent is B)
    - Path 2: A -> C (C is visited, parent is A, not B)
    - With parent tracking: "C is visited and A != B (parent)" → FALSE POSITIVE cycle!
    - But this is NOT a cycle - just two different paths to the same node
    
    Another example: A -> B, A -> C, C -> B (NO cycle)
    - Path 1: A -> B (B is visited, parent is A)
    - Path 2: A -> C -> B (B is visited, parent is C, not A)
    - Parent tracking would incorrectly say: "B visited and C != A" → cycle (WRONG!)
    
    The key: In directed graphs, you can reach a visited node via different paths
    without it being a cycle. Only if that node is STILL in the recursion stack
    (meaning we're still processing the path that led to it) = back edge = cycle.
    
    Args:
        graph: Adjacency list representation
        node: Current node being processed
        visited: Boolean array for all visited nodes (persists)
        recursion_stack: Boolean array for nodes in current DFS path (cleared on backtrack)
        
    Returns:
        True if cycle found in subtree, False otherwise
    """
    # Mark as visited (permanent) and add to recursion stack (temporary)
    visited[node] = True
    on_stack[node] = True

    for neighbor in graph[node]:
        if not visited[neighbor]:
            # Continue DFS - if cycle found in subtree, propagate up
            if has_cycle_directed(graph, neighbor, visited, on_stack):
                return True
        elif on_stack[neighbor]:
            # Found node in recursion stack → back edge → cycle!
            return True

    # Backtrack: remove from recursion stack (but keep in visited)
    on_stack[node] = False
    return False


def is_cyclic_directed_recursive(graph, n):
    """
    Detect cycle in directed graph using recursive DFS with recursion stack.
    
    This is the most common interview approach for directed graph cycle detection.
    
    Args:
        graph: Adjacency list representation of directed graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V) for recursion stack
    """
    visited = [False] * n
    on_stack = [False] * n  # Tracks nodes in current DFS path

    # Check all components (handle disconnected graph)
    for node in range(n):
        if not visited[node]:
            if has_cycle_directed(graph, node, visited, on_stack):
                return True
    return False


# ============================================================================
# DIRECTED GRAPHS - METHOD 3: DFS WITH RECURSION STACK (Iterative)
# ============================================================================

def is_cyclic_directed_iterative(graph, n):
    """
    Detect cycle in directed graph using iterative DFS with recursion stack.
    
    Simulates recursion using explicit stack with ENTER/EXIT phases.
    Useful when recursion depth might be an issue.
    
    Args:
        graph: Adjacency list representation of directed graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V) for explicit stack
    """
    visited = [False] * n
    recursion_stack = [False] * n  # Tracks nodes in current DFS path
    explicit_stack = []  # Stack for iterative DFS: (node, "ENTER"/"EXIT")

    # Check all components (handle disconnected graph)
    for start in range(n):
        if not visited[start]:
            explicit_stack.append((start, "ENTER"))

            while explicit_stack:
                node, action = explicit_stack.pop()

                if action == "EXIT":
                    # Backtrack: remove from recursion stack
                    recursion_stack[node] = False
                    continue

                # Skip if already fully processed
                if visited[node]:
                    continue

                # Mark as visited and add to recursion stack
                visited[node] = True
                recursion_stack[node] = True
                explicit_stack.append((node, "EXIT"))  # Schedule exit phase

                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        # Continue DFS
                        explicit_stack.append((neighbor, "ENTER"))
                    elif recursion_stack[neighbor]:
                        # Found node in recursion stack → back edge → cycle!
                        return True

    return False


# ============================================================================
# DIRECTED GRAPHS - METHOD 4: 3-COLOR ALGORITHM (Not intuitive can ignore)
# ============================================================================

def has_cycle_directed_3color(graph, node, color):
    """
    Helper function for 3-color algorithm cycle detection in directed graph.
    
    Colors:
    - WHITE (0): Unvisited node
    - GRAY (1): Currently being processed (in current DFS path)
    - BLACK (2): Fully processed (visited but not in current path)
    
    Key Insight: Same as recursion stack method, but uses colors instead of
    two separate boolean arrays. If we encounter a GRAY node → cycle!
    
    Args:
        graph: Adjacency list representation
        node: Current node being processed
        color: Array tracking color state of each node
        
    Returns:
        True if cycle found in subtree, False otherwise
    """
    # Mark as GRAY (currently processing)
    color[node] = 1  # GRAY
    
    for neighbor in graph[node]:
        if color[neighbor] == 0:  # WHITE (unvisited)
            # Continue DFS - if cycle found in subtree, propagate up
            if has_cycle_directed_3color(graph, neighbor, color):
                return True
        elif color[neighbor] == 1:  # GRAY (in current path) → cycle!
            return True
        # If BLACK (2), ignore - already fully processed from another path
    
    # Backtrack: mark as BLACK (fully processed)
    color[node] = 2  # BLACK
    return False


def is_cyclic_directed_3color(graph, n):
    """
    Detect cycle in directed graph using 3-color algorithm.
    
    This is conceptually identical to the recursion stack method but uses
    a single color array instead of two boolean arrays (visited + recursion_stack).
    
    Args:
        graph: Adjacency list representation of directed graph
        n: Number of nodes
        
    Returns:
        True if cycle exists, False otherwise
        
    Time: O(V + E)
    Space: O(V)
    """
    # 0 = WHITE (unvisited), 1 = GRAY (in path), 2 = BLACK (processed)
    color = [0] * n
    
    # Check all components (handle disconnected graph)
    for node in range(n):
        if color[node] == 0:  # WHITE (unvisited)
            if has_cycle_directed_3color(graph, node, color):
                return True
    return False


# ============================================================================
# DIRECTED GRAPHS - METHOD 5: TORTOISE AND HARE (Floyd's Cycle Detection)
# ============================================================================

def has_cycle_linked_list(head):
    """
    Alternative implementation: start both pointers at head.
    
    This version starts both pointers at head, which requires checking
    slow != fast at the start of each iteration.
    """
    if not head:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
        
        if slow == fast:
            return True  # Cycle detected
    
    return False  # Fast reached end, no cycle

# ============================================================================
# HASHSET APPROACH (Visited Set)
# ============================================================================

def has_cycle_linked_list_hashset(head):
    """
    Detects cycle in a linked list using a Hashset (Visited Set).
    
    Approach:
    - Traverse the list and add each node to a set.
    - If we encounter a node that is already in the set, a cycle exists.
    
    NOTE ON GENERAL GRAPHS:
    - This simple 'visited set' approach works for Linked Lists because each node 
      has at most one outgoing edge.
    - For general graphs (Directed/Undirected), this approach gives FALSE POSITIVES.
      In a graph, we might visit a node multiple times from different paths 
      (e.g., A->B->C and A->C). This is valid and not a cycle.
      For graphs, we must distinguish between "visited in current path" vs 
      "visited in previous path".
    """
    visited = set()
    curr = head
    while curr:
        if curr in visited:
            return True
        visited.add(curr)
        curr = curr.next
    return False

# Example linked list node class for testing
class ListNode:
    """Simple linked list node for testing tortoise and hare algorithm."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# TESTING
# ============================================================================

if __name__ == '__main__':
    # Test case 1: Directed graph with cycle
    edges = [
        [],      # Node 0: no outgoing edges
        [0, 3],  # Node 1: edges to 0 and 3
        [0],     # Node 2: edge to 0
        [1, 2]   # Node 3: edges to 1 and 2 (creates cycle: 1→3→1)
    ]
    n = len(edges)
    print("Test 1 (directed with cycle):")
    print(f"  Path tracking: {cycleInGraph(edges)}")
    print(f"  Topological: {is_cyclic_directed_topological(edges, n)}")
    print(f"  Recursive DFS: {is_cyclic_directed_recursive(edges, n)}")
    print(f"  Iterative DFS: {is_cyclic_directed_iterative(edges, n)}")
    print(f"  3-Color: {is_cyclic_directed_3color(edges, n)}")
    
    # Test case 2: Directed graph without cycle
    edges_no_cycle = [
        [1],           # Node 0: edge to 1
        [2, 3, 4, 5, 6, 7],  # Node 1: edges to multiple nodes
        [],            # Node 2: no outgoing edges
        [2, 7],        # Node 3: edges to 2 and 7
        [5],           # Node 4: edge to 5
        [],            # Node 5: no outgoing edges
        [4],           # Node 6: edge to 4
        []             # Node 7: no outgoing edges
    ]
    n2 = len(edges_no_cycle)
    print("\nTest 2 (directed without cycle):")
    print(f"  Path tracking: {cycleInGraph(edges_no_cycle)}")
    print(f"  Topological: {is_cyclic_directed_topological(edges_no_cycle, n2)}")
    print(f"  Recursive DFS: {is_cyclic_directed_recursive(edges_no_cycle, n2)}")
    print(f"  Iterative DFS: {is_cyclic_directed_iterative(edges_no_cycle, n2)}")
    print(f"  3-Color: {is_cyclic_directed_3color(edges_no_cycle, n2)}")

    # Test case 2b: Undirected iterative DFS regression tests (no visited guard)
    undirected_cases = {
        "Triangle (3-cycle)": (
            [
                [1, 2],
                [0, 2],
                [0, 1],
            ],
            True,
        ),
        "Tree (line of 4 nodes)": (
            [
                [1, 2],
                [0, 3],
                [0],
                [1],
            ],
            False,
        ),
        "Square (4-cycle)": (
            [
                [1, 3],
                [0, 2],
                [1, 3],
                [0, 2],
            ],
            True,
        ),
        "Disconnected (one tree component, one cycle component)": (
            [
                [1],        # component 1 (tree)
                [0],
                [3, 4],     # component 2 (cycle 2-3-4-2)
                [2, 4],
                [2, 3],
            ],
            True,
        ),
        "Star graph (acyclic)": (
            [
                [1, 2, 3, 4],
                [0],
                [0],
                [0],
                [0],
            ],
            False,
        ),
    }
    print("\nTest 2b (Undirected iterative DFS without visited guard):")
    for name, (graph_case, expected) in undirected_cases.items():
        result = is_cyclic_undirected_iterative(graph_case, len(graph_case))
        print(f"  {name}: {result} (expected {expected})")
    
    # Test case 3: Demonstration - Why parent tracking fails in directed graphs
    print("\nTest 3 (Why Parent Tracking Fails in Directed Graphs):")
    # Graph: A(0) -> B(1) -> C(2), A(0) -> C(2)
    # This has NO cycle - just two paths to C
    edges_no_cycle_parent_test = [
        [1, 2],  # A -> B, A -> C
        [2],     # B -> C
        []       # C has no outgoing edges
    ]
    n3 = len(edges_no_cycle_parent_test)
    print(f"  Graph: A->B->C, A->C (NO cycle, just two paths to C)")
    print(f"  Correct method (recursion stack): {is_cyclic_directed_recursive(edges_no_cycle_parent_test, n3)}")
    print(f"  WRONG method (parent tracking): {is_cyclic_directed_wrong_parent_tracking(edges_no_cycle_parent_test, n3)}")
    print(f"  => Parent tracking gives FALSE POSITIVE!")
    
    # Test case 4: Tortoise and Hare (Linked List)
    print("\nTest 4 (Tortoise and Hare - Linked List):")
    # Create linked list with cycle: 1 -> 2 -> 3 -> 4 -> 2 (cycle back to 2)
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Cycle: points back to node2
    print(f"  Linked list with cycle: {has_cycle_linked_list(node1)}")
    
    # Create linked list without cycle: 1 -> 2 -> 3 -> 4 -> None
    node1_no_cycle = ListNode(1)
    node2_no_cycle = ListNode(2)
    node3_no_cycle = ListNode(3)
    node4_no_cycle = ListNode(4)
    node1_no_cycle.next = node2_no_cycle
    node2_no_cycle.next = node3_no_cycle
    node3_no_cycle.next = node4_no_cycle
    print(f"  Linked list without cycle: {has_cycle_linked_list(node1_no_cycle)}")