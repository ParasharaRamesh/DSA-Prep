'''
Tarjan's Algorithm for Finding Bridge Edges in Undirected Graphs

Problem: Find all bridge edges (critical connections) in an undirected graph.
A bridge edge is an edge whose removal increases the number of connected components.

LeetCode 1192: Critical Connections in a Network
https://leetcode.com/problems/critical-connections-in-a-network/description/

NOTE: The concept of bridges is only well-defined for UNDIRECTED graphs!

================================================================================
KEY CONCEPTS
================================================================================

1. BRIDGE EDGE
   - An edge (u, v) is a bridge if removing it disconnects the graph
   - Also called "critical connection" or "cut edge"
   - Example: In graph 0-1-2, edge (1,2) is a bridge (removing it splits into [0,1] and [2])
   - Example: In cycle 0-1-2-0, NO edge is a bridge (removing any edge still leaves a path)

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

4. BRIDGE CONDITION
   - Edge (u, v) is a bridge if: disc[u] < low[v]
   - This means v (and its subtree) cannot reach u or any ancestor of u
   - Removing (u, v) would disconnect v's subtree from the rest

================================================================================
ALGORITHM OVERVIEW
================================================================================

The algorithm is similar to finding articulation points, but with a stricter condition.

Key Differences from Articulation Points:
- For bridges: disc[u] < low[v] (STRICT inequality)
- For articulation points: disc[u] <= low[v] (non-strict inequality)

Why the difference?
- If low[v] == disc[u]: v's subtree has a back edge directly to u
  → Removing (u, v) doesn't disconnect (v can still reach u via back edge)
  → Edge is NOT a bridge
- If low[v] > disc[u]: v's subtree has NO back edge to u or u's ancestors
  → Removing (u, v) disconnects v's subtree
  → Edge IS a bridge

Algorithm Steps:
1. Perform DFS traversal
2. For each node u:
   a. Set disc[u] = low[u] = current_time
   b. Explore neighbors v:
      - Skip parent (avoid going back up the tree)
      - If v not discovered: DFS(v), then check bridge condition
      - If v already discovered: Update low[u] with back edge
3. Check bridge condition: if disc[u] < low[v], edge (u, v) is a bridge

================================================================================
WHY IT WORKS - DETAILED EXPLANATION
================================================================================

BRIDGE CONDITION: disc[u] < low[v]

This condition means:
- u was discovered before v (disc[u] < disc[v] is always true for tree edges)
- v (and its entire subtree) cannot reach u or any ancestor of u
- The only path from v's subtree to the rest of the graph is through edge (u, v)
- Therefore, removing (u, v) disconnects v's subtree → (u, v) is a bridge

Example 1: Bridge Edge
   Graph: 0 - 1 - 2
   DFS tree: 0 → 1 → 2
   - disc[0]=0, disc[1]=1, disc[2]=2
   - low[2]=2 (no back edges)
   - When checking edge (1, 2):
     - disc[1]=1 < low[2]=2 → BRIDGE!
   - Removing (1, 2) disconnects node 2

Example 2: NOT a Bridge (Back Edge Exists)
   Graph: 0 - 1 - 2 - 0 (triangle)
   DFS tree: 0 → 1 → 2, with back edge 2 → 0
   - disc[0]=0, disc[1]=1, disc[2]=2
   - When exploring 2 → 0: low[2] = min(low[2], disc[0]) = 0
   - When checking edge (1, 2):
     - disc[1]=1, low[2]=0
     - disc[1] < low[2]? NO (1 is NOT < 0) → NOT a bridge
   - Removing (1, 2) doesn't disconnect (2 can reach 0 via back edge)

Example 3: NOT a Bridge (Back Edge to Ancestor)
   Graph: 0 - 1 - 2 - 1 (2 connects back to 1)
   DFS tree: 0 → 1 → 2, with back edge 2 → 1
   - disc[0]=0, disc[1]=1, disc[2]=2
   - When exploring 2 → 1: low[2] = min(low[2], disc[1]) = 1
   - When checking edge (1, 2):
     - disc[1]=1, low[2]=1
     - disc[1] < low[2]? NO (1 is NOT < 1) → NOT a bridge
   - Removing (1, 2) doesn't disconnect (2 can reach 1 directly)

================================================================================
TIME & SPACE COMPLEXITY
================================================================================

Time Complexity: O(V + E)
- Each vertex visited once: O(V)
- Each edge examined once: O(E)

Space Complexity: O(V)
- disc array: O(V)
- low array: O(V)
- Recursion stack: O(V) in worst case
'''


class Solution:
    def criticalConnections(self, n: int, connections: list) -> list:
        """
        Find all bridge edges (critical connections) in an undirected graph.
        
        Args:
            n: Number of vertices in the graph (vertices are labeled 0 to n-1)
            connections: List of edges, where each edge is [u, v] representing
                         an undirected edge between u and v
        
        Returns:
            List of bridge edges. Each edge is represented as [u, v] where u < v.
        
        Example:
            n = 4
            connections = [[0,1], [1,2], [2,0], [1,3]]
            Graph: 0-1-2-0 (triangle) and 1-3
            Bridges: [[1, 3]] (only edge connecting node 3)
        """
        # Build adjacency list from edge list
        # For undirected graph, add edge in both directions
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)
        
        # Global discovery time counter
        self.time = 0
        
        # disc[u] = discovery time of node u (None if not yet discovered)
        # Example: If DFS discovers nodes 0→1→2, then disc[0]=0, disc[1]=1, disc[2]=2
        self.disc = [None] * n
        
        # low[u] = smallest discovery time reachable from u
        # Updated when we find back edges to earlier nodes
        # Example: If u can reach node with disc=1, then low[u] ≤ 1
        self.low = [None] * n
        
        # List to store bridge edges found
        # Each bridge is stored as [u, v] where u < v
        self.bridges = []
        
        # Perform DFS for each connected component
        # This handles disconnected graphs
        for u in range(n):
            if self.disc[u] is None:  # Node not yet discovered
                # Start DFS with parent = -1 (no parent for root)
                self.dfs(u, -1, adj)
        
        return self.bridges
    
    def dfs(self, u: int, parent: int, adj: list) -> None:
        """
        Perform DFS to find bridge edges.
        
        This function:
        1. Marks u as discovered and sets its discovery time
        2. Explores all neighbors of u (except parent)
        3. Updates low-link values based on tree edges and back edges
        4. Checks bridge condition for tree edges
        
        Args:
            u: Current node being explored
            parent: Parent of u in the DFS tree (-1 if u is root)
            adj: Adjacency list of the graph
        
        Example Walkthrough:
            Graph: 0 - 1 - 2
            dfs(0, -1):
              - disc[0] = low[0] = 0, time = 1
              - Explore 0 → 1: dfs(1, 0)
                - disc[1] = low[1] = 1, time = 2
                - Explore 1 → 2: dfs(2, 1)
                  - disc[2] = low[2] = 2, time = 3
                  - No neighbors (except parent 1)
                  - Check edge (1, 2): disc[1]=1 < low[2]=2 → BRIDGE!
                - Backtrack: low[1] = min(low[1], low[2]) = min(1, 2) = 1
                - Check edge (0, 1): disc[0]=0 < low[1]=1 → BRIDGE!
              - Backtrack: low[0] = min(low[0], low[1]) = min(0, 1) = 0
        """
        # Initialize discovery time and low-link value
        # Both start at the same value (current time)
        self.disc[u] = self.low[u] = self.time
        self.time += 1  # Increment for next node
        
        # Explore all neighbors of u
        for v in adj[u]:
            # Skip the edge leading back to parent
            # In undirected graphs, we don't want to go back up the tree
            # Example: If DFS path is 0→1→2, when at node 1, we skip edge 1→0
            if v == parent:
                continue
            
            # Case 1: Neighbor v has not been discovered yet (Tree Edge)
            # This is a forward edge in the DFS tree
            if self.disc[v] is None:
                # Recursively explore v and its descendants
                # After this call returns, v's low-link value is correctly computed
                self.dfs(v, u, adj)
                
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
                
                # Check if edge (u, v) is a bridge
                # Condition: disc[u] < low[v]
                # 
                # This means:
                # - u was discovered before v (always true for tree edges)
                # - v (and its entire subtree) cannot reach u or any ancestor of u
                # - The only path from v's subtree to the rest is through (u, v)
                # - Removing (u, v) would disconnect v's subtree → BRIDGE!
                # 
                # Why strict inequality (<) and not (<=)?
                # - If low[v] == disc[u], v has a back edge directly to u
                # - Removing (u, v) doesn't disconnect (v can still reach u)
                # - Therefore, edge is NOT a bridge
                # 
                # Example 1: Bridge
                #   Graph: 0 - 1 - 2
                #   disc[1]=1, low[2]=2 (no back edges from 2)
                #   disc[1] < low[2]? YES (1 < 2) → Edge (1, 2) is a bridge
                # 
                # Example 2: NOT a bridge (back edge exists)
                #   Graph: 0 - 1 - 2 - 0 (triangle)
                #   disc[1]=1, low[2]=0 (2 has back edge to 0)
                #   disc[1] < low[2]? NO (1 is NOT < 0) → Edge (1, 2) is NOT a bridge
                if self.disc[u] < self.low[v]:
                    # Edge (u, v) is a bridge!
                    # Store as [min(u,v), max(u,v)] for consistent output
                    self.bridges.append([min(u, v), max(u, v)])
            
            # Case 2: Neighbor v has been discovered (Back Edge)
            # This means v is an ancestor of u in the DFS tree
            # We found a cycle! Update u's low-link value
            else:
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
