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

    def kosaraju(self, graph=None):
        if graph == None:
            graph = self.adj

        # 1. get the finishing order
        finished_node_stack = self.get_finish_order_dfs(graph)

        # 2. get reversed graph
        reversed_graph = self.reverse_graph(graph)

        # 3. find scc's
        sccs = self.find_sccs_using_reverse_graph_dfs(reversed_graph, finished_node_stack)
        return sccs

    def get_finish_order_dfs(self, graph):
        visited = set()
        finishing_node_stack = []

        # function to go through stuff
        def dfs(node):
            if node not in visited:
                visited.add(node)

                for neighbor in graph[node]:
                    dfs(neighbor)

                finishing_node_stack.append(node)

        # do dfs across all nodes
        for node in graph.keys():
            dfs(node)

        # return the finishing order
        return finishing_node_stack

    def reverse_graph(self, graph):
        reversed_graph = {k: [] for k in graph}

        for i, js in graph.items():
            for j in js:
                reversed_graph[j].append(i)

        return reversed_graph

    def find_sccs_using_reverse_graph_dfs(self, reversed_graph, finished_node_stack):
        sccs = []  # list of sets of sccs
        processed = set()

        while finished_node_stack:
            node = finished_node_stack.pop()

            # skip if already processed
            if node in processed:
                continue

            # find out the scc and add nodes to the processed set
            scc = self.dfs(node, reversed_graph, processed, [])

            # add to final list of sccs
            sccs.append(scc)

        return sccs

    # common helpers
    def dfs(self, node, graph, visited=set(), collector=[]):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    collector = self.dfs(neighbor, graph, visited, collector)
            collector.append(node)

        return collector

if __name__ == '__main__':
    graph = {
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
    scc = SCC(graph)
    print(scc.kosaraju(graph))
