'''
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).


Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.


Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-106 <= nums1[i], nums2[i] <= 106

Insights:
. easy to do in linear time just use the merge algorithm of mergesort and then find the middle

'''
from typing import List


class Solution:
    def findMedianSortedArrays_merge_On(self, nums1: List[int], nums2: List[int]) -> float:
        m = len(nums1)
        n = len(nums2)
        total = m + n

        res = []
        i = 0
        j = 0

        # merge
        while i < m and j < n:
            if nums1[i] <= nums2[j]:
                res.append(nums1[i])
                i += 1
            else:
                res.append(nums2[j])
                j += 1

        if i < m:
            res.extend(nums1[i:])
        elif j < n:
            res.extend(nums2[j:])

        if total % 2 == 1:
            return res[total // 2]
        else:
            return (res[total // 2] + res[(total // 2) - 1]) / 2

    #optinmal binary search solution
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # ensuring that A is the smaller of the two because we are going to do binary search on the smaller array
        if len(nums1) < len(nums2):
            A, B = nums1, nums2
        else:
            A, B = nums2, nums1

        total = len(A) + len(B)
        half = total // 2

        l = 0
        r = len(A) - 1

        '''
        try to find the boundary point in A such that:
            . all elements before that point are in the left boundary and all elements in B's part also in left boundary

        once we have the left boundary of the "merged" array then its easy to find the median
        '''
        while True:
            m = (l + r) // 2

            Aleft = A[m] if m >= 0 else float("-inf")
            Aright = A[m + 1] if m + 1 < len(A) else float("inf")
            Bleft = B[half - m - 2] if half - m - 2 >= 0 else float("-inf")
            Bright = B[half - m - 1] if half - m - 1 < len(B) else float("inf")

            # found the left partition
            if Aleft <= Bright and Bleft <= Aright:
                if total % 2 == 1:
                    # return only one value which is immediately to the right of the left elements
                    return min(Aright, Bright)
                else:
                    # need to return the middle two (rightmost of left boundary, and leftmost of right boundary)
                    max_left_boundary = max(Aleft, Bleft)
                    min_right_boundary = min(Aright, Bright)
                    return (max_left_boundary + min_right_boundary) / 2
            elif Aleft > Bright:
                # element at A[m] shouldnt be part of left partition, so we need to move right pointer of A to m-1 so that the m changes to before
                r = m - 1
            else:
                # element at Bleft shouldnt be part of left partition, so we need to move left pointer of A to m+1 so that Bleft will move backwards since more elements from A are included
                l = m + 1

