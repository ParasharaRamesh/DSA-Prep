'''
You are given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. The result should also be sorted in ascending order.

An integer a is closer to x than an integer b if:

|a - x| < |b - x|, or
|a - x| == |b - x| and a < b
Example 1:

Input: arr = [2,4,5,8], k = 2, x = 6

Output: [4,5]
Example 2:

Input: arr = [2,3,4], k = 3, x = 1

Output: [2,3,4]
Constraints:

1 <= k <= arr.length <= 10,000.
-10,000 <= arr[i], x <= 10,000
arr is sorted in ascending order.

'''

from bisect import *
from collections import deque

class Solution:
    # my solution sliding window
    def findClosestElements_sliding_window(self, arr: List[int], k: int, x: int) -> List[int]:
        n = len(arr)

        # trivial case where k == len(arr); return arr as is
        if k == n:
            return arr

        # find the index of where x can go using binary search
        ind = bisect_left(arr, x)

        # in case the index is 0 (include [:k]) or len(arr) (answer is [-k:])
        if ind == 0:
            return arr[:k]

        if ind == n:
            return arr[-k:]

        # else you do a sliding window
        l_ind = ind if arr[ind] == x else ind -1 # can start from one index before
        l = max(0, l_ind - k + 1)
        r = min(ind, n-k)

        window = deque(arr[l:l+k])
        window_abs_diff_sum = 0
        for ele in window:
            window_abs_diff_sum += abs(x-ele)

        best_window = window.copy()
        best_window_abs_diff_sum = window_abs_diff_sum
        
        # window of k starting from i: l + 1 => r
        for i in range(l + 1, r + 1):
            # remove the left element in the window            
            remove = window.popleft()
            window_abs_diff_sum -= abs(x - remove)

            # need to add the element at i + k - 1
            add = arr[i + k - 1]
            window.append(add)
            window_abs_diff_sum += abs(x - add)

            # check if best
            if window_abs_diff_sum < best_window_abs_diff_sum:
                best_window_abs_diff_sum = window_abs_diff_sum
                best_window = window.copy()

                # optimization
                if best_window_abs_diff_sum == 0:
                    break
        return list(best_window)

    def findClosestElements_comparator(self, arr: List[int], k: int, x: int) -> List[int]:
        arr.sort(key=lambda num: (abs(num - x), num))
        return sorted(arr[:k])

    '''
    two pointer approach
    Initialize l = 0 and r = n - 1.
    While r - l >= k:
      Compare the distances of arr[l] and arr[r] from x.
      Remove the element that is farther by moving the corresponding pointer inward.
      If distances are equal, prefer the left element (smaller value), so move r inward.
    Return the subarray from index l to r (inclusive).
    '''
    def findClosestElements_two_pointer(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr) - 1
        while r - l >= k:
            if abs(x - arr[l]) <= abs(x - arr[r]):
                r -= 1
            else:
                l += 1

        return arr[l: r + 1]

    '''
    Solution not implemented for this one
    Binary search + growing two pointer:
      - do binary search and find the index
      - start with l = i-1 and r = i and grow outwards
      - pick the array element which has smaller absolute distance and move the pointer outwards
    '''

    '''
    Binary search directly on arr:
      We can binary search directly for the starting index of the k-length window.
      For any starting index m, we compare the distances of arr[m] and arr[m + k] to x. 
      If arr[m + k] is closer, the window should shift right;
      otherwise, it should stay or shift left. This narrows down the optimal starting position.
    '''
    def findClosestElements_binary_search(self, arr: List[int], k: int, x: int) -> List[int]:
        l, r = 0, len(arr) - k
        while l < r:
            m = (l + r) // 2
            if x - arr[m] > arr[m + k] - x:
                l = m + 1
            else:
                r = m
        return arr[l:l + k]
