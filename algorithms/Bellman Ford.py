'''
. This is also a single source shortest path algorithm, but has a worse timecomplexity than Dijkstra with O(EV)
. This algorithm can also handle negative edges and can also be used to detect negative cycles
. Basically we try to relax the distances to each node everytime, whereas in dijstra's with a heap and a greedy implementation we just pick the smallest edge everytime and once a node is processed it is never revisited.
. In the case of negative cycles, Bellman Fod (BF) can help since it can also detect longer paths with negative edges which might lead to shorter costs in total which wont be the case when doing dijstra's
. Even though you're looking at all edges in every pass, you can't use an edge to relax a target node unless the source node already has a correct distance.
That’s why we need V-1 passes to propagate shortest distances along paths of length up to V-1 edges.
. K Hop constrained shortest paths property:
d[x] after n passes = min distance from src to x over all paths with ≤ n edges
. NOTE: this property is true only in the case where we use copies of the distances and do the BF update in a stable way. If not this is not true
'''

''' 1. classic bellman ford with in place updates => its not guaranteed to obey the k hop shortest path constraint property since its unstable updates'''


def classic_bellman_ford(graph, V, source):
    # Initialize distances from source to all vertices as infinite
    dist = [float('inf')] * V
    dist[source] = 0

    # Relax all edges V-1 times ( v-1 times because assuming that it did obey that k hop constraing, then the longest path which is a direct linkedlist would have exactly v-1 edges) so better do it v-1 times to get the final answer
    for _ in range(V - 1):
        for u, v, weight in graph:
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight

    # Check for negative-weight cycles ( just one more pass and if we can still improve means that for sure we have negative edges )
    for u, v, weight in graph:
        if dist[u] != float('inf') and dist[u] + weight < dist[v]:
            print("Graph contains negative weight cycle")
            return None

    '''
    If we want to detect what nodes are present in this negative cycle, we can as well put all the 'v' nodes in the last pass in a set and do kosaraju to find all the strongly connnected components and from that filter to get the ones which have the negative cycle edge weights
    '''
    return dist

'''
2. K Constraint shortest hop property obeying stable bellman ford algorithm.

as for why this works, this is because we are doing stable updates by using the copy of the distances from the previous pass which means that in every pass (k)
we only update that node if its neighbour ( which was say k-1 hops away from the src ) was updated at all to begin with in the previous pass (i.e k-1th pass)
which is why in the kth pass , we can use the shortest k-1 hop distance from its neighbor /parent to update the kth hop distance to this node. 

And across all other k hop paths from all its other neighbours ( which were also k-1 away from src ) will be used to update this => FOR SURE, we get the lowest distance to this node (x)
after k hops ( after considering all other k hop edge distances from src )

'''
def bellman_ford_k_hops(graph, V, source, k):
    dist = [float('inf')] * V
    dist[source] = 0

    for _ in range(k):
        # in this particular pass, new_dist is the one which will be updated using the old value from the previous pass i.e. from dist
        new_dist = dist.copy()
        for u, v, weight in graph:
            # use old value (u) -> to update -> potential new value of v.
            if dist[u] != float('inf') and dist[u] + weight < new_dist[v]:
                new_dist[v] = dist[u] + weight
        # update the old dist with the new dist, so that in the next pass, dist will have the updated values from this kth pass distances ( i.e. new_dist )
        dist = new_dist

    return dist
