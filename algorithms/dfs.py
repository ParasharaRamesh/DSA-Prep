from collections import deque
from typing import Dict, Iterable, List, Hashable


def dfs_recursive(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Recursive Depth-First Search (DFS) — Style B (visited check inside neighbor loop).

    Core invariant of this implementation:
    --------------------------------------
    A node is marked `visited` IMMEDIATELY when the DFS function is entered.
    This moment corresponds exactly to pushing the node onto the recursion stack.

    This is also exactly equivalent to the iterative dfs code with the stack .. because we marking visited on push to the stack

    Why this is mandatory:
    ----------------------
    1. The Python call stack *is* the DFS stack.
       Calling `visit(node)` pushes a new frame onto that stack.

    2. Graphs may contain cycles.
       If a node is not marked visited at entry time, a back-edge can
       cause the same node to be re-entered while it is already on the
       call stack, leading to infinite recursion.

    3. DFS does not rely on shortest paths or optimality.
       Once a node is discovered, there is no benefit to rediscovering
       it via a different path.

    Meaning of `visited`:
    ---------------------
    `visited` means "this node has already been DISCOVERED",
    not "this node has been fully processed".

    Therefore:
    ----------
    - Nodes currently in the recursion stack are already visited.
    - Nodes are never re-entered once discovered.

    Style B explanation:
    --------------------
    In this style, the `visited` check is placed at the edge traversal
    level (inside the neighbor loop), rather than as a guard at function
    entry.

    This works *only because* the node is marked visited immediately
    upon entry to the function.

    This style:
    - Avoids unnecessary recursive calls that immediately return
    - Closely mirrors the canonical iterative DFS pattern
    - Reads naturally as "traverse unvisited neighbors"

    Summary rule:
    -------------
    - Mark visited on function entry
    - Recurse only on unvisited neighbors
    """

    order: List[Hashable] = []
    visited = set()

    def visit(node: Hashable) -> None:
        # DISCOVERY STEP:
        # Mark the node visited immediately upon entry.
        # This is equivalent to pushing the node onto the DFS stack.
        visited.add(node)

        # PREORDER ACTION:
        # Record the node at discovery time.
        order.append(node)

        # EDGE EXPLORATION:
        # Only recurse into neighbors that have not yet been discovered.
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

        # FUNCTION RETURN = BACKTRACKING.
        # No visited update is needed here because discovery is already complete.

    # Start DFS from the given start node.
    visit(start)
    return order



def dfs_iterative(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Iterative Depth-First Search (DFS) using an explicit stack.

    Core invariant of this implementation:
    --------------------------------------
    A node is marked `visited` at the moment it is PUSHED onto the stack
    (i.e., when it is first discovered), not when it is popped.

    Why this matters:
    -----------------
    1. Graphs may contain cycles.
       If a node is NOT marked visited at discovery time, it can be
       pushed onto the stack multiple times by different parents before
       it is ever popped.

    2. Marking visited on push guarantees:
         - Each node is pushed onto the stack at most once
         - The stack size remains bounded by O(V)
         - The traversal always terminates on cyclic graphs

    3. DFS does NOT rely on path optimality (unlike BFS or Dijkstra).
       Once a node is discovered, there is no benefit to rediscovering it
       via another path.

    4. This exactly mirrors recursive DFS semantics:
         - Recursive DFS marks a node visited immediately upon entry
         - The explicit stack version must enforce the same invariant

    Important distinction:
    ----------------------
    - Discovery (push) ≠ Processing (pop)
    - Visited means "already discovered", not "fully processed"

    Therefore:
    ----------
    - Nodes in the stack are already visited
    - No visited check is needed when popping
    """

    order: List[Hashable] = []

    # Mark the start node visited immediately upon discovery.
    visited = {start}

    # The stack contains nodes that have been discovered but not yet processed.
    stack: List[Hashable] = [start]

    while stack:
        node = stack.pop()

        # No "if node in visited" check here.
        # By invariant, every node in the stack is already visited.
        order.append(node)

        # To mimic recursive DFS preorder on adjacency lists,
        # neighbors are pushed in reverse order so that the leftmost
        # neighbor is processed first.
        neighbors = list(graph.get(node, []))
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)      # mark visited at DISCOVERY
                stack.append(neighbor)     # push exactly once

    return order

def bfs(graph: Dict[Hashable, Iterable[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Breadth-First Search (BFS) for an unweighted graph.

    Core invariant of this implementation:
    --------------------------------------
    A node is marked `visited` at the moment it is ENQUEUED (discovered),
    not when it is dequeued (processed).

    Why this matters:
    -----------------
    1. BFS explores nodes in increasing order of distance from `start`.
       Because all edges have equal weight, the FIRST time a node is
       discovered is guaranteed to be via the shortest path.

    2. Once a node is discovered and enqueued, it NEVER needs to be
       enqueued again. Marking it visited immediately prevents:
         - Duplicate entries in the queue
         - Exponential queue growth
         - Redundant neighbor expansions

    3. As a consequence of (2), EVERY node that appears in the queue
       is *already* in `visited`. Therefore:
         - Checking `if node in visited` when dequeuing is incorrect
           and will break the algorithm.
         - The dequeue step can safely assume the node is valid.

    Important distinction:
    ----------------------
    "Not visited yet" does NOT mean "not already enqueued".
    Marking visited on enqueue closes this gap and ensures each node
    is enqueued at most once.

    This is different from Dijkstra's algorithm, where a node may be
    discovered multiple times with different distances and must only
    be finalized when popped from a priority queue.

    Summary rule for BFS:
    ---------------------
    - Mark visited on ENQUEUE
    - Never check visited on DEQUEUE
    """

    order: List[Hashable] = []

    # Initialize the visited set with the start node.
    # This asserts that the start node has already been discovered.
    visited = {start}

    # The queue holds nodes that have been discovered but not yet processed.
    # By invariant, every node in this queue is already in `visited`.
    queue = deque([start])

    while queue:
        # Dequeue the next node in BFS order.
        node = queue.popleft()

        # No "if node in visited" check here!
        # Doing so would be redundant and incorrect, because every node
        # in the queue is guaranteed to already be visited.
        order.append(node)

        # Explore neighbors.
        for neighbor in graph.get(node, []):
            # Only undiscovered neighbors are enqueued.
            # This guarantees that each node is enqueued at most once.
            if neighbor not in visited:
                # Mark visited AT DISCOVERY TIME (enqueue time).
                # This prevents multiple parents from enqueueing
                # the same node before it is dequeued.
                visited.add(neighbor)
                queue.append(neighbor)

    return order