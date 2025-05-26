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

    def leastInterval_math(self, tasks: List[str], n: int) -> int:
        freq = [0] * 26
        for t in tasks:
            freq[ord(t) - ord('A')] += 1

        max_freq = max(freq)
        max_count = sum(1 for f in freq if f == max_freq)

        blocks = max_freq - 1
        block_size = n + 1

        # Total slots excluding the last max frequency tasks
        total_slots = blocks * block_size

        # Add the last max frequency tasks
        total_slots += max_count

        # DEBUG
        # Number of tasks placed in max frequency slots
        tasks_placed = max_freq * max_count
        # Remaining tasks to fill idle slots
        remaining_tasks = len(tasks) - tasks_placed

        # Calculate idle slots needed after placing remaining tasks
        idle_slots = total_slots - len(tasks)

        # If we have more idle slots than remaining tasks, idle time is needed
        # Otherwise, tasks fill the schedule fully, no idle needed
        if idle_slots > 0:
            return total_slots
        else:
            return len(tasks)


'''

## 🧠 Goal:

Minimize CPU cycles to finish all tasks **with cooldown `n`** between same tasks.

---

## ✅ Key Insight:

The **bottleneck** is the **most frequent task**. It forces the most constraints on spacing due to the cooldown `n`.

---

## 🤔 Step-by-step Derivation (How You Could Have Thought of It)

---

### **Step 1: Think in terms of scheduling blocks**

Suppose the task `"A"` appears 3 times, and no other task appears as frequently.

With `n = 2`, you want to separate A’s occurrences like this:

```
A _ _ A _ _ A
```

Each `_` must be filled with:

* A different task, or
* Idle if nothing else can go there.

This creates a skeleton: `(maxf - 1)` full **blocks** of size `(n + 1)` each, and then finally the last occurrence of "A".

Let’s say:

* `maxf = frequency of most frequent task`
* Then you need `(maxf - 1)` full *gaps* of `n` between them.

So, total time without considering other tasks:

```
time = (maxf - 1) * (n + 1) + 1
```

But…

---

### **Step 2: Generalize for multiple max-frequency tasks**

If you have:

```
tasks = ["A", "A", "A", "B", "B", "B"], n = 2
```

You'd like to lay them out as:

```
A B _ A B _ A B
```

→ Both A and B appear 3 times (same frequency). They can fill their own "columns" in the same skeleton.

This leads to the full formula:

```python
time = (maxf - 1) * (n + 1) + maxCount
```

* `maxCount = number of tasks with maxf frequency`
* Why? Because in the last block, we may need multiple high-freq tasks side by side.

---

### **Step 3: Compare with total number of tasks**

Sometimes, there's *enough variety* of tasks to fully fill all idle slots. In that case, the greedy block model underestimates real CPU time.

So the actual answer is:

```python
return max(len(tasks), time)
```

* If there are many tasks, we naturally fill in the gaps (no idle needed).
* If not, we need idle cycles to respect cooldown.

---

## 💡 Example Walkthrough (with math)

```python
tasks = ["A", "A", "A", "B", "C"], n = 3
```

* Frequencies: A=3, B=1, C=1
* `maxf = 3` (A)
* `maxCount = 1` (only A has that frequency)

→ `time = (3 - 1) * (3 + 1) + 1 = 2 * 4 + 1 = 9`

Do we need all 9 slots? Yes. B and C only fill 2 of the 6 gaps. The rest are idles.

---

## ✅ Why This Is a Valid and Optimal Strategy

This is **greedy packing**:

* Spread the most frequent tasks as far apart as cooldown allows.
* Fill remaining idle slots with other tasks.
* If tasks overflow the gaps, great! Less idle time.

This is provably optimal because:

* If you don’t spread the most frequent task optimally, you’ll have to insert more idles later.
* This method uses the fewest possible idles, or none at all if task variety allows.

---

## 🔁 How to Rediscover It:

Ask yourself:

1. “Which task constrains the schedule the most?” → The most frequent one.
2. “How many gaps must be between its appearances?” → `n`
3. “How can I layout a minimal valid schedule?” → Fixed-sized blocks with gaps.
4. “What if others share this frequency?” → Stack them in last block.
5. “What if I have many other tasks?” → Compare with total task count.

---

## ✨ Summary of the Formula:

```python
time = (maxf - 1) * (n + 1) + maxCount
return max(time, len(tasks))
```

* `maxf`: frequency of the most frequent task
* `maxCount`: number of tasks with that max frequency
* `len(tasks)`: actual number of CPU steps needed if there's enough variety to fill gaps

---


'''



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