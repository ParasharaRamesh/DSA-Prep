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

    '''
    Optimal O(log(min(m,n))) binary search solution:
    
    KEY INSIGHTS TO SOLVE THIS PROBLEM:
    ====================================
    
    1. BRUTE FORCE OBSERVATION:
       - Easy to do in O(m+n) time: just use merge algorithm from mergesort, then find middle element(s)
       - But we need O(log(m+n)) which screams "binary search"
    
    2. MEDIAN PROPERTY:
       - The median divides a sorted array into two equal (or nearly equal) halves
       - For merged array: LEFT partition has (m+n)//2 elements, RIGHT has the rest
       - All elements in LEFT ≤ all elements in RIGHT
    
    3. PARTITION INSIGHT:
       - Instead of merging arrays, we can PARTITION both arrays such that:
         * Combined LEFT partitions have exactly (m+n)//2 elements
         * max(LEFT partitions) ≤ min(RIGHT partitions)
       - If we find such a partition, we've found the median!
    
    4. BINARY SEARCH STRATEGY:
       - We don't know where to partition, so try different partition points
       - Do binary search on the SMALLER array (for efficiency)
       - If we partition A at index m, we MUST partition B at index (half - m - 2)
         to ensure left partition has exactly 'half' elements total
    
    5. VALIDATION CONDITION:
       - For a valid partition, we need 4 boundary elements:
         * Aleft (rightmost of A's left partition)
         * Aright (leftmost of A's right partition)
         * Bleft (rightmost of B's left partition)
         * Bright (leftmost of B's right partition)
       - Valid partition requires: Aleft ≤ Bright AND Bleft ≤ Aright
       - This ensures all left elements ≤ all right elements
    
    6. BINARY SEARCH ADJUSTMENT:
       - If Aleft > Bright: A's partition is too far right, move it left (r = m-1)
       - If Bleft > Aright: A's partition is too far left, move it right (l = m+1)
    
    Example walkthrough:
    A = [1, 3, 8, 9, 15]
    B = [7, 11, 18, 19, 21, 25]
    
    Total = 11, half = 5 (need 5 elements in left partition)
    
    Try m=2 (middle of A):
    A: [1, 3, | 8, 9, 15]  (Aleft=3, Aright=8)
    B: [7, 11, 18, | 19, 21, 25]  (Bleft=18, Bright=19)
    Left partition: [1,3,8] from A + [7,11] from B = 5 elements ✓
    Check: Aleft(3) ≤ Bright(19)? YES, Bleft(18) ≤ Aright(8)? NO!
    → Bleft > Aright means A's partition too far left, move right (l = m+1)
    
    Try m=3:
    A: [1, 3, 8, | 9, 15]  (Aleft=8, Aright=9)
    B: [7, | 11, 18, 19, 21, 25]  (Bleft=7, Bright=11)
    Left partition: [1,3,8,9] from A + [7] from B = 5 elements ✓
    Check: Aleft(8) ≤ Bright(11)? YES, Bleft(7) ≤ Aright(9)? YES!
    → Valid partition found!
    Median = min(Aright, Bright) = min(9, 11) = 9 (odd total)
    '''
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        
        '''
        STEP 1: Ensure A is the smaller array
        ======================================
        We perform binary search on A, so we want A to be smaller for efficiency.
        Time complexity: O(log(min(m,n))) instead of O(log(max(m,n)))
        
        Example:
        nums1 = [1, 2, 3, 4, 5], nums2 = [6, 7]
        After swap: A = [6, 7], B = [1, 2, 3, 4, 5]
        This reduces binary search iterations from log(5) to log(2)
        '''
        if len(nums1) < len(nums2):
            A, B = nums1, nums2
        else:
            A, B = nums2, nums1

        '''
        STEP 2: Calculate partition size
        =================================
        'total' = combined length of both arrays
        'half' = number of elements that should be in the LEFT partition
        
        For odd total (e.g., 7): half = 3, so left has 3, right has 4
        For even total (e.g., 8): half = 4, so left has 4, right has 4
        
        Example:
        A = [1, 3], B = [2, 4, 5]
        total = 5, half = 2
        We need 2 elements in left partition of merged array [1, 2, | 3, 4, 5]
        '''
        total = len(A) + len(B)
        half = total // 2

        '''
        STEP 3: Initialize binary search pointers
        ==========================================
        l, r define the search space in array A
        We're searching for the correct partition index 'm' in A
        
        Note: We use indices 0 to len(A)-1 because 'm' represents the
        LAST index included in A's left partition (not the partition point itself)
        
        Example:
        A = [1, 3, 8, 9]
        l = 0, r = 3
        If m = 1, it means A's left partition is [1, 3] (indices 0 to 1)
        '''
        l = 0
        r = len(A) - 1

        '''
        STEP 4: Binary search for valid partition
        ==========================================
        We use 'while True' because we're guaranteed to find a valid partition
        (the problem guarantees valid input)
        '''
        while True:
            '''
            Calculate middle index of current search space
            This is our candidate partition point in array A
            
            Example:
            l = 0, r = 3
            m = (0 + 3) // 2 = 1
            This means we're trying: A's left partition = A[0:m+1] = A[0:2]
            '''
            m = (l + r) // 2

            '''
            STEP 5: Determine the 4 boundary elements
            ==========================================
            
            Aleft: Last element in A's left partition (A[m])
            Aright: First element in A's right partition (A[m+1])
            Bleft: Last element in B's left partition
            Bright: First element in B's right partition
            
            WHY "half - m - 2" for Bleft index?
            -----------------------------------
            - A's left partition has (m + 1) elements (indices 0 to m)
            - Total left partition needs 'half' elements
            - So B's left partition needs: half - (m + 1) = half - m - 1 elements
            - Last index in B's left partition: (half - m - 1) - 1 = half - m - 2
            
            Example:
            A = [1, 3, 8], B = [2, 4, 5, 6], total = 7, half = 3
            If m = 1 (A's left = [1, 3], 2 elements):
            - B's left needs: 3 - 2 = 1 element
            - B's left partition: B[0:1] = [2]
            - Bleft index: 0 = half(3) - m(1) - 2
            - Bright index: 1 = half(3) - m(1) - 1
            
            WHY use infinity for out-of-bounds?
            -----------------------------------
            - If m = -1 (A contributes nothing to left), Aleft = -∞ (never violates Aleft ≤ Bright)
            - If m+1 = len(A) (A contributes everything to left), Aright = +∞ (never violates Bleft ≤ Aright)
            - This handles edge cases elegantly without special conditions
            
            Example edge case:
            A = [1, 2], B = [3, 4, 5, 6], m = -1 (A contributes 0 to left)
            Aleft = -∞, Aright = A[0] = 1
            Bleft = B[2] = 5, Bright = B[3] = 6
            Check: -∞ ≤ 6? YES, 5 ≤ 1? NO → adjust search
            '''
            Aleft = A[m] if m >= 0 else float("-inf")
            Aright = A[m + 1] if m + 1 < len(A) else float("inf")
            Bleft = B[half - m - 2] if half - m - 2 >= 0 else float("-inf")
            Bright = B[half - m - 1] if half - m - 1 < len(B) else float("inf")

            '''
            STEP 6: Check if current partition is valid
            ============================================
            
            Valid partition condition: Aleft ≤ Bright AND Bleft ≤ Aright
            
            WHY this condition?
            -------------------
            - Aleft ≤ Bright ensures: max(A's left) ≤ min(B's right)
            - Bleft ≤ Aright ensures: max(B's left) ≤ min(A's right)
            - Together they guarantee: max(all left elements) ≤ min(all right elements)
            - This is the definition of a valid median partition!
            
            Example of VALID partition:
            A = [1, 3, | 8, 9], B = [2, 4, | 5, 6]
            Aleft=3, Aright=8, Bleft=4, Bright=5
            Check: 3 ≤ 5? YES, 4 ≤ 8? YES → VALID!
            Left partition: [1, 2, 3, 4], Right partition: [5, 6, 8, 9]
            
            Example of INVALID partition:
            A = [1, 8, | 9, 10], B = [2, | 3, 4, 5]
            Aleft=8, Aright=9, Bleft=2, Bright=3
            Check: 8 ≤ 3? NO → INVALID (Aleft > Bright)
            '''
            if Aleft <= Bright and Bleft <= Aright:
                '''
                STEP 7a: Calculate median for ODD total length
                ===============================================
                
                For odd total, median is the FIRST element of the right partition
                (the middle element when merged)
                
                WHY min(Aright, Bright)?
                ------------------------
                - Right partition starts with Aright (from A) and Bright (from B)
                - The smaller of these two is the first element of merged right partition
                - This is our median!
                
                Example:
                A = [1, 3], B = [2, 4, 5]
                total = 5 (odd), half = 2
                
                Try m=0:
                A's left = [1] (1 element), B's left needs 1 element
                Aleft=1, Aright=3, Bleft=2, Bright=4
                Check: 1 ≤ 4? YES, 2 ≤ 3? YES → VALID!
                Median = min(Aright, Bright) = min(3, 4) = 3 ✓
                Merged array: [1, 2, | 3, 4, 5] → median is 3 (middle element)
                '''
                if total % 2 == 1:
                    return min(Aright, Bright)
                else:
                    '''
                    STEP 7b: Calculate median for EVEN total length
                    ================================================
                    
                    For even total, median is average of:
                    - Last element of left partition: max(Aleft, Bleft)
                    - First element of right partition: min(Aright, Bright)
                    
                    WHY max(Aleft, Bleft)?
                    ----------------------
                    - Left partition ends with Aleft (from A) and Bleft (from B)
                    - The larger of these is the last element of merged left partition
                    
                    WHY min(Aright, Bright)?
                    ------------------------
                    - Right partition starts with Aright (from A) and Bright (from B)
                    - The smaller of these is the first element of merged right partition
                    
                    Example:
                    A = [1, 2, | 3, 4], B = [5, 6, | 7, 8]
                    total = 8 (even), half = 4
                    Aleft=2, Aright=3, Bleft=6, Bright=7
                    max_left = max(2, 6) = 6
                    min_right = min(3, 7) = 3
                    Wait, 6 > 3, so this partition is invalid!
                    
                    Correct example:
                    A = [1, 3, | 8, 9], B = [2, 4, | 5, 6]
                    total = 8 (even), half = 4
                    Aleft=3, Aright=8, Bleft=4, Bright=5
                    max_left = max(3, 4) = 4
                    min_right = min(8, 5) = 5
                    Median = (4 + 5) / 2 = 4.5 ✓
                    Merged: [1, 2, 3, 4, | 5, 6, 8, 9]
                    '''
                    max_left_boundary = max(Aleft, Bleft)
                    min_right_boundary = min(Aright, Bright)
                    return (max_left_boundary + min_right_boundary) / 2
            
            '''
            STEP 8a: Adjust search space - A's partition too far RIGHT
            ===========================================================
            
            If Aleft > Bright, it means:
            - The last element of A's left partition is GREATER than
              the first element of B's right partition
            - This violates the median property (left ≤ right)
            - We need to DECREASE A's contribution to left partition
            - Move right pointer left: r = m - 1
            
            Example:
            A = [7, 8, | 9, 10], B = [1, | 2, 3, 4]
            Aleft=8, Bright=2
            8 > 2 → A's partition too far right!
            We need fewer elements from A in left partition
            Solution: r = m - 1, so next m will be smaller
            '''
            elif Aleft > Bright:
                r = m - 1
            else:
                '''
                STEP 8b: Adjust search space - A's partition too far LEFT
                ==========================================================
                
                If Bleft > Aright, it means:
                - The last element of B's left partition is GREATER than
                  the first element of A's right partition
                - This violates the median property (left ≤ right)
                - We need to INCREASE A's contribution to left partition
                  (which automatically decreases B's contribution)
                - Move left pointer right: l = m + 1
                
                Example:
                A = [1, | 2, 3, 4], B = [7, 8, 9, | 10]
                Aleft=1, Aright=2, Bleft=9, Bright=10
                9 > 2 → B's contribution to left is too large!
                We need more elements from A in left partition (and fewer from B)
                Solution: l = m + 1, so next m will be larger
                
                WHY does increasing m decrease B's left partition?
                ---------------------------------------------------
                Recall: B's left partition size = half - (m + 1)
                If m increases, (m + 1) increases, so (half - (m + 1)) decreases
                More from A's left means less from B's left, maintaining total = half
                '''
                l = m + 1

