from collections import deque
from typing import Dict, Iterable, List, Hashable


def dfs_recursive(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Recursive Depth-First Search.

    graph: adjacency list, e.g. {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
    start: starting node/key present in the graph

    returns: list of nodes in visitation order
    """
    order: List[Hashable] = []
    visited = set()

    def visit(node: Hashable) -> None:
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, []):
            visit(neighbor)

    visit(start)
    return order


def dfs_iterative(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Iterative Depth-First Search using an explicit stack.

    Push neighbors in reverse order to mimic recursive pre-order on lists.
    """
    order: List[Hashable] = []
    visited = set()
    stack: List[Hashable] = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        neighbors = list(graph.get(node, []))
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def bfs(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Breadth-First Search using a queue.
    """
    order: List[Hashable] = []
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order