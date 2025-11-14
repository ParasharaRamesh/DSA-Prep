'''
Bellman-Ford Algorithm
======================

Overview:
---------
• Single-source shortest path algorithm
• Time complexity: O(V * E) - worse than Dijkstra's O(E log V)
• Can handle graphs with negative edge weights
• Can detect negative weight cycles
• Unlike Dijkstra's greedy approach, Bellman-Ford considers all edges in each pass

Key Differences from Dijkstra's:
---------------------------------
• Dijkstra's: Greedy algorithm that processes nodes once using a priority queue
• Bellman-Ford: Relaxes all edges V-1 times, allowing revisiting of nodes
• Bellman-Ford can find shorter paths through negative edges that Dijkstra's misses

Why V-1 Passes?
---------------
• In a graph with V vertices, the longest simple path has at most V-1 edges
• After V-1 passes, all shortest paths should be found (if no negative cycles exist)
• One additional pass is used to detect negative weight cycles

K-Hop Constraint Property:
--------------------------
• After n passes with stable updates: dist[x] = minimum distance from source to x 
  over all paths with ≤ n edges
• This property ONLY holds when using stable updates (copying distances between passes)
• Classic in-place updates do NOT guarantee this property
'''


def classic_bellman_ford(edges, num_vertices, source_vertex):
    '''
    Classic Bellman-Ford Algorithm with In-Place Updates
    
    Characteristics:
    • Uses in-place distance updates (unstable)
    • Does NOT guarantee k-hop constraint property
    • Simpler implementation, slightly more memory efficient
    
    Parameters:
    -----------
    edges: List of tuples (u, v, weight) representing directed edges
    num_vertices: Total number of vertices in the graph
    source_vertex: Starting vertex for shortest path computation
    
    Returns:
    --------
    List of shortest distances from source_vertex to all vertices
    Returns None if a negative weight cycle is detected
    '''
    # Initialize: All distances are infinite except source (distance = 0)
    distances = [float('inf')] * num_vertices
    distances[source_vertex] = 0
    
    # Relaxation Phase: V-1 passes to find shortest paths
    # Each pass considers all edges and attempts to improve distances
    for pass_num in range(num_vertices - 1):
        for source_node, target_node, edge_weight in edges:
            # Relax edge if:
            # 1. Source node has been reached (not infinite)
            # 2. Path through source_node is shorter than current distance to target_node
            if (distances[source_node] != float('inf') and 
                distances[source_node] + edge_weight < distances[target_node]):
                distances[target_node] = distances[source_node] + edge_weight
    
    # Negative Cycle Detection: One additional pass
    # If we can still improve distances, a negative cycle exists
    for source_node, target_node, edge_weight in edges:
        if (distances[source_node] != float('inf') and 
            distances[source_node] + edge_weight < distances[target_node]):
            print("Graph contains negative weight cycle")
            return None
    
    '''
    Note on Negative Cycle Detection:
    ----------------------------------
    To identify which nodes are affected by the negative cycle:
    • Collect all nodes 'v' that can be improved in the detection pass
    • Use Kosaraju's algorithm to find strongly connected components
    • Filter components that contain edges with negative cycle weights
    '''
    
    return distances


def bellman_ford_k_hops(edges, num_vertices, source_vertex, max_hops):
    '''
    Bellman-Ford Algorithm with K-Hop Constraint Property
    
    Characteristics:
    • Uses stable updates (copies distances between passes)
    • GUARANTEES k-hop constraint property
    • After k passes: dist[x] = minimum distance over all paths with ≤ k edges
    
    Why Stable Updates Matter:
    ---------------------------
    • In pass kstored in previous_di, we use distances from pass k-1 (stances)
    • This ensures we only consider paths with exactly k edges in the k-th pass
    • Without copying, we might use updated values from the same pass, breaking the property
    
    How It Works:
    -------------
    • Pass 0: Only source has distance 0, all others are infinite
    • Pass 1: Update nodes reachable in 1 edge from source
    • Pass 2: Update nodes reachable in 2 edges from source (using pass 1 distances)
    • Pass k: Update nodes reachable in k edges from source (using pass k-1 distances)
    
    The K-Hop Constraint Property Explained:
    ----------------------------------------
    After k passes, for any node x:
    • distances[x] = minimum distance from source to x over ALL paths with ≤ k edges
    
    Why this works:
    • In pass k, we read from previous_distances (pass k-1 results)
    • We update current_distances using: previous_distances[u] + weight
    • This means we're finding paths of exactly k edges
    • We take the minimum across all such k-edge paths
    • Combined with previous passes, we get the minimum over all paths with ≤ k edges
    
    Example:
    --------
    Graph: A -> B (weight 1), B -> C (weight 2), A -> C (weight 5)
    Source: A, k = 2
    
    Pass 0: dist[A]=0, dist[B]=∞, dist[C]=∞
    Pass 1: dist[A]=0, dist[B]=1, dist[C]=5  (1-edge paths)
    Pass 2: dist[A]=0, dist[B]=1, dist[C]=3  (2-edge path A->B->C found)
    
    After 2 passes: dist[C] = 3 (minimum over paths with ≤ 2 edges)
    
    Parameters:
    -----------
    edges: List of tuples (u, v, weight) representing directed edges
    num_vertices: Total number of vertices in the graph
    source_vertex: Starting vertex for shortest path computation
    max_hops: Maximum number of edges to consider in paths
    
    Returns:
    --------
    List of shortest distances from source_vertex to all vertices
    (considering only paths with ≤ max_hops edges)
    '''
    # Initialize: All distances are infinite except source (distance = 0)
    # This represents distances after 0 passes (0-hop paths)
    previous_distances = [float('inf')] * num_vertices
    previous_distances[source_vertex] = 0
    
    # Perform k passes, each pass finds shortest paths with exactly k edges
    for current_pass in range(max_hops):
        # Create a copy for stable updates
        # We'll update current_distances using values from previous_distances
        current_distances = previous_distances.copy()
        
        # Relax all edges using distances from the previous pass
        for source_node, target_node, edge_weight in edges:
            # Check if we can improve target_node's distance using this edge
            # We use previous_distances[source_node] to ensure we're considering
            # paths with exactly (current_pass + 1) edges
            if (previous_distances[source_node] != float('inf') and 
                previous_distances[source_node] + edge_weight < current_distances[target_node]):
                current_distances[target_node] = previous_distances[source_node] + edge_weight
        
        # Update previous_distances for the next pass
        # After this, previous_distances contains shortest distances over paths with ≤ (current_pass + 1) edges
        previous_distances = current_distances
    
    return previous_distances
