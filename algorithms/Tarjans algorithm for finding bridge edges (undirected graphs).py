'''
Prerequisite is the articulation points algorithm and its info.

only change here is that it is a strict inequality (disc[u] < low[v])
. if low[v] == disc[u] => v or its subtree has a back edge to u itself, therefore even if u-v is removed , v's descendants are connected to u and there are no splits
. therefore low[v] has to be greater than disc[u] that there is no back edge at all

Look at leetcode 1192 -> https://leetcode.com/problems/critical-connections-in-a-network/description/

'''


class Solution:
    def articulationPoints(self, V, adj):
        self.time = 0  # Global time counter
        self.disc = [None] * V  # Discovery times
        self.low = [None] * V  # Low-link values
        self.bridges = []

        # Run DFS for every component
        for u in range(V):
            if not self.disc[u]:
                self.dfs(u, -1, adj)

        return self.bridges

    def dfs(self, u, parent, adj):
        self.disc[u] = self.low[u] = self.time
        self.time += 1

        for v in adj[u]:  # Explore neighbors
            if v == parent:
                continue  # Skip the edge leading back to the parent

            if not self.disc[v]:  # Tree Edge
                self.dfs(v, u, adj)  # DFS on child
                self.low[u] = min(self.low[u], self.low[v])

                # Bridge condition (strict inequality)
                if self.disc[u] < self.low[v]:
                    self.bridges.append([u, v])

            else:  # Back edge case
                self.low[u] = min(self.low[u], self.disc[v])
