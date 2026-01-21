'''
You are given a 0-indexed integer array nums and a positive integer k.

You can apply the following operation on the array any number of times:

Choose any subarray of size k from the array and decrease all its elements by 1.
Return true if you can make all the array elements equal to 0, or false otherwise.

A subarray is a contiguous non-empty part of an array.

 

Example 1:

Input: nums = [2,2,3,1,1,0], k = 3
Output: true
Explanation: We can do the following operations:
- Choose the subarray [2,2,3]. The resulting array will be nums = [1,1,2,1,1,0].
- Choose the subarray [2,1,1]. The resulting array will be nums = [1,1,1,0,0,0].
- Choose the subarray [1,1,1]. The resulting array will be nums = [0,0,0,0,0,0].
Example 2:

Input: nums = [1,3,1,1], k = 2
Output: false
Explanation: It is not possible to make all the array elements equal to 0.
 

Constraints:

1 <= k <= nums.length <= 10^5
0 <= nums[i] <= 10^6
'''
from typing import List

class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        '''
        ALGORITHM: DYNAMIC 1D DIFFERENCE ARRAY (MODEL B)
        -----------------------------------------------
        We track a 'running_adjustment' which is the sum of all previous 
        decrements. At any index i:
        Actual Value = nums[i] + running_adjustment
        
        Because we process left-to-right, if Actual Value > 0, we are FORCED 
        to apply a decrement of that exact magnitude starting at index i.
        '''
        
        n = len(nums)
        
        '''
        EXPIRY SCHEDULE (The Difference Array):
        This array stores the values that will be REMOVED from the 
        running_adjustment when we reach a certain index.
        
        Example: If we subtract 5 from a range starting at i=0 with k=2,
        the range is [0, 1]. At index 2, we must "undo" that -5.
        So, expiry_schedule[2] = -(-5) = +5.
        '''
        expiry_schedule = [0] * n
        
        '''
        RUNNING ADJUSTMENT (Prefix Sum of Changes):
        The total of all active negative changes covering index i.
        
        Example: If we started two operations of -2 and -3,
        running_adjustment = -5.

        In this case, we are doing a rolling version of difference arrays which is why we dont have to maintain the start of the change e.g. expiry_schedule[start] = -val 

        Instead we just keep counting that in the running adjustment and only when the window slides out do we subtract it from the running adjustment.
        '''
        running_adjustment = 0

        for i in range(n):
            '''
            STEP 1: APPLY EXPIRIES
            Update the running adjustment with any "undo" values scheduled 
            for this index.
            
            Example: 
            State: running_adjustment = -5, expiry_schedule[i] = +2
            Calculation: -5 + 2 = -3
            Result: The total active decrement is now only -3.
            '''
            running_adjustment += expiry_schedule[i]
            
            '''
            STEP 2: CALCULATE CURRENT STATE
            Apply the running adjustment to the original value.
            
            Example:
            State: nums[i] = 10, running_adjustment = -3
            Calculation: 10 + (-3) = 7
            Result: actual_val is 7. We still need to reduce this by 7.
            i.e. this 10 was already a part of a window where everything was subtracted by 3 which is why at this point the actual value is 7
            '''
            actual_val = nums[i] + running_adjustment

            '''
            STEP 3: EVALUATE TARGET
            If the value is already 0, no action. If it's negative, 
            it means we over-subtracted.
            
            Example:
            State: actual_val = -2.
            Action: Return False (Impossible to increase a negative to 0).
            '''
            if actual_val == 0:
                continue

            if actual_val < 0:
                return False

            '''
            STEP 4: BOUNDARY CONSTRAINT
            At this point actual_val > 0

            But if no window can start from this point then it is impossible to make the array elements equal to 0
        
            An operation of size k must fit within the array.

            the very last window of size k starts at i = n - k and goes till n - 1
            . Which means that if i + k == n it is valid and only greater than that is invalid
            
            Example: 
            State: n=5, i=4, k=2. 
            Calculation: 4 + 2 = 6. 
            Action: 6 > 5, so Return False (Window of exactly size k cannot start from index 4).
            '''
            if i + k > n:
                return False

            '''
            STEP 5: APPLY NEW CHANGE
            Since actual_val is > 0 we are forced to apply an operation of size actual_val starting at index i to remove it to make it 0
            
            We need to subtract 'actual_val'. This means the change is -actual_val.
            1. Update running_adjustment immediately (L point).
            2. Schedule the inverse change at i + k (R + 1 point).
            
            Example:
            State: actual_val = 7, k = 3
            1. running_adjustment becomes -3 + (-7) = -10.
            2. If i+k < n, expiry_schedule[i+k] = +7.
            '''
            change = -actual_val
            running_adjustment += change
            
            if i + k < n:
                expiry_schedule[i + k] -= change

        '''
        If we reach the end and all forced operations were legal, 
        the array effectively became all zeros.
        '''
        return True