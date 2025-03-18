class SCC:
    def __init__(self, adj):
        self.adj = adj

    '''
    KOSARAJU ALGORITHM

    . Strongly connected components only work in directed graphs, where inside one 'scc' every pair of vertices is reachable from the other
    . Main ideas:
        0. Assuming we know what the SCCs are we can combine them into a 'super node' and we can still see a directed graph of super nodes.
            - the last super node is the one which will finish first in the traversal ( i.e. last in the graph to be visited)
            - assuming we reverse the edges, whatever was already a super node will continue to be a super node, just that from the src super node we can
            no longer visit the other super nodes
        1. do a dfs , visit every node only once & keep track of the finishing times of each node (say in a stack)
            - so the nodes which finish first will be on the bottom on the stack and the nodes which finish the last will be on the top
        2. reverse the graph's edges.
            - this way whatever was already a scc will continue to be a scc
            - from the src scc ( i.e. the last finishing node) we can no longer visit the other scc's
        3. do a dfs in the order of last finishing and collect each of the scc's
            - now doing a dfs will only yield an scc as we then have to move onto the next in the finishing order
     '''

    def kosaraju(self, adj=None):
        if adj == None:
            adj = self.adj

        # 1. get the finishing order
        finished_node_stack = self.get_finish_order_dfs(adj)

        # 2. get reversed graph
        reverse_adj = self.reverse_graph(adj)

        # 3. find scc's
        sccs = self.find_sccs_using_reverse_graph_dfs(reverse_adj, finished_node_stack)
        # print(f"sccs are: {scc}")

        return len(sccs)

    def get_finish_order_dfs(self, adj):
        # lets just assume that we start dfs from node #0
        visited = set()
        finishing_node_stack = []

        # function to go through stuff
        def dfs(node):
            if node not in visited:
                visited.add(node)

                for neighbor in adj[node]:
                    dfs(neighbor)

                finishing_node_stack.append(node)

        # do dfs across all nodes
        for node in adj.keys():
            dfs(node)

        # return the finishing order
        return finishing_node_stack

    def reverse_graph(self, adj):
        reverse_adj = {k: [] for k in adj}

        for i, js in adj.items():
            for j in js:
                reverse_adj[j].append(i)

        return reverse_adj

    def find_sccs_using_reverse_graph_dfs(self, reverse_adj, finished_node_stack):
        sccs = []  # list of sets of sccs
        processed = set()

        while finished_node_stack:
            node = finished_node_stack.pop()

            # skip if already processed
            if node in processed:
                continue

            # find out the scc and add nodes to the processed set
            scc = self.dfs(node, reverse_adj, processed, [])

            # add to final list of sccs
            sccs.append(scc)

        return sccs

    # common helpers
    def dfs(self, node, adj, visited=set(), collect=[]):
        if node not in visited:
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    collect = self.dfs(neighbor, adj, visited, collect)
            collect.append(node)

        return collect

if __name__ == '__main__':
    adj = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [4],
        4: [5, 7],
        5: [6],
        6: [4],
        7: []
    }

    # 4 sccs are {0,1,2} , {3} , {4,5,6} , {7}
    scc = SCC(adj)
    print(scc.kosaraju(adj))
