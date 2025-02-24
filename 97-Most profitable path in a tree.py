'''
Leetcode 2467: https://leetcode.com/problems/most-profitable-path-in-a-tree/description/

There is an undirected tree with n nodes labeled from 0 to n - 1, rooted at node 0. You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.

At every node i, there is a gate. You are also given an array of even integers amount, where amount[i] represents:

the price needed to open the gate at node i, if amount[i] is negative, or,
the cash reward obtained on opening the gate at node i, otherwise.
The game goes on as follows:

Initially, Alice is at node 0 and Bob is at node bob.
At every second, Alice and Bob each move to an adjacent node. Alice moves towards some leaf node, while Bob moves towards node 0.
For every node along their path, Alice and Bob either spend money to open the gate at that node, or accept the reward. Note that:
If the gate is already open, no price will be required, nor will there be any cash reward.
If Alice and Bob reach the node simultaneously, they share the price/reward for opening the gate there. In other words, if the price to open the gate is c, then both Alice and Bob pay c / 2 each. Similarly, if the reward at the gate is c, both of them receive c / 2 each.
If Alice reaches a leaf node, she stops moving. Similarly, if Bob reaches node 0, he stops moving. Note that these events are independent of each other.
Return the maximum net income Alice can have if she travels towards the optimal leaf node.


'''

from typing import List
from collections import deque

class Solution:
    def getBobToRootPath(self, bob, graph):
        frontier = deque([
            [bob, [bob]]  # node, path
        ])

        seen = [False] * len(graph.keys())
        while frontier:
            node, path = frontier.popleft()

            seen[node] = True

            if node == 0:
                return path

            for neigh in graph[node]:
                if not seen[neigh]:
                    frontier.append([neigh, path + [neigh]])

        return None

    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        # build graph
        graph = {node: [] for node in range(len(amount))}

        for i, j in edges:
            graph[i].append(j)
            graph[j].append(i)

        # find bobs optimal path
        bobPath = self.getBobToRootPath(bob, graph)
        assert len(bobPath) > 0, "cant find path from bob to alice!"

        # simulate
        cost = float("-inf")

        # alice frontier
        frontier = [
            [0, amount[0], 1] #node, cost to node, alice_steps
        ]
        seen = [False] * len(graph.keys())

        while frontier:
            node, cost_to_node, steps = frontier.pop()
            seen[node] = True

            unseen_neighbors = list(filter(lambda neigh: not seen[neigh], graph[node]))
            if len(unseen_neighbors) == 0:
                cost = max(cost, cost_to_node)
                continue

            for neigh in unseen_neighbors:
                neigh_cost = cost_to_node
                bob_steps = bobPath[:steps + 1]

                if neigh == bob_steps[-1]:
                    neigh_cost += amount[neigh] // 2
                elif neigh in bob_steps:
                    neigh_cost += 0 #dont do anything
                else:
                    neigh_cost += amount[neigh]

                frontier.append([neigh, neigh_cost, steps + 1])


        print(f"final cost is : {cost}")
        return cost

if __name__ == '__main__':
    s = Solution()

    edges = [[0, 1], [1, 2], [1, 3], [3, 4]]
    bob = 3
    amount = [-2, 4, 2, -4, 6]
    ans = s.mostProfitablePath(edges, bob, amount)
    print(ans, ans == 6)

    edges = [[0,1]]
    bob = 1
    amount = [-7280,2350]
    ans = s.mostProfitablePath(edges, bob, amount)
    print(ans, ans == -7280)