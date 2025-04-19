'''
Given a node in a connected undirected graph, return a deep copy of the graph.

Each node in the graph contains an integer value and a list of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}
The graph is shown in the test cases as an adjacency list. An adjacency list is a mapping of nodes to lists, used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

For simplicity, nodes values are numbered from 1 to n, where n is the total number of nodes in the graph. The index of each node within the adjacency list is the same as the node's value (1-indexed).

The input node will always be the first node in the graph and have 1 as the value.

Example 1:



Input: adjList = [[2],[1,3],[2]]

Output: [[2],[1,3],[2]]
Explanation: There are 3 nodes in the graph.
Node 1: val = 1 and neighbors = [2].
Node 2: val = 2 and neighbors = [1, 3].
Node 3: val = 3 and neighbors = [2].

Example 2:



Input: adjList = [[]]

Output: [[]]
Explanation: The graph has one node with no neighbors.

Example 3:

Input: adjList = []

Output: []
Explanation: The graph is empty.

Constraints:

0 <= The number of nodes in the graph <= 100.
1 <= Node.val <= 100
There are no duplicate edges and no self-loops in the graph.

'''
from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        adj = dict()

        # lets not do bidirected adj
        def build_adj(node):
            nonlocal adj

            if not node:
                return

            if node.val in adj:
                # skip it
                return

            adj[node.val] = [neigh.val for neigh in node.neighbors]

            for neigh in node.neighbors:
                build_adj(neigh)

        build_adj(node)

        def deep_copy():
            nodes = dict()

            # creating a ref for that node
            for node_val in adj:
                nodes[node_val] = Node(node_val)

            # go through again
            for node_val, neighbors in adj.items():
                for neigh_val in neighbors:
                    neigh_node = nodes[neigh_val]
                    nodes[node_val].neighbors.append(neigh_node)

            return nodes[1] if 1 in nodes else None

        return deep_copy()
