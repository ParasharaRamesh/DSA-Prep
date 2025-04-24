'''
You are given a list of flight tickets tickets where tickets[i] = [from_i, to_i] represent the source airport and the destination airport.

Each from_i and to_i consists of three uppercase English letters.

Reconstruct the itinerary in order and return it.

All of the tickets belong to someone who originally departed from "JFK". Your objective is to reconstruct the flight path that this person took, assuming each ticket was used exactly once.

If there are multiple valid flight paths, return the lexicographically smallest one.

For example, the itinerary ["JFK", "SEA"] has a smaller lexical order than ["JFK", "SFO"].
You may assume all the tickets form at least one valid flight path.

Example 1:



Input: tickets = [["BUF","HOU"],["HOU","SEA"],["JFK","BUF"]]

Output: ["JFK","BUF","HOU","SEA"]
Example 2:



Input: tickets = [["HOU","JFK"],["SEA","JFK"],["JFK","SEA"],["JFK","HOU"]]

Output: ["JFK","HOU","JFK","SEA","JFK"]
Explanation: Another possible reconstruction is ["JFK","SEA","JFK","HOU","JFK"] but it is lexicographically larger.

Constraints:

1 <= tickets.length <= 300
from_i != to_i

'''
from typing import List
from collections import defaultdict

# Better solution, try to be greedy and if not backtrack
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # sort it in alphabetical order in both places
        tickets.sort(key=lambda x: (x[0], x[1]))

        graph = defaultdict(list)
        for i, j in tickets:
            graph[i].append(j)

        # start dfs from jfk, but we always try to pick the smallest one first
        itinerary = ["JFK"]

        def dfs(node):
            # found a lexicographically smallest path!
            if len(itinerary) - 1 == len(tickets):
                return True

            # base case, although there might be a case where the node is removed from the graph
            if node not in graph or len(graph[node]) == 0:
                return False

            temp = graph[node]
            for i, neigh in enumerate(temp):
                # removing that neighbour from future dfs calls down the line
                graph[node].pop(i)
                if not graph[node]:
                    # removing the key itself
                    graph.pop(node)
                itinerary.append(neigh)

                # try out this path
                if dfs(neigh):
                    return True

                # if that didn't work we need to rollback the operations
                if node not in graph:
                    graph[node] = [neigh]
                else:
                    graph[node].insert(i, neigh)
                itinerary.pop()

            # nothing worked out
            return False

        # try dfs from jfk, somewhere it will return the correct order
        dfs("JFK")
        return itinerary


# TLE with dfs, MLE with bfs :(
class Solution_error:
    def updateItinerary(self, itinerary, path):
        if len(itinerary) == 0:
            return path

        # retain the one which is lexographically smaller
        for i_n, p_n in zip(itinerary, path):
            if i_n > p_n:
                return path
            elif i_n < p_n:
                return itinerary

        return itinerary

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # construct graph
        num_edges = len(tickets)
        graph = defaultdict(list)
        for i, j in tickets:
            graph[i].append(j)

        # start dfs with all edges from JFK
        itinerary = []
        frontier = [("JFK", j, [], set()) for j in graph["JFK"]]

        # multisource dfs
        while frontier:
            i, j, path, visited_edges = frontier.pop()

            if (i, j) not in visited_edges:
                visited_edges.add((i, j))
                path.append(i)

            if len(visited_edges) == num_edges:
                path.append(j)
                itinerary = self.updateItinerary(itinerary, path)
                continue

            for k in graph[j]:
                if (j, k) not in visited_edges:
                    frontier.append((j, k, path.copy(), visited_edges.copy()))

        return itinerary


if __name__ == '__main__':
    s = Solution()

    tickets = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    expected = ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
    itinerary = s.findItinerary(tickets)
    assert expected == itinerary, f"expected: {expected}, but was: {itinerary}"

    tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    expected = ["JFK", "MUC", "LHR", "SFO", "SJC"]
    itinerary = s.findItinerary(tickets)
    assert expected == itinerary, f"expected: {expected}, but was: {itinerary}"
