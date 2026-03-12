'''
You are given n tasks labeled from 0 to n - 1 represented by a 2D integer array tasks, where tasks[i] = [enqueueTimei, processingTimei] means that the ith task will be available to process at enqueueTime[i] and will take processingTime[i] to finish processing.

You have a single-threaded CPU that can process at most one task at a time and will act in the following way:

If the CPU is idle and there are no available tasks to process, the CPU remains idle.
If the CPU is idle and there are available tasks, the CPU will choose the one with the shortest processing time. If multiple tasks have the same shortest processing time, it will choose the task with the smallest index.
Once a task is started to process, the CPU will process the entire task without stopping.
The CPU can finish a task then start a new one instantly.
Return the order in which the CPU will process the tasks.

Example 1:

Input: tasks = [[1,4],[3,3],[2,1]]

Output: [0,2,1]
Example 2:

Input: tasks = [[5,2],[4,4],[4,1],[2,1],[3,3]]

Output: [3,4,2,0,1]
Constraints:

1 <= tasks.length <= 100,000
1 <= enqueueTime[i], processingTime[i] <= 1,000,000,000

'''

from heapq import *

class Solution:
    def getOrder_sorting_and_heap(self, tasks: List[List[int]]) -> List[int]:
        n = len(tasks)
        for i, task in enumerate(tasks):
            task.append(i)

        tasks.sort(key = lambda item: (item[0], item[1]))
        order = []
        curr_time = tasks[0][0]
        frontier = []

        # adding all tasks with same start time
        i = 0
        while i < n and tasks[i][0] == curr_time:
            # push duration , ind
            heappush(frontier, [tasks[i][1], tasks[i][2]]) 
            i += 1

        while frontier:
            duration, ind = heappop(frontier)

            order.append(ind)
            curr_time += duration

            # add all tasks with enqueue time <= curr_time
            while i < n and tasks[i][0] <= curr_time:
                heappush(frontier, [tasks[i][1], tasks[i][2]])
                i += 1
            
            # if at all no task was addable then pick the next task with start time > curr_time and all tasks with same start time
            if not frontier and i < n:
                curr_time = tasks[i][0]
                while i < n and tasks[i][0] == curr_time:
                    # push duration , ind
                    heappush(frontier, [tasks[i][1], tasks[i][2]]) 
                    i += 1

        assert len(order) == n,f"{order=} not having length {n}! Missed something!!"
        return order

  def getOrder_two_heaps(self, tasks: List[List[int]]) -> List[int]:
        available = []
        pending = []
        for i, (enqueueTime, processTime) in enumerate(tasks):
            heappush(pending, (enqueueTime, processTime, i))

        time = 0
        res = []
        while pending or available:
            while pending and pending[0][0] <= time:
                enqueueTime, processTime, i = heapq.heappop(pending)
                heappush(available, (processTime, i))

            if not available:
                time = pending[0][0]
                continue

            processTime, i = heapq.heappop(available)
            time += processTime
            res.append(i)

        return res
