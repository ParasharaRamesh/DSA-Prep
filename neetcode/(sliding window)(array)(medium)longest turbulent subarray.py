'''
You are given an integer array arr, return the length of a maximum size turbulent subarray of arr.

A subarray is turbulent if the comparison sign flips between each adjacent pair of elements in the subarray.

More formally, a subarray [arr[i], arr[i + 1], ..., arr[j]] of arr is said to be turbulent if and only if:

For i <= k < j:
arr[k] > arr[k + 1] when k is odd, and
arr[k] < arr[k + 1] when k is even.
Or, for i <= k < j:
arr[k] > arr[k + 1] when k is even, and
arr[k] < arr[k + 1] when k is odd.
Example 1:

Input: arr = [2,4,3,2,2,5,1,4]

Output: 4
Explanation: The longest turbulent subarray is [2,5,1,4].

Example 2:

Input: arr = [1,1,2]

Output: 2
Constraints:

1 <= arr.length <= 40,000
0 <= arr[i] <= 1,000,000,000

'''
from typing import List

class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        if len(arr) == 1:
            return 1

        longest = 1
        prev = arr[0]
        should_inc = None

        l = 0
        r = 1

        while r < len(arr):
            # if at all the values are the same then keep going until they are not and start l and r from there
            skipped_equal = False
            while r < len(arr) and arr[r - 1] == arr[r]:
                r += 1 
                skipped_equal = True

            if r == len(arr):
                longest = max(longest, 1) # because its all the same suffix
                continue

            if skipped_equal or should_inc == None:
                l = r - 1
                should_inc = False if arr[l] < arr[r] else True
                prev = arr[r]
                r += 1
                longest = max(longest, r - l)
                continue

            # check zigzag
            if (should_inc and prev < arr[r]) or (not should_inc and prev > arr[r]):
                should_inc ^= True
                prev = arr[r]
                r += 1
                longest = max(longest, r - l)
                continue

            l = r - 1
            should_inc = False if arr[l] < arr[r] else True
            prev = arr[r]
            r += 1

        return longest