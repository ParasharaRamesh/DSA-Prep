'''
You are given an array of CPU tasks tasks, where tasks[i] is an uppercase english character from A to Z. You are also given an integer n.

Each CPU cycle allows the completion of a single task, and tasks may be completed in any order.

The only constraint is that identical tasks must be separated by at least n CPU cycles, to cooldown the CPU.

Return the minimum number of CPU cycles required to complete all tasks.

Example 1:

Input: tasks = ["X","X","Y","Y"], n = 2

Output: 5
Explanation: A possible sequence is: X -> Y -> idle -> X -> Y.

Example 2:

Input: tasks = ["A","A","A","B","C"], n = 3

Output: 9
Explanation: A possible sequence is: A -> B -> C -> Idle -> A -> Idle -> Idle -> Idle -> A.

Constraints:

1 <= tasks.length <= 1000
0 <= n <= 100

Insights:
. Initialize a frequency map using Counter to count how often each task appears.
. Set up a max heap, a deque (for cooldown tracking), and a timer.
. Add all tasks from the frequency map to the max heap, storing their negative frequencies (to get the max heap).
. While there are tasks left in either the heap or the cooldown queue:
    - Pop the task with the highest frequency from the heap. If it has remaining executions, add it to the cooldown queue with its next available time (timer + n + 1), and decrement its execution count.
    - Increment the timer by 1. This has to be done outside of both heap and queue loops, because if the heap is empty (no ready tasks to be executed) but the queue contains items that cannot be popped (because the tasks are still cooling), the timer still has to increase as this represents idle time.
    - Check the cooldown queue for any tasks whose cooldown has expired (i.e., timer == next available time). If so, move the task from the cooldown queue back into the heap. Only one task from the cooldown queue will be ready to return to the heap at each time interval because we are processing the tasks one interval at a time.
. Once both the heap and the cooldown queue are empty, all tasks have been completed, and the timer is returned.


'''

from typing import List
from collections import Counter, deque
import heapq


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        freq = Counter(tasks)
        heap = []
        cooldown = deque()
        timer = 0

        # create a max heap
        for key, value in freq.items():
            heapq.heappush(heap, -value)

        while heap or cooldown:
            if heap:
                task = -heapq.heappop(heap)
                if task > 1:
                    cooldown.append((task - 1, timer + n + 1))
            timer += 1

            while cooldown and cooldown[0][1] == timer:
                task_count, next_iteration = cooldown[0]
                cooldown.popleft()
                heapq.heappush(heap, -task_count)

        return timer


if __name__ == '__main__':
    s = Solution()

    tasks = ["A","B","C","A"]
    n = 2
    res = s.leastInterval(tasks, n)
    assert res == 4, f"expected: 4, was {res}"

    tasks = ["A","A"]
    n = 2
    res = s.leastInterval(tasks, n)
    assert res == 4, f"expected: 4, was {res}"

    tasks = ["A","A","A","B","B","B"]
    n = 2
    res = s.leastInterval(tasks, n)
    assert res == 8, f"expected: 8, was {res}"

    tasks = ["A","C","A","B","D","B"]
    n = 1
    res = s.leastInterval(tasks, n)
    assert res == 6, f"expected: 6, was {res}"

    tasks = ["A","A","A", "B","B","B"]
    n = 3
    res = s.leastInterval(tasks, n)
    assert res == 10, f"expected: 10, was {res}"