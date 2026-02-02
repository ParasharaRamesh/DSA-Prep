'''
You are given a 0-indexed array of integers nums of length n, and two positive integers k and dist.

The cost of an array is the value of its first element. For example, the cost of [1,2,3] is 1 while the cost of [3,4,1] is 3.

You need to divide nums into k disjoint contiguous subarrays, such that the difference between the starting index of the second subarray and the starting index of the kth subarray should be less than or equal to dist. In other words, if you divide nums into the subarrays nums[0..(i1 - 1)], nums[i1..(i2 - 1)], ..., nums[ik-1..(n - 1)], then ik-1 - i1 <= dist.

Return the minimum possible sum of the cost of these subarrays.

 

Example 1:

Input: nums = [1,3,2,6,4,2], k = 3, dist = 3
Output: 5
Explanation: The best possible way to divide nums into 3 subarrays is: [1,3], [2,6,4], and [2]. This choice is valid because ik-1 - i1 is 5 - 2 = 3 which is equal to dist. The total cost is nums[0] + nums[2] + nums[5] which is 1 + 2 + 2 = 5.
It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 5.
Example 2:

Input: nums = [10,1,2,2,2,1], k = 4, dist = 3
Output: 15
Explanation: The best possible way to divide nums into 4 subarrays is: [10], [1], [2], and [2,2,1]. This choice is valid because ik-1 - i1 is 3 - 1 = 2 which is less than dist. The total cost is nums[0] + nums[1] + nums[2] + nums[3] which is 10 + 1 + 2 + 2 = 15.
The division [10], [1], [2,2,2], and [1] is not valid, because the difference between ik-1 and i1 is 5 - 1 = 4, which is greater than dist.
It can be shown that there is no possible way to divide nums into 4 subarrays at a cost lower than 15.
Example 3:

Input: nums = [10,8,18,9], k = 3, dist = 1
Output: 36
Explanation: The best possible way to divide nums into 4 subarrays is: [10], [8], and [18,9]. This choice is valid because ik-1 - i1 is 2 - 1 = 1 which is equal to dist.The total cost is nums[0] + nums[1] + nums[2] which is 10 + 8 + 18 = 36.
The division [10], [8,18], and [9] is not valid, because the difference between ik-1 and i1 is 3 - 1 = 2, which is greater than dist.
It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 36.
 

Constraints:

3 <= n <= 105
1 <= nums[i] <= 109
3 <= k <= n
k - 2 <= dist <= n - 2

'''

'''
Insights:

. DUAL-HEAP SLIDING WINDOW LOGIC (TOP-K SUM)

. ARCHITECTURE: 
  . Best Heap (Max-Heap) tracks the (k-2) smallest values with the largest of those at the top. 
  . Bench Heap (Min-Heap) tracks all other candidates currently in the window. 
  . Counters (HashMaps) are the "Source of Truth" to mark elements as logically deleted. 
  . Variables best_sum and best_size track the current state of the Best bucket.

. THE LAZY JANITOR: 
  . Elements are not physically removed from heaps immediately. 
  . We only pop from a heap when the top element's count in the hash map reaches 0. 
  . You must run the Janitor (while loop) before you PEEK at a heap top to make a decision.

. ADD_TO_WINDOW(x): 
    . If Best is under capacity, add x to Best and update sum/size. 
    . If Best is full, clean the Best top and compare x to the current maximum. 
      . If x is smaller than the max, add x to Best and move the old max to the Bench. 
      . If x is larger, just add it to the Bench.

. REMOVE_FROM_WINDOW(x): 
    . Check the counters to see if x was logically in the Best or Bench bucket. 
    . If x was in Best, decrement the sum/size and immediately fill the hole from the Bench.
    . If x was in Bench, just decrement the counter; no refill is needed.

. THE i-LOOP LOGIC: 
  . The total cost for index i is nums[0] + nums[i] + best_sum. 
  . As i moves to i+1, the pool changes. 
  . Remove nums[i+1] because it is becoming the mandatory start of the next subarray. 
  . Add nums[i + dist + 1] because it is the new element entering the reach of the distance window.
'''
from heapq import *
from collections import defaultdict

class Solution:
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        n = len(nums)

        # We need to pick k-2 more elements from the window
        needed = k - 2
        
        # Initialize your state
        # best represents a max heap of minimum k - 2 elements and the rest is in the bench
        self.best_h, self.bench_h = [], []
        self.best_cnt, self.bench_cnt = defaultdict(int), defaultdict(int)
        self.best_size, self.best_sum = 0, 0
        
        # 1. INITIAL WINDOW: For i = 1, the candidates are indices [2, 1 + dist]
        # We fill the heaps with this initial range
        for j in range(2, min(n, 2 + dist)):
            self.add_to_window(nums[j], needed)
            
        ans = float('inf')
        
        # 2. ITERATE i from 1 up to the limit
        # The limit is n - (k-1) because we need room for k-1 subarrays
        for i in range(1, n - k + 2):
            # Update global minimum: nums[0] + mandatory second + best of rest
            ans = min(ans, nums[0] + nums[i] + self.best_sum)
            
            # 3. SLIDE THE WINDOW for the next i
            # Leaving: nums[i+1] (the next mandatory i)
            if i + 1 < n:
                self.remove_from_window(nums[i + 1], needed)
            
            # Entering: nums[i + dist + 1]
            if i + dist + 1 < n:
                self.add_to_window(nums[i + dist + 1], needed)
                
        return ans

    # main
    def add_to_window(self, x, needed):
        if self.best_size < needed:
            # If the best bucket hasn't reached capacity K yet
            self._add_to_best(x)
        else:
            # Best bucket is full. We must determine if x is smaller than the current maximum in 'best'
            self._clean_best()  # Ensure we are comparing x to a valid current element
            
            current_max_best = -self.best_h[0]
            
            if x < current_max_best:
                # x is a better candidate for the 'best' set.
                # 1. Add x to best
                self._add_to_best(x)
                
                # 2. Remove the element that was previously the maximum in 'best'
                # Since we just added x, the heap top might still be current_max_best or x.
                # heappop will correctly give us the largest of the now K+1 elements.
                removed_val = -heappop(self.best_h)
                self.best_cnt[removed_val] -= 1
                self.best_sum -= removed_val
                self.best_size -= 1
                
                # 3. Move that removed element to the bench
                self._add_to_bench(removed_val)
            else:
                # x is not smaller than our current maximum in 'best'
                self._add_to_bench(x)
    
    def remove_from_window(self, x, needed):
        # 1. Determine which bucket x logically belongs to
        if self.best_cnt[x] > 0:
            # x was in the 'best' set
            self.best_cnt[x] -= 1
            self.best_sum -= x
            self.best_size -= 1
        else:
            # x was on the 'bench'
            self.bench_cnt[x] -= 1

        # 2. If removing x created a hole in 'best', we must fill it from 'bench'
        if self.best_size < needed:
            self._clean_bench() # Ensure we pull a valid element
            
            if self.bench_h:
                # Take the smallest element from the bench
                new_best_val = heappop(self.bench_h)
                self.bench_cnt[new_best_val] -= 1
                
                # Move it into the 'best' set
                self._add_to_best(new_best_val)

    # Helpers
    def _clean_best(self):
        # Remove elements that are no longer in the window but are at the top of the heap
        while self.best_h and self.best_cnt[-self.best_h[0]] == 0:
            heappop(self.best_h)
    
    def _clean_bench(self):
        # Remove elements that are no longer in the window but are at the top of the bench
        while self.bench_h and self.bench_cnt[self.bench_h[0]] == 0:
            heappop(self.bench_h)

    def _add_to_best(self, x):
        heappush(self.best_h, -x)
        self.best_cnt[x] += 1
        self.best_sum += x
        self.best_size += 1

    def _add_to_bench(self, x):
        heappush(self.bench_h, x)
        self.bench_cnt[x] += 1
