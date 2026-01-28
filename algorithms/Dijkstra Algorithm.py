import heapq
from heapq import *
from typing import List, Dict

# --------------------------------------------------------------------------
# APPROACH 1: Optimized Dijkstra with Distance Array (The "Classic" Way)
# --------------------------------------------------------------------------
def dijkstrasAlgorithm(start, edges):
    '''
    DIJKSTRA THEORY: RELAXATION (PUSH) VS. FINALIZATION (POP)
    ----------------------------------------------------------
    1. THE CONDITIONAL PUSH (Relaxation):
       We only push a node onto the heap if the NEW calculated path is 
       strictly better than the best distance we have recorded so far. 
       This keeps the heap size manageable and prevents redundant work.

    2. THE POP CHECK (Finalization):
       Even with Conditional Pushes, the heap can contain multiple entries 
       for the same node (e.g., if we found a better path while a previous 
       path was still sitting in the heap). 
       The FIRST time a node is popped, it is "Finalized." Any subsequent 
       pops for that same node are "stale" and must be ignored.

    3. WHY NOT MARK VISITED ON PUSH?
       In weighted graphs, the first path you find (discovery) isn't 
       necessarily the shortest. 
       Example:
       Path A: Start -> B (Weight 10)
       Path B: Start -> C -> B (Weights 2 + 3 = 5)
       If we marked B "visited" when we saw Path A, we'd never accept Path B.
    '''
    
    # Initialize distances: Distance to start is 0, all others are Infinity.
    distances = [float("inf") for i in range(len(edges))]
    distances[start] = 0
    
    # visited = Finalized set. unvisited = All nodes yet to be finalized.
    visited = set()
    unvisited = set(list(range(len(edges))))
    edgeQ = []

    # Initial seeding of the heap from the start node.
    for neighbour, weight in edges[start]:
        # Only update and push if this is the best path seen so far.
        if weight < distances[neighbour]:
            distances[neighbour] = weight
            # Priority Queue stores (cumulative_weight, source, destination).
            edgeQ.append((weight, start, neighbour))
    
    heapify(edgeQ)

    # Visited keeps track of notes which are finalized!
    # The start node is finalized by definition (distance 0).
    visited.add(start)
    
    while unvisited:
        if edgeQ:
            w, i, j = heappop(edgeQ)
            
            # FINALIZATION CHECK:
            # If j is in visited, we already found a shorter way to reach it.
            # This pop is a "zombie" or "stale" path.
            if j in visited:
                continue
                
            # Node j is now officially finalized.
            visited.add(j)
            
            # Explore neighbors of the finalized node j.
            for neighbour, weight in edges[j]:
                # THE DOUBLE GUARD: 
                # 1. Don't look at finalized nodes.
                # 2. Only look at paths that improve our current best estimate.
                if neighbour not in visited:
                    newDist = distances[j] + weight
                    if newDist < distances[neighbour]:
                        distances[neighbour] = newDist
                        heappush(edgeQ, (newDist, j, neighbour))
        else:
            # Handle disconnected components (nodes that were never reached).
            unvisited -= visited
            for leftOutNode in unvisited:
                distances[leftOutNode] = -1
            unvisited.clear()
            
    return distances


# --------------------------------------------------------------------------
# APPROACH 2: Node-Centric / Lazy Deletion (NeetCode Style)
# --------------------------------------------------------------------------
class Solution:
    '''
    THEORY: DICTIONARY-BASED LAZY FINALIZATION
    -----------------------------------------
    This version is more compact and uses the 'shortest' dictionary 
    to handle both the results and the "finalized" (visited) set.

    Differences from Approach 1:
    - It uses a "Lazy Deletion" strategy. It doesn't check 'newDist < currentBest'
      before pushing. It relies on the 'if n1 in shortest: continue' check 
      at pop-time to discard suboptimal paths.
    - Heap size can grow to O(E) because we push every discovery, but the 
      'if n2 not in shortest' check during the neighbor loop still acts 
      as a basic optimization to avoid re-exploring fully finalized nodes.
    '''
    def shortestPath(self, n: int, edges: List[List[int]], src: int) -> Dict[int, int]:
        # Construct Adjacency List
        adj = {i: [] for i in range(n)}
        for s, d, w in edges:
            adj[s].append([d, w])

        # Maps node -> its finalized shortest distance.
        shortest = {}
        
        # Priority Queue: [cumulative_weight, current_node]
        minHeap = [[0, src]]
        
        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            
            # POP-TIME FINALIZATION CHECK:
            # If n1 is already in shortest, we've already finalized it via a better path.
            if n1 in shortest:
                continue
            
            # This is the moment n1's distance is finalized.
            shortest[n1] = w1

            for n2, w2 in adj[n1]:
                # BASIC OPTIMIZATION:
                # Don't push a neighbor if that neighbor is already finalized.
                if n2 not in shortest:
                    heapq.heappush(minHeap, [w1 + w2, n2])

        # Fill in nodes that could not be reached from the source.
        for i in range(n):
            if i not in shortest:
                shortest[i] = -1

        return shortest

if __name__ == '__main__':
    start = 0
    # Graph: Adjacency list with weighted edges
    edges_list = [
        [[1, 7]],                   # Node 0
        [[2, 6], [3, 20], [4, 3]],  # Node 1
        [[3, 14]],                  # Node 2
        [[4, 2]],                   # Node 3
        [],                         # Node 4
        []                          # Node 5
    ]
    
    # Testing the Optimized Approach 1
    print("Optimized Dijkstra Result:", dijkstrasAlgorithm(start, edges_list))
    
    # Testing NeetCode Style Approach 2
    # Format conversion: [src, dst, weight]
    flat_edges = [
        [0, 1, 7], [1, 2, 6], [1, 3, 20], [1, 4, 3], [2, 3, 14], [3, 4, 2]
    ]
    sol = Solution()
    print("NeetCode Style Result:", sol.shortestPath(6, flat_edges, 0))
