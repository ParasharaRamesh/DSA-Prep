'''
. Its a pattern for finding the maximum/minimum in a range very quickly in an online manner.
. Take a look at the solution of "sliding window maximum"
. what this means is that if the state of the queue is something like

[ 9-0 ,  6-4,  2-8,  .. ] => from [0, 4) : 9 is the maximum from [4,8): 6 is the maximum and so on ..

. To find maximum => use monotonic decreasing queue
. To find minimum => use monotonic increasing queue
. A Monotonic Queue cannot answer "What is the max in [L, R]?" for any random L and R given at any time.
. It is O(1) only in the context of a sliding window where the boundaries L and R move monotonically (usually R increases, and L follows).
. As you build it (move R), you maintain the queue. At any given moment, the front of the queue is the answer for the current [L, R].
. If someone asks about a range that already passed or a range far ahead, the Monotonic Queue doesn't help unless you "replay" the process.

Sample problems where this can be used:
1. Static sliding window maximum 
2. Max sum subarray of length atmost k 
. if it was exactly equal to k then its trivial static sliding window problem which is not the case here
. because this has negative numbers the sum is not monotonic 
. this means if we have prefix sums, we need to find the min p[x] for x in range [i-1, j) in the formula (p[j] - p[i-1]) -> so that we get the max value
. so we just ask the query at each p[j] what is the p[min] and this sliding window minimum can be answered in an online manner using monotonic queue pattern

3. Longest Subarray with Max-Min <= K
. maintain 2 monotonic queues for figuring out both the max and min in an online way using monotonic decreasing and increasing deques

4. In how many subarrays is a particular A[i] maximum or minimum?
=>  depends on the state of the deque in the end where you can compare adjacent elements to see regions of influence

'''

from collections import deque

def longest_subarray_with_limit(nums, k):
    max_q = deque() # Decreasing: front is max
    min_q = deque() # Increasing: front is min
    left = 0
    max_len = 0
    
    for right in range(len(nums)):
        # Maintain max_q (Decreasing)
        while max_q and max_q[-1] < nums[right]:
            max_q.pop()
        max_q.append(nums[right])
        
        # Maintain min_q (Increasing)
        while min_q and min_q[-1] > nums[right]:
            min_q.pop()
        min_q.append(nums[right])
        
        # If max - min > k, the window is invalid
        while max_q[0] - min_q[0] > k:
            # If the element we are leaving behind was a min or max,
            # we must remove it from the front of the corresponding queue
            if nums[left] == max_q[0]:
                max_q.popleft()
            if nums[left] == min_q[0]:
                min_q.popleft()
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len