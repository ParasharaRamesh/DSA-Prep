'''
Tarjan's Algorithm for Finding Strongly Connected Components (SCCs) in Directed Graphs

Problem: Find all strongly connected components in a directed graph.
A strongly connected component is a maximal set of vertices where every vertex
can reach every other vertex in the set.

Video Reference: https://www.youtube.com/watch?v=wUgWX0nc4NY

================================================================================
KEY CONCEPTS
================================================================================

1. DISCOVERY TIME (disc[u])
   - The time when node u was first discovered during DFS
   - Each node gets a unique discovery time
   - Example: If we discover nodes in order A→B→C, then disc[A]=0, disc[B]=1, disc[C]=2

2. LOW-LINK VALUE (low[u])
   - The smallest discovery time of any node reachable from u (including u itself)
   - Initially: low[u] = disc[u] (node can reach itself)
   - Updated as we discover back edges and cycles
   - Example: If u can reach node with disc=2, then low[u] ≤ 2

3. STRONGLY CONNECTED COMPONENT (SCC)
   - All nodes in an SCC will eventually have the same low-link value
   - The root of an SCC is the node with disc[u] == low[u]
    . the "SCC root" is the node in a strongly connected component (SCC) with the lowest discovery time (i.e., the node that was visited first in DFS within that component).
   - Example: In graph A→B→C→A, all three nodes form one SCC with low[A]=low[B]=low[C]

================================================================================
ALGORITHM OVERVIEW
================================================================================

The algorithm uses DFS with two key data structures:
1. Discovery time array (disc): Tracks when each node was discovered
2. Low-link value array (low): Tracks the earliest reachable ancestor

Key Insight: Nodes in the same SCC will converge to the same low-link value.

Algorithm Steps:
1. Perform DFS traversal
2. For each node u:
   a. Set disc[u] = low[u] = current_time
   b. Push u onto stack and mark as on_stack
   c. Explore neighbors v:
      - If v not discovered: DFS(v), then low[u] = min(low[u], low[v])
      - If v on stack (back edge): low[u] = min(low[u], disc[v])
   d. If disc[u] == low[u]: u is SCC root, pop stack until u

================================================================================
WHY IT WORKS - DETAILED EXPLANATION
================================================================================

RULE 1: Tree Edge Update (low[u] = min(low[u], low[v]))
   When exploring u → v and v is not yet discovered:
   - After completely exploring v's subtree, update u's low-link value
   - THERE IS A CHANCE THAT EVENTUALLY low[u] = low[v]. But it could also be that v starts a new SCC all-together.
        a. If they belong to the same SCC, then definitely low[u] = low[v] eventually.
        b. If they DO NOT belong to the same SCC, then low[u] != low[v]. As v may start/belong to another SCC. In which case u's low value should continue to stay as is.
        c. Note that u was Discovered before v therefore:
            - it has a lower disc[u] < disc[v]
            - it initially starts out with a lower low link value also low[u] < low[v]
            - anything which is explored from v will always have a larger discovery time and low link value (atleast at the beginning before they all converge)
    - Combining all 3 cases after dfs(v) is completely done, we get the update rule:
        - low[u] = min(low[u], low[v])
    - Interesting thing is that inside an SCC, v might find out another path which leads back to u (i.e. a back edge/cycle).
    - So v's low link value would have already been updated to the correct lowest low link value for that SCC using the idea #2 given below.
   
   Examples:
   a. Graph: 0 → 1 → 2 → 3
   Suppose nodes 1,2,3 form an SCC (with cycles between them)
   - After exploring 1→2→3, all get low = 1 (lowest in their SCC)
   - When backtracking to 0: low[0] = min(low[0], low[1]) = min(0, 1) = 0
   - Since disc[0] = 0 = low[0], node 0 is root of its own SCC
   - Node 0 does NOT belong to the SCC containing 1,2,3
   b. Refer to example here => https://www.youtube.com/watch?v=wUgWX0nc4NY&t=666s
            . Here after 4,5,6 is explored all will have the same low link value as 4, and then when it goes back to 3. 3 will continue to keep its low link value as 3 => it is not a part of 4's SCC!

RULE 2: Back Edge Update (low[u] = min(low[u], disc[v]))
   When exploring u → v and v is already on the stack:
   - This means v is an ancestor in the current DFS path (cycle detected!)
   - Update u's low-link to v's discovery time
   - This propagates the earliest ancestor's discovery time through the cycle
   
   Example:
   Graph: 0 → 1 → 2 → 0 (cycle)
   - disc[0]=0, disc[1]=1, disc[2]=2
   - When exploring 2 → 0: 0 is on stack, so low[2] = min(low[2], disc[0]) = 0
   - When backtracking: low[1] = min(low[1], low[2]) = min(1, 0) = 0
   - When backtracking: low[0] = min(low[0], low[1]) = min(0, 0) = 0
   - All nodes converge to low = 0, forming one SCC

RULE 3: SCC Root Detection (disc[u] == low[u])
   When a node u finishes DFS and disc[u] == low[u]:
   - u is the root of its SCC (first node discovered in that SCC)
   - All nodes in u's SCC are on the stack above u
   - Pop stack until u to collect the entire SCC
   
   Example:
   Stack: [0, 1, 2, 3] (0 at bottom, 3 at top)
   After DFS completes:
   - disc[0] = 0, low[0] = 0 → 0 is root
   - Pop: 3, 2, 1, 0 → SCC = [0, 1, 2, 3]

================================================================================
TIME & SPACE COMPLEXITY
================================================================================

Time Complexity: O(V + E)
- Each vertex visited once: O(V)
- Each edge examined once: O(E)

Space Complexity: O(V)
- disc array: O(V)
- low array: O(V)
- stack: O(V) in worst case
- on_stack array: O(V)
'''


class Solution:
    def tarjans(self, V: int, adj: list) -> list:
        """
        Find all strongly connected components in a directed graph using Tarjan's algorithm.
        
        Args:
            V: Number of vertices in the graph (vertices are labeled 0 to V-1)
            adj: Adjacency list representation of the directed graph
                 adj[i] is a list of vertices that vertex i has edges to
        
        Returns:
            List of lists, where each inner list contains vertices in one SCC.
            SCCs are sorted lexicographically by their smallest vertex.
        
        Example:
            V = 5
            adj = [[1], [2], [0, 3], [4], []]
            Graph: 0→1→2→0 (SCC1: [0,1,2]), 3→4 (SCC2: [3,4])
            Returns: [[0, 1, 2], [3, 4]]
        """
        # Global discovery time counter (increments for each new node discovered)
        self.time = 0
        
        # disc[u] = discovery time of node u (None if not yet discovered)
        # Example: If we discover nodes in order 0→1→2, then disc[0]=0, disc[1]=1, disc[2]=2
        self.disc = [None] * V
        
        # low[u] = smallest discovery time reachable from u (including u itself)
        # Initially equals disc[u], but decreases as we find back edges to earlier nodes
        # Example: If u can reach node with disc=2, then low[u] ≤ 2
        self.low = [None] * V
        
        # Stack to track nodes in the current DFS path
        # Nodes are pushed when discovered and popped when their SCC is found
        # Example: If DFS path is 0→1→2, stack = [0, 1, 2]
        self.stack = []
        
        # on_stack[u] = True if node u is currently on the stack
        # Used to detect back edges (edges to nodes already in current DFS path)
        # Example: If stack = [0, 1, 2], then on_stack[0]=on_stack[1]=on_stack[2]=True
        self.on_stack = [False] * V
        
        # List to store all strongly connected components found
        # Each SCC is a list of vertices
        self.sccs = []
        
        # Perform DFS starting from each unvisited node
        # This handles disconnected components in the graph
        # Example: If graph has two disconnected components, we need to start DFS twice
        for i in range(V):
            if self.disc[i] is None:  # Node not yet discovered
                self.dfs(i, adj)
        
        # Sort each SCC internally (for consistent output)
        # Example: SCC [2, 0, 1] becomes [0, 1, 2]
        self.sccs = [sorted(scc) for scc in self.sccs]
        
        # Sort SCCs by their smallest vertex (lexicographic order)
        # Example: [[2, 3], [0, 1]] becomes [[0, 1], [2, 3]]
        self.sccs.sort(key=lambda scc: scc[0])
        
        return self.sccs
    
    def dfs(self, u: int, adj: list) -> None:
        """
        Perform DFS starting from node u to find SCCs.
        
        This function:
        1. Marks u as discovered and sets its discovery time
        2. Pushes u onto the stack
        3. Explores all neighbors of u
        4. Updates low-link values based on tree edges and back edges
        5. If u is an SCC root, pops the stack to collect the SCC
        
        Args:
            u: Current node being explored
            adj: Adjacency list of the graph
        
        Example Walkthrough:
            Graph: 0 → 1 → 2 → 0 (cycle)
            dfs(0):
              - disc[0] = low[0] = 0, push 0, time = 1
              - Explore 0 → 1: dfs(1)
                - disc[1] = low[1] = 1, push 1, time = 2
                - Explore 1 → 2: dfs(2)
                  - disc[2] = low[2] = 2, push 2, time = 3
                  - Explore 2 → 0: 0 is on stack (back edge!)
                    - low[2] = min(low[2], disc[0]) = min(2, 0) = 0
                  - disc[2] != low[2] (2 != 0), so 2 is not root
                - Backtrack: low[1] = min(low[1], low[2]) = min(1, 0) = 0
                - disc[1] != low[1] (1 != 0), so 1 is not root
              - Backtrack: low[0] = min(low[0], low[1]) = min(0, 0) = 0
              - disc[0] == low[0] (0 == 0), so 0 is root!
              - Pop stack: [2, 1, 0] → SCC = [0, 1, 2]
        """
        # Initialize discovery time and low-link value
        # Both start at the same value (current time)
        # Example: First node discovered gets disc=0, low=0
        #          Second node gets disc=1, low=1
        self.disc[u] = self.low[u] = self.time
        self.time += 1  # Increment for next node
        
        # Push u onto stack and mark as on stack
        # This allows us to detect back edges later
        # Example: If DFS path is 0→1→2, stack = [0, 1, 2]
        self.stack.append(u)
        self.on_stack[u] = True
        
        # Explore all neighbors of u
        for v in adj[u]:
            # Case 1: Neighbor v has not been discovered yet (Tree Edge)
            # This is a forward edge in the DFS tree
            # We need to recursively explore v first, then update u's low-link value
            if self.disc[v] is None:
                # Recursively explore v and its descendants
                # After this call returns, v's low-link value is correctly computed
                self.dfs(v, adj)
                
                # After v is completely explored, update u's low-link value
                # Rule: low[u] = min(low[u], low[v])
                # 
                # Why? Because anything reachable from v is also reachable from u
                # If v belongs to the same SCC as u, their low values will converge
                # 
                # Example:
                #   Graph: u → v → w → v (cycle)
                #   After exploring v→w→v:
                #     - low[v] = disc[v] (v is root of its SCC)
                #     - low[w] = disc[v] (w can reach v)
                #   When backtracking to u:
                #     - low[u] = min(low[u], low[v]) = min(disc[u], disc[v])
                #   If u and v are in same SCC: low[u] = disc[v] (converges)
                #   If u and v are in different SCCs: low[u] stays as disc[u]
                self.low[u] = min(self.low[u], self.low[v])
            
            # Case 2: Neighbor v has been discovered AND is on the stack (Back Edge)
            # This means v is an ancestor in the current DFS path - we found a cycle!
            # We update u's low-link value to v's discovery time
            elif self.on_stack[v]:
                # Rule: low[u] = min(low[u], disc[v])
                # 
                # Why disc[v] and not low[v]?
                # - v is already on the stack, meaning it's in the current DFS path
                # - We want the earliest discovery time in the cycle
                # - disc[v] is the earliest time in this cycle
                # 
                # Example:
                #   Graph: 0 → 1 → 2 → 0 (cycle)
                #   disc[0]=0, disc[1]=1, disc[2]=2
                #   When exploring 2 → 0:
                #     - 0 is on stack (back edge detected!)
                #     - low[2] = min(low[2], disc[0]) = min(2, 0) = 0
                #   This propagates: low[1] = 0, low[0] = 0
                #   All nodes in cycle get same low value → same SCC
                self.low[u] = min(self.low[u], self.disc[v])
            
            # Case 3: Neighbor v has been discovered but NOT on stack
            # This means v belongs to a different SCC that was already processed
            # We don't update u's low-link value (v is in a different component)
            # Example: If we already found SCC [v, w] and popped them from stack,
            #          then u → v doesn't create a cycle with u
        
        # After exploring all neighbors, check if u is the root of an SCC
        # Condition: disc[u] == low[u]
        # 
        # Why this works:
        # - If u is the root, it was the first node discovered in its SCC
        # - All nodes in u's SCC are descendants of u in the DFS tree
        # - They all have low-link value equal to disc[u] (the root's discovery time)
        # - Since u was discovered first, disc[u] is the smallest in its SCC
        # - Therefore, disc[u] == low[u] (u can't reach any earlier node)
        # 
        # Example:
        #   SCC with nodes [0, 1, 2] where 0 is root
        #   disc[0]=0, low[0]=0, low[1]=0, low[2]=0
        #   When 0 finishes DFS: disc[0] == low[0] → 0 is root!
        #   Stack: [0, 1, 2] (0 at bottom)
        #   Pop until 0: SCC = [2, 1, 0] (reversed order)
        if self.disc[u] == self.low[u]:
            # u is the root of its SCC
            # Collect all nodes in this SCC by popping from stack
            scc = []
            
            # Keep popping until we reach u
            # All nodes between top of stack and u belong to the same SCC
            # They all have the same low-link value (equal to disc[u])
            while True:
                node = self.stack.pop()
                self.on_stack[node] = False  # Mark as no longer on stack
                scc.append(node)
                
                # Stop when we reach the root u
                # u was pushed first, so it's at the bottom of the SCC group
                # Example: Stack = [0, 1, 2, 3] where 0 is root
                #          Pop: 3, 2, 1, 0 → SCC = [3, 2, 1, 0]
                if node == u:
                    break
            
            # Add the collected SCC to our results
            self.sccs.append(scc)
