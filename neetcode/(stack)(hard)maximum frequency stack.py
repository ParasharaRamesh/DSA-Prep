'''
Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.

Implement the FreqStack class:

FreqStack() constructs an empty frequency stack.
void push(int val) pushes an integer val onto the top of the stack.
int pop() removes and returns the most frequent element in the stack.
If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.
Example 1:

Input: ["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]

Output: [null, null, null, null, null, null, null, 5, 7, 5, 4]
Explanation:
FreqStack freqStack = new FreqStack();
freqStack.push(5); // The stack is [5]
freqStack.push(7); // The stack is [5,7]
freqStack.push(5); // The stack is [5,7,5]
freqStack.push(7); // The stack is [5,7,5,7]
freqStack.push(4); // The stack is [5,7,5,7,4]
freqStack.push(5); // The stack is [5,7,5,7,4,5]
freqStack.pop(); // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
freqStack.pop(); // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
freqStack.pop(); // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
freqStack.pop(); // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].

Constraints:

0 <= val <= 1,000,000,000
At most 20,000 calls will be made to push and pop.
It is guaranteed that there will be at least one element in the stack before calling pop.

'''
from collections import defaultdict
from heapq import *

'''
. I went down the rabbit hole of trying to maintain a sortedDict of values
. which is not really needed in this case
. even though it looks like groups might contain stale data since pushing the same value again means that it is has now become a part of a new group we dont remove it from the older groups even though its incorrect because we keep track of the max freq anyways

'''
class FreqStack:
    def __init__(self):
        # value -> frequency
        self.freq = defaultdict(int)
        # frequency -> stack of values with that frequency
        self.groups = defaultdict(list)
        # current maximum frequency
        self.maxfreq = 0

    def push(self, val: int) -> None:
        f: int = self.freq[val] + 1
        self.freq[val] = f
        self.groups[f].append(val)
        if f > self.maxfreq:
            self.maxfreq = f

    def pop(self) -> int:
        # take the most frequent and most recently pushed among them
        val = self.groups[self.maxfreq].pop()

        # decrement the frequency
        self.freq[val] -= 1

        # if at all that was the last value in the group[maxFreq] stack => decrement maxFreq
        if not self.groups[self.maxfreq]:
            self.maxfreq -= 1
        return val
'''
. here the max heap is based on the frequency and the index as the next tie breaker
. push and pop is now logarithmic
'''
class FreqStack_heap:

    def __init__(self):
        self.heap = []
        self.cnt = defaultdict(int)
        self.index = 0

    def push(self, val: int) -> None:
        self.cnt[val] += 1
        heapq.heappush(self.heap, (-self.cnt[val], -self.index, val))
        self.index += 1

    def pop(self) -> int:
        _, _, val = heapq.heappop(self.heap)
        self.cnt[val] -= 1
        return val