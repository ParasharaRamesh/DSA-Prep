'''
Given an array of integers nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to limit.

 

Example 1:

Input: nums = [8,2,4,7], limit = 4
Output: 2 
Explanation: All subarrays are: 
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4. 
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4. 
Therefore, the size of the longest subarray is 2.
Example 2:

Input: nums = [10,1,2,4,7,2], limit = 5
Output: 4 
Explanation: The subarray [2,4,7,2] is the longest since the maximum absolute diff is |2-7| = 5 <= 5.
Example 3:

Input: nums = [4,2,2,2,4,4,2,2], limit = 0
Output: 3
 
Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 109
0 <= limit <= 109
'''

'''
Thoughts:
. bruteforce would be n^3 soln because n^2 subarrays and n to find min and max
. clearly its a dynamic sliding window kind of problem where we keep growing the subarray as long as it fits the criterion and shrink it when it doesnt
. question is how to update the max and min dynamically 
    - initially I started thinking about using segment trees or something efficient to find the min and max in faster time (say logarithmic time)
    - didnt code it up though because I would have gotten an n^2 logn time which would give TLE

. Solution 1 (using sorted list):
    - sorted list : add, remove is all logn time
    - in the grow phase just keep adding things to the sorted list as long as the max_val - min_val <= limit and move the 'r' pointer until that criterion breaks
    - in the shrink phase we basically have to keep removing the element at the 'l' pointer and then move that forward until the reverse criterion holds. i.e. max_val - min_val >= limit
    - keep track of the longest window so far and return that 

. Solution 2 (using min heap and max heap)
    - same idea as sliding window, just that we use a min heap and max heap to answer the question of what is the min and max in the range [l,r]
    - in the grow phase just add the element to both the min heap and max heap and keep growing until the constraint is valid
    - in the shrink phase , we first move the l pointer by 1 and we know that we need to keep shrinking until max_val - min_val < limit and stop the moment it is >= limit
        - in this process keep removing things from both heaps in case any element doesnt fall in the range [l,r] (basically anything which is [0, l-1] as in the shrink phase only l could have moved)
        - then use the heaps to answer that question again
    - keep track of the longest window so far and return that 

. Solution 3 (using 2 deques - monotonic queue):
    - initially you might think that we can just have a max and min variable which we can use to keep track of things as we keep going through the list 
    - however once we modify the max or min values as we move the r pointer , we dont know how things change the moment we move the l pointer
    - which means we need to have a list of next possible max values and another list of next possible min values incase the l pointer moves forward
    - this is exactly why we have 2 deques one to keep track of min values and another to keep track of max values
    - here we use the monotonic property :
        - basically at every index what is the next min or next max (which is exactly what we want) so that once something is removed from the min or max queues we can just take the next min/max and do the logic
        - for maintain a list of min values we maintain a monotonically increasing list and analogously a montonically decreasing list for max values
'''

from collections import deque
from typing import List
from sortedcontainers import SortedList
from heapq import *

class Solution:
    def longestSubarray_sortedlist(self, nums: List[int], limit: int) -> int:
        if len(nums) == 1:
            return 1

        l, r = 0, 0
        best = 1
        sl = SortedList()

        while l <= r and r < len(nums):
            # grow
            while l <= r and r < len(nums):
                # add the rth one
                sl.add(nums[r])
                min_val, max_val = sl[0], sl[-1]
                if abs(max_val - min_val) <= limit:
                    best = max(best, r - l + 1)
                    r += 1
                else:
                    r += 1
                    break

            # shrink
            while l <= r and r < len(nums):
                min_val, max_val = sl[0], sl[-1]
                if abs(max_val - min_val) > limit:
                    sl.remove(nums[l])
                    l += 1
                else:
                    break

        return best

    def longestSubarray_heap(self, nums: List[int], limit: int) -> int:
        if len(nums) == 1:
            return 1

        # keep track of a maxheap and minheap along with indicies so that we can easily answer the query
        min_heap = []
        max_heap = []

        best = 0
        l, r = 0, -1

        while r < len(nums):
            # just so that adding the rth element becomes easier next grow phase
            r += 1

            # grow as much as possible while adhering to constraint
            while r < len(nums):
                # add it to both along with indices
                heappush(min_heap, (nums[r], r))
                heappush(max_heap, (-nums[r], r))

                # check if the limit condition holds
                max_val = -max_heap[0][0]
                min_val = min_heap[0][0]

                if max_val - min_val <= limit:
                    best = max(best, r - l + 1)
                    r += 1
                else:
                    # the rth element now violates this constraint
                    break

            # shrink as much as possible while violating constraint
            while l <= r and r < len(nums):
                # we plan to shrink
                l += 1

                # get that max which is in range [l,r]
                while max_heap and not (l <= max_heap[0][1] <= r):
                    heappop(max_heap)

                if not max_heap:
                    break

                max_val = -max_heap[0][0]

                # get that min which is in range [l,r]
                while min_heap and not (l <= min_heap[0][1] <= r):
                    heappop(min_heap)

                if not min_heap:
                    break

                min_val = min_heap[0][0]

                # if the constraint is satisfied again break
                if max_val - min_val <= limit:
                    break

        return best

    # using the idea of monotonic queues
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        decQ = deque() 
        incQ = deque() 
        ans = 0
        left = 0

        for right, num in enumerate(nums):
            while decQ and num > decQ[-1]:
                decQ.pop()
            decQ.append(num)

            while incQ and num < incQ[-1]:
                incQ.pop()
            incQ.append(num)

            while decQ[0] - incQ[0] > limit:
                if decQ[0] == nums[left]:
                    decQ.popleft()

                if incQ[0] == nums[left]:
                    incQ.popleft()

                left += 1

            ans = max(ans, right - left + 1)

        return ans

if __name__ == "__main__":
    s = Solution()

    nums = [10,1,2,4,7,2]
    limit = 5
    ans = s.longestSubarray_heap(nums, limit)
    expected = 4
    assert ans == expected, f"{nums=} {limit=} {ans=} instead of {expected=}"

    nums = [4,2,2,2,4,4,2,2]
    limit = 0
    ans = s.longestSubarray_heap(nums, limit)
    expected = 3
    assert ans == expected, f"{nums=} {limit=} {ans=} instead of {expected=}"

    nums = [8,2,4,7]
    limit = 4
    ans = s.longestSubarray_heap(nums, limit)
    expected = 2
    assert ans == expected, f"{nums=} {limit=} {ans=} instead of {expected=}"