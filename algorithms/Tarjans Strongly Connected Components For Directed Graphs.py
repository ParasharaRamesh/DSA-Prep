'''
Video explainer: https://www.youtube.com/watch?v=wUgWX0nc4NY
Some defintions:

* low link value of a node is the smallest node id reachable from that node when doing a DFS including itself. (i.e. that node is the starting point of the dfs)
    - However note that , it is initialized to disc which means it is rather a unit of time and not of id.
    - It represents the smallest discovery time of any reachable ancestor!
* in some sense all the nodes which have the same low link value belong to the same scc, but this is not entirely accurate as it depends on the traversal order:
    - look at the counter example here -> https://www.youtube.com/watch?v=wUgWX0nc4NY&t=253s
* so we need to also consider the discovery time of each of the nodes as well and take that into account.

Observations/Ideas:

* Let us use disc as an array of discovery times and low as an array of each node's lowest link value.
* once a node is discovered and its low link value is correctly updated & it is found out as an SCC we need to remove it from the stack
* at any point in time we only need to explore nodes which are YET to be "DISCOVERED" (i.e. not yet visited/processed)

0. Let's say when ever we visit a node u, we assign the discovery time and the low link value to be the same
    low[u] = disc[v] = time of discovery (t)
1. When exploring the graph, lets say from u -> v. We need to note that eventually after v is entirely explored, it COULD be a part of the same SCC as u.
    . THERE IS A CHANCE THAT EVENTUALLY low[u] = low[v]. But it could also be that v starts a new SCC all-together.
        a. If they belong to the same SCC, then definitely low[u] = low[v] eventually.
        b. If they DO NOT belong to the same SCC, then low[u] != low[v]. As v may start/belong to another SCC. In which case u's low value should continue to stay as is.
        c. Note that u was Discovered before v therefore:
            - it has a lower disc[u] < disc[v]
            - it initially starts out with a lower low link value also low[u] < low[v]
            - anything which is explored from v will always have a larger discovery time and low link value (atleast at the beginning before they all converge)
    . Combining all 3 cases after dfs(v) is completely done, we get the update rule:
        - low[u] = min(low[u], low[v])
        - refer to example here => https://www.youtube.com/watch?v=wUgWX0nc4NY&t=666s
            . Here after 4,5,6 is explored all will have the same low link value as 4, and then when it goes back to 3. 3 will continue to keep its low link value as 3 => it is not a part of 4's SCC!
    . Interesting thing is that inside an SCC, v might find out another path which leads back to u (i.e. a back edge/cycle).
    . So v's low link value would have already been updated to the correct lowest low link value for that SCC using the idea #2 given below.
2. Usually inside a strongly connected component, there might be back edges to nodes which were already visited ( i.e. a cycle ).
    . how do we know that something was already seen before? => it is on the dfs stack when exploring the current node.
        - i.e. when exploring v (after u-> v) we might see that v has an edge back to u in which case u will be on the dfs stack at that point in time.
    . Therefore, even here, the low link values of both these nodes u, v should eventually be the same.
    . Why not update it right then and there?
        low[u] = min(low[u], disc[v])
    . i.e there might be an edge from u->v where v is already an ancestor on the stack => it was already discovered earlier itself, so we can use the earlier discovery time to update.
    . this way nodes being explored later also will get the same low link value as the ancestor which was already discovered before.
    . NOTE: we cannot just simply do low[u] = disc[v] because there might be multiple neighbours v which had been discovered before. But we always need to update it to the EARLIEST discovered node.
        - this is why we take the min so that the earliest discovery time is preserved across multiple backedges by updating it in the low[u] everytime!
    . when combined with rule #1, all of the nodes in the dfs stack belonging to the same SCC will keep updating its low link value to be the same.
3. Usually all the nodes in one SCC clump up together on the stack and the start node/ root node ( lets call that as 'u') of that SCC will always have:
    . low[u] = disc[u]
    . this is because that node (u) was the first one to be discovered and from there the dfs started and went onwards.
     . Eventually after exploring all the nodes, using rules #1 and #2 all nodes in its SCC will have the same low link values
    . but only this node will have the same low link value as the discovery time.
    . this root node will also be somewhere on towards the bottom of the stack since it was old discovered node.
    . Now we just have to keep popping the stack and collecting until we reach this particular node u.
    . All collected items will belong to the same SCC !! :)
'''

class Solution:

    # Function to return a list of lists of integers denoting the members of strongly connected components in the given graph.
    def tarjans(self, V, adj):
        '''

        :param V: no of vertices
        :param adj: adjecency list
        :return:
        '''

        self.time = 0 # Discovery time counter
        self.disc = [None] * V  # Discovery time of nodes
        self.low = [None] * V  # Lowest discovery time reachable from each node

        self.stack = []  # Stack to keep track of nodes in current SCC
        self.on_stack = [False] * V  # Boolean array to track stack presence

        self.sccs = []  # List to store the SCCs

        # Perform DFS on each node, as long as it was not already discovered!
        for i in range(V):
            if not self.disc[i]:
                self.dfs(i, adj)

         # sort it in lexograpically ascending order
        self.sccs = [sorted(scc) for scc in self.sccs]
        self.sccs.sort(key=lambda scc: scc[0])

        return self.sccs

    def dfs(self, u, adj):
        '''

        :param u: curr node being explored
        :param adj: adjacency list
        '''

        self.disc[u] = self.low[u] = self.time # assign discovery time and low-ling value to the current time
        self.time += 1 #increment time

        # push onto stack and mark as onstack
        self.stack.append(u)
        self.on_stack[u] = True

        # explore neighbours
        for v in adj[u]:
            # NOTE: all the nodes which were already discovered would have been a part of another SCC so we should not process them again !

            if not self.disc[v]:# neighbor not visited, then visit it and update the low link time
                self.dfs(v, adj)
                self.low[u] = min(self.low[u], self.low[v]) # after the neighbour is completely explored update the low link value of u to that of v, since whatever is reachable from v is also reachable from u.
            elif self.on_stack[v]: # if neighbor was already visited/discovered and also on the stack, which means it is an ancestor/ belongs to the same SCC.
                self.low[u] = min(self.low[u], self.disc[v])

        # Now node u has finished doing dfs. This node u could be the root of a particular SCC if disc[u] == low[u]
        if self.disc[u] == self.low[u]: # checking if u is the root of it's SCC !
            scc = []
            while True:
                node = self.stack.pop()
                self.on_stack[node] = False
                scc.append(node)
                if node == u: # since this node u would have been somewhere in the bottom of the dfs stack considering that it started the dfs in the first place!!
                    break
            self.sccs.append(scc)