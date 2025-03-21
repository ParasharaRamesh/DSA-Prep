'''
* Articulation points are those vertices which when removed from the graph splits it into 2 or more connected components.
* NOTE: in case we are finding articulation points in directed graphs then we can find the articulation points using the same logic as the SCC roots.
    - there are some SCC roots (U) which have incoming edges from nodes belonging to another SCC (V).
    - U union V are the set of articulation points.
* However in case of undirected graphs, the idea of using discovery times and low link values can still help. if we make a few key observations.

Observations:
1. we can update the low and disc in the same way as we did for the SCC in directed graphs
2. a node in a cycle can never be an articulation point:
 - In this case since it is an undirected graph we don't need to maintain an explicit stack like the SCC case to track back edges ( i.e. to ones which are not its parent)
 - as long as node v is already discovered and v was not the parent of u, then u-v is a back edge.
 - in which case we update the low[u] with the min of itself and disc[v]. ( as v could have been discovered earlier in the dfs path => it could have a smaller discovery time than u)
3. u is not the root of the DFS tree and it has a child v such that no vertex in the subtree rooted with v has a back edge to one of the ancestors in DFS tree of u.:
    - if disc[u] <= low[v] => u is an articulation point.
    - means that u was discovered a lot earlier than v, and v's lowest link value is greater than disc of u , which means that it cannot have a back edge to u or its ' ancestors
    - why <=, as in why the equals?
        . because initially disc[u] = low[u] < disc[v] = low[v]
        . low[v] will become equal to low[u] ( which was already equal to disc[u] if they are connected.
        . The lowest node reachable from v is exactly u, meaning it entirely depends on u for connectivity!!
4. a node u, after having explored all of its children, might have more than 1 child , and it might also be the root without having any parent.
    - in which case u is also an articulation point as it can be removed to disconnect all of its children

Just keep adding all of the articulation points to a set and return that in the end.
'''


class Solution:
    def articulationPoints(self, V, adj):
        self.time = 0  # Global time counter
        self.disc = [None] * V  # Discovery times
        self.low = [None] * V  # Low-link values
        self.parent = [None] * V  # Parent array
        self.ap = set()  # Store articulation points

        # Run DFS for every component
        for u in range(V):
            if self.disc[u] == None:
                self.dfs(u, adj)

        return sorted(list(self.ap)) if self.ap else [None]  # Sort result

    def dfs(self, u, adj):
        self.disc[u] = self.low[u] = self.time
        self.time += 1
        children = 0  # Count children to check root rule

        for v in adj[u]:  # Explore neighbors
            if not self.disc[v]:  # Tree Edge
                # set the parent child reln
                self.parent[v] = u
                children += 1 # incrementing no of children of u

                # explore neighbour/child
                self.dfs(v, adj)

                # Update low-link value
                self.low[u] = min(self.low[u], self.low[v])

                # Articulation Point Condition (for non-root)
                # if there is a parent for u (non root) and its discovery time is earlier than the low of neighbour
                if self.parent[u] and self.disc[u] <= self.low[v]:
                    self.ap.add(u)
            elif v != self.parent[u]:  # Back Edge as it was already discovered
                self.low[u] = min(self.low[u], self.disc[v])

        # after u is completely explored, it could have been a root with more than 1 child. In which case it is also an articulation point.
        if not self.parent[u] and children > 1:
            self.ap.add(u)
