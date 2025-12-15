'''
Tarjan's Algorithm for Finding Articulation Points in Undirected Graphs

Problem: Find all articulation points (cut vertices) in an undirected graph.
An articulation point is a vertex whose removal increases the number of connected components.

NOTE: The concept of articulation points is only well-defined for UNDIRECTED graphs!

For directed graphs:
- Can use SCC roots logic: Find SCC roots (U) with incoming edges from other SCCs (V)
- Articulation points = U ∪ V

================================================================================
KEY CONCEPTS
================================================================================

1. ARTICULATION POINT (Cut Vertex)
   - A vertex whose removal disconnects the graph
   - Example: In graph 0-1-2, vertex 1 is an articulation point
     (removing 1 splits graph into [0] and [2])
   - Example: In cycle 0-1-2-0, NO vertex is an articulation point
     (removing any vertex still leaves a connected path)

2. DISCOVERY TIME (disc[u])
   - The time when node u was first discovered during DFS
   - Used to determine the order of node discovery

3. LOW-LINK VALUE (low[u])
   - The smallest discovery time of any node reachable from u via:
     a) u itself
     b) Tree edges (DFS tree)
     c) Back edges (edges to ancestors)
   - Initially: low[u] = disc[u]
   - Updated when we find back edges to earlier nodes

4. ARTICULATION POINT CONDITIONS
   Condition 1 (Non-root): disc[u] <= low[v] for some child v
   - If u is not root and has a child v with no back edge to u's ancestors
   - Removing u disconnects v's subtree → u is articulation point
   
   Condition 2 (Root): u is root with more than 1 child
   - Root with multiple children connects different subtrees
   - Removing root disconnects these subtrees → root is articulation point

================================================================================
ALGORITHM OVERVIEW
================================================================================

The algorithm uses DFS with discovery times and low-link values.

Key Insight: A node in a cycle is NOT an articulation point (removing it
doesn't disconnect because there's an alternate path through the cycle).

Algorithm Steps:
1. Perform DFS traversal
2. For each node u:
   a. Set disc[u] = low[u] = current_time
   b. Explore neighbors v:
      - Skip parent (avoid going back up the tree)
      - If v not discovered: DFS(v) -> update low[u] comparing with low[v], then check articulation condition
      - If v already discovered: Update low[u] with back edge
   c. Check if u is root with multiple children
3. Return all articulation points found

================================================================================
WHY IT WORKS - DETAILED EXPLANATION
================================================================================

CONDITION 1: Non-root Articulation Point (disc[u] <= low[v])

This condition means:
- u has a child v
- v (and its entire subtree) cannot reach any ancestor of u
- The only path from v's subtree to the rest is through u
- Removing u disconnects v's subtree → u is articulation point

Why <= (non-strict inequality)?
- If disc[u] == low[v]: v's subtree can reach u, but NOT u's ancestors
- v entirely depends on u for connectivity to the rest of the graph
- Removing u still disconnects v's subtree → u is articulation point
- If low[v] < disc[u]: v can reach u's ancestors → u is NOT articulation point

Example 1: Articulation Point
   Graph: 0 - 1 - 2
   DFS tree: 0 → 1 → 2
   - disc[0]=0, disc[1]=1, disc[2]=2
   - low[2]=2 (no back edges)
   - When checking node 1:
     - disc[1]=1 <= low[2]=2 → Node 1 is articulation point!
   - Removing 1 disconnects node 2

Example 2: NOT an Articulation Point (Back Edge Exists)
   Graph: 0 - 1 - 2 - 0 (triangle)
   DFS tree: 0 → 1 → 2, with back edge 2 → 0
   - disc[0]=0, disc[1]=1, disc[2]=2
   - When exploring 2 → 0: low[2] = min(low[2], disc[0]) = 0
   - When checking node 1:
     - disc[1]=1, low[2]=0
     - disc[1] <= low[2]? NO (1 is NOT <= 0) → Node 1 is NOT articulation point
   - Removing 1 doesn't disconnect (2 can reach 0 via back edge)

Example 3: Edge Case (low[v] == disc[u])
   Graph: 0 - 1 - 2 - 1 (2 connects back to 1, but not to 0)
   DFS tree: 0 → 1 → 2, with back edge 2 → 1
   - disc[0]=0, disc[1]=1, disc[2]=2
   - When exploring 2 → 1: low[2] = min(low[2], disc[1]) = 1
   - When checking node 1:
     - disc[1]=1, low[2]=1
     - disc[1] <= low[2]? YES (1 <= 1) → Node 1 is articulation point!
   - Why? 2 can reach 1, but NOT 0 (1's parent)
   - Removing 1 disconnects 2 from 0

CONDITION 2: Root Articulation Point (children > 1)

If root has multiple children:
- Each child's subtree is connected only through the root
- Removing root disconnects these subtrees
- Root is articulation point

Example:
   Graph: 0 - 1, 0 - 2 (root 0 has two children)
   - Root 0 has 2 children (1 and 2)
   - Removing 0 splits graph into [1] and [2]
   - Node 0 is articulation point

================================================================================
TIME & SPACE COMPLEXITY
================================================================================

Time Complexity: O(V + E)
- Each vertex visited once: O(V)
- Each edge examined once: O(E)

Space Complexity: O(V)
- disc array: O(V)
- low array: O(V)
- parent array: O(V)
- Recursion stack: O(V) in worst case
'''


class Solution:
    def articulationPoints(self, V: int, adj: list) -> list:
        """
        Find all articulation points (cut vertices) in an undirected graph.
        
        Args:
            V: Number of vertices in the graph (vertices are labeled 0 to V-1)
            adj: Adjacency list representation of the undirected graph
                 adj[i] is a list of vertices adjacent to vertex i
        
        Returns:
            Sorted list of articulation points, or [None] if no articulation points exist.
        
        Example:
            V = 4
            adj = [[1], [0, 2, 3], [1], [1]]
            Graph: 0-1-2 and 1-3 (vertex 1 connects everything)
            Articulation points: [1] (removing 1 splits into [0], [2], [3])
        """
        # Global discovery time counter
        self.time = 0
        
        # disc[u] = discovery time of node u (None if not yet discovered)
        # Example: If DFS discovers nodes 0→1→2, then disc[0]=0, disc[1]=1, disc[2]=2
        self.disc = [None] * V
        
        # low[u] = smallest discovery time reachable from u
        # Updated when we find back edges to earlier nodes
        # Example: If u can reach node with disc=1, then low[u] ≤ 1
        self.low = [None] * V
        
        # parent[u] = parent of u in the DFS tree (None if u is root)
        # Used to:
        # 1. Skip the edge leading back to parent
        # 2. Check if u is root (parent[u] is None)
        # Example: If DFS tree is 0→1→2, then parent[1]=0, parent[2]=1, parent[0]=None
        self.parent = [None] * V
        
        # Set to store articulation points found
        # Using set to avoid duplicates
        self.ap = set()
        
        # Perform DFS for each connected component
        # This handles disconnected graphs
        for u in range(V):
            if self.disc[u] is None:  # Node not yet discovered
                self.dfs(u, adj)
        
        # Return sorted list of articulation points
        # Return [None] if no articulation points found (as per problem requirements)
        return sorted(list(self.ap)) if self.ap else [None]
    
    def dfs(self, u: int, adj: list) -> None:
        """
        Perform DFS to find articulation points.
        
        This function:
        1. Marks u as discovered and sets its discovery time
        2. Explores all neighbors of u (except parent)
        3. Updates low-link values based on tree edges and back edges
        4. Checks articulation point conditions for non-root nodes
        5. Checks if root has multiple children
        
        Args:
            u: Current node being explored
            adj: Adjacency list of the graph
        
        Example Walkthrough:
            Graph: 0 - 1 - 2
            dfs(0):
              - disc[0] = low[0] = 0, parent[0] = None, time = 1
              - Explore 0 → 1: dfs(1)
                - disc[1] = low[1] = 1, parent[1] = 0, time = 2
                - Explore 1 → 2: dfs(2)
                  - disc[2] = low[2] = 2, parent[2] = 1, time = 3
                  - No neighbors (except parent 1)
                  - Check: parent[2] exists, disc[2] <= low[?] → No children, skip
                - Backtrack: low[1] = min(low[1], low[2]) = min(1, 2) = 1
                - Check: parent[1] exists (0), disc[1]=1 <= low[2]=2 → AP!
              - Backtrack: low[0] = min(low[0], low[1]) = min(0, 1) = 0
              - Check root: parent[0] is None, children = 1 → Not AP (only 1 child)
        """
        # Initialize discovery time and low-link value
        # Both start at the same value (current time)
        self.disc[u] = self.low[u] = self.time
        self.time += 1  # Increment for next node
        
        # Count children of u in the DFS tree
        # Used to check if root has multiple children (root articulation point condition)
        children = 0
        
        # Explore all neighbors of u
        for v in adj[u]:
            # Case 1: Neighbor v has not been discovered yet (Tree Edge)
            # This is a forward edge in the DFS tree
            if self.disc[v] is None:
                # Set parent-child relationship
                # v's parent in DFS tree is u
                self.parent[v] = u
                children += 1  # Increment child count
                
                # Recursively explore v and its descendants
                # After this call returns, v's low-link value is correctly computed
                self.dfs(v, adj)
                
                # After v is completely explored, update u's low-link value
                # Rule: low[u] = min(low[u], low[v])
                # 
                # Why? Because anything reachable from v is also reachable from u
                # If v can reach an earlier node via back edge, u can too
                # 
                # Example:
                #   Graph: 0 - 1 - 2 - 0 (cycle)
                #   After exploring 2 → 0 (back edge):
                #     - low[2] = min(low[2], disc[0]) = 0
                #   When backtracking to 1:
                #     - low[1] = min(low[1], low[2]) = min(1, 0) = 0
                #   This propagates the earliest reachable node up the tree
                self.low[u] = min(self.low[u], self.low[v])
                
                # Check Articulation Point Condition (for non-root nodes ONLY)
                # Condition: disc[u] <= low[v]
                # 
                # This means:
                # - u has a child v
                # - v (and its entire subtree) cannot reach any ancestor of u
                # - The only path from v's subtree to the rest is through u
                # - Removing u disconnects v's subtree → u is articulation point
                # 
                # Why <= (non-strict) and not < (strict)?
                # - If low[v] == disc[u]: v can reach u, but NOT u's ancestors
                # - v entirely depends on u for connectivity to the rest
                # - Removing u still disconnects v's subtree → u is articulation point
                # - If low[v] < disc[u]: v can reach u's ancestors → u is NOT AP
                # 
                # Example 1: Articulation Point
                #   Graph: 0 - 1 - 2
                #   disc[1]=1, low[2]=2 (no back edges from 2)
                #   disc[1] <= low[2]? YES (1 <= 2) → Node 1 is AP!
                # 
                # Example 2: NOT an Articulation Point
                #   Graph: 0 - 1 - 2 - 0 (triangle)
                #   disc[1]=1, low[2]=0 (2 has back edge to 0)
                #   disc[1] <= low[2]? NO (1 is NOT <= 0) → Node 1 is NOT AP
                # 
                # Example 3: Edge Case (low[v] == disc[u])
                #   Graph: 0 - 1 - 2 - 1 (2 connects back to 1, but not to 0)
                #   disc[1]=1, low[2]=1 (2 can reach 1, but not 0)
                #   disc[1] <= low[2]? YES (1 <= 1) → Node 1 is AP!
                #   Why? 2 depends entirely on 1 for connectivity to 0
                
                # Why must this be non-root only?
                # - If we drop the `parent[u] is not None` guard, roots with a single
                #   child would become false positives.
                # - Example false positive (chain): 0 - 1 - 2, DFS root = 0
                #   * low[1]=1, disc[0]=0 → disc[0] <= low[1] is true
                #   * Removing 0 leaves edge 1-2; graph stays connected → 0 is NOT AP
                if self.parent[u] is not None and self.disc[u] <= self.low[v]:
                    # u is not root AND has child v with no back edge to u's ancestors
                    # u is an articulation point!
                    self.ap.add(u)
            
            # Case 2: Neighbor v has been discovered AND v is not the parent (Back Edge)
            # This means v is an ancestor of u in the DFS tree (we found a cycle!)
            # We update u's low-link value to v's discovery time
            elif v != self.parent[u]:
                # Rule: low[u] = min(low[u], disc[v])
                # 
                # Why disc[v] and not low[v]?
                # - v is an ancestor, discovered earlier than u
                # - We want the earliest discovery time in the cycle
                # - disc[v] is the earliest time (v was discovered before u)
                # 
                # Example:
                #   Graph: 0 - 1 - 2 - 0 (cycle)
                #   DFS: 0 → 1 → 2
                #   disc[0]=0, disc[1]=1, disc[2]=2
                #   When exploring 2 → 0 (back edge):
                #     - low[2] = min(low[2], disc[0]) = min(2, 0) = 0
                #   This propagates: low[1] = 0, low[0] = 0
                #   All nodes in cycle can reach node 0 (earliest)
                self.low[u] = min(self.low[u], self.disc[v])
        
        # Check Root Articulation Point Condition
        # After exploring all children, check if u is root with multiple children
        # 
        # Why is root with multiple children an articulation point?
        # - Each child's subtree is connected only through the root
        # - Removing root disconnects these subtrees
        # - Root is articulation point
        # 
        # Example true positive (needs this root-specific check):
        #   Graph: 0 - 1, 0 - 2 (root 0 has two children, no back edges)
        #   - Non-root rule is skipped for root, so without this check 0 is missed.
        #   - Removing 0 splits graph into [1] and [2] → 0 IS an AP.
        # 
        # Why not if children == 1?
        # - Root with 1 child: removing root doesn't disconnect (only one subtree)
        #   Example: chain 0 - 1 - 2 with root=0 → removing 0 leaves 1-2 connected
        # - Root with 0 children: single node, not an articulation point
        if self.parent[u] is None and children > 1:
            # u is root (no parent) AND has more than 1 child
            # u is an articulation point!
            self.ap.add(u)
