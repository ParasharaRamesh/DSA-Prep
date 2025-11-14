"""
Topological Sort Algorithm

The topological sort algorithm is used to find a linear ordering of nodes in a directed acyclic graph (DAG)
such that for every directed edge (u, v), node u comes before node v in the ordering.

General Algorithm Approach:
1. Find all nodes with zero in-degree (no incoming edges)
2. Add one of these zero in-degree nodes to the result
3. Remove that node from the graph and decrement the in-degree of all its neighbors
4. Repeat steps 1-3 until all nodes are processed

If at any point there are no zero in-degree nodes remaining but there are still unprocessed nodes,
this indicates a cycle exists in the graph, and topological sort is not possible.

The algorithm uses Kahn's algorithm approach:
- Maintain an in-degree count for each node
- Use a queue/stack to process zero in-degree nodes
- As we process nodes, we decrement in-degrees of neighbors
- When a neighbor's in-degree reaches zero, it becomes eligible for processing
"""

from typing import List


def topological_order(n: int, edges: List[List[int]]) -> List[int]:
    """
    Perform topological sort on a directed graph.
    
    Args:
        n: Number of nodes in the graph (nodes are labeled 0 to n-1)
        edges: List of edges where each edge is [u, v] meaning u -> v (u must come before v)
    
    Returns:
        List of nodes in topological order, or empty list if cycle is detected
    """
    # Step 1: Build adjacency list and initialize in-degree array
    # adj[i] contains all nodes that node i points to (children of node i)
    adj = [[] for _ in range(n)]
    
    # indegree[i] counts how many nodes point to node i (number of dependencies)
    indegree = [0] * n
    
    # Build the graph and count in-degrees
    for u, v in edges:
        # Edge u -> v means u must come before v
        adj[u].append(v)      # Add v as a neighbor of u
        indegree[v] += 1       # v has one more incoming edge (dependency on u)
    
    # Step 2: Initialize result list to store topological order
    output = []
    
    # Step 3: Helper function to process a node and its descendants
    def process_node(node: int):
        """
        Process a node with zero in-degree:
        1. Add it to the output (it has no remaining dependencies)
        2. Decrement its in-degree (mark as processed)
        3. For each neighbor, decrement their in-degree
        4. If a neighbor's in-degree becomes zero, recursively process it
        """
        # Add node to topological order (all its dependencies are satisfied)
        output.append(node)
        
        # Mark this node as processed by decrementing its in-degree to -1
        # This is a hack to ensure this node never gets processed again
        # (since we only process nodes when indegree == 0, and -1 will never satisfy that)
        indegree[node] -= 1
        
        # Process all neighbors (nodes that this node points to)
        for neighbor in adj[node]:
            # Decrement neighbor's in-degree (one of its dependencies is satisfied)
            indegree[neighbor] -= 1
            
            # If neighbor now has zero in-degree, it's ready to be processed
            if indegree[neighbor] == 0:
                process_node(neighbor)
    
    # Step 4: Start processing from all nodes with zero in-degree
    # These are nodes with no dependencies and can be processed first
    for i in range(n):
        if indegree[i] == 0:
            process_node(i)
    
    # Step 5: Cycle detection
    # If we processed all n nodes, we have a valid topological order
    # Otherwise, there's a cycle (some nodes still have dependencies)
    return output if len(output) == n else []


if __name__ == '__main__':
    # Example 1: Valid DAG
    # Graph: 5 -> 2 -> 3 -> 1
    #        5 -> 0
    #        4 -> 0
    #        4 -> 1
    n = 6
    edges = [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]]
    result = topological_order(n, edges)
    print(f"Topological order: {result}")
    # Expected: A valid ordering where 4 and 5 come before their children,
    #           and 2 comes before 3, 3 comes before 1, etc.
    # Example: [4, 5, 0, 2, 3, 1] or [5, 4, 2, 0, 3, 1]
    
    # Example 2: Graph with cycle
    # Cycle: 0 -> 1 -> 2 -> 0
    edges_with_cycle = [[0, 1], [1, 2], [2, 0]]
    result = topological_order(3, edges_with_cycle)
    print(f"Graph with cycle: {result}")
    # Expected: [] (empty list because cycle is detected)
