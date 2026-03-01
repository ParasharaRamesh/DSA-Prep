'''
You have a lock with 4 circular wheels. Each wheel has 10 slots: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot.

The lock initially starts at '0000', a string representing the state of the 4 wheels.

You are given a list of deadends dead ends, meaning if the lock displays any of these codes, the wheels of the lock will stop turning and you will be unable to open it.

Given a target representing the value of the wheels that will unlock the lock, return the minimum total number of turns required to open the lock, or -1 if it is impossible.

Example 1:

Input: deadends = ["1111","0120","2020","3333"], target = "5555"

Output: 20
Example 2:

Input: deadends = ["4443","4445","4434","4454","4344","4544","3444","5444"], target = "4444"

Output: -1
Constraints:

1 <= deadends.length <= 500
deadends[i].length == 4
target.length == 4
target will not be in the list deadends.
target and deadends[i] consist of digits only.
'''

from collections import deque
from copy import deepcopy

class Solution:
    def get_neighbours(self, state: str, deadends: set(str), visited: set(str)) -> List[str]:
        neighbours = []
        state = list(state)
        for i in range(len(state)):
            num = int(state[i])

            plus1 = state.copy()
            plus1[i] = str((num + 1) % 10)
            plus1 = "".join(plus1)
            if plus1 not in deadends and plus1 not in visited:
                neighbours.append(plus1)

            plus2 = state.copy()
            plus2[i] = str((num - 1) % 10)
            plus2 = "".join(plus2)
            if plus2 not in deadends and plus2 not in visited:
                neighbours.append(plus2)

        return list(neighbours)

    def openLock(self, deadends: List[str], target: str) -> int:
        start = "0000"
        deadends = set(deadends)
        visited = set()

        if start in deadends:
            return -1

        frontier = deque([(start, 0)])

        while frontier:
            node, steps = frontier.popleft()

            if node == target:
                return steps

            # get neighbours which are not deadends and not in visited
            neighbours = self.get_neighbours(node, deadends, visited)

            for neigh in neighbours:
                visited.add(neigh)
                frontier.append((neigh, steps + 1))

        return -1