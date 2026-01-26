"""
GENERAL PATTERNS FOR O(1) SPACE ARRAY MANIPULATION
==================================================
These patterns are used when you need to track information about 
the presence or frequency of numbers in an array without 
allocating extra memory (like a Set or Dictionary).
"""

# ---------------------------------------------------------
# IDEA 1: NEGATIVE MARKING (The "State" Flag)
# ---------------------------------------------------------
'''
CONCEPT:
Use the SIGN of the number at index `i` to represent a boolean state 
(e.g., "Has the number i+1 been seen?").

PREREQUISITE: 
The array must contain only positive numbers (or you must clean it 
first). 

LOGIC:
To mark the number 'x' as "seen":
1. Go to index abs(x) - 1.
2. If the value there is positive, multiply it by -1.
3. To read the original value later, always use abs(nums[i]).
'''

def pattern_negative_marking(nums):
    # Example: Check which numbers from 1 to N are present
    n = len(nums)
    
    # 1. Mark presence
    for i in range(n):
        val = abs(nums[i])
        if 1 <= val <= n:
            idx = val - 1
            if nums[idx] > 0:
                nums[idx] *= -1
    
    # 2. Identify missing (the first index that is still positive)
    for i in range(n):
        if nums[i] > 0:
            return i + 1
    return n + 1


# ---------------------------------------------------------
# IDEA 2: MODULO ENCODING (The "Two-in-One" Storage)
# ---------------------------------------------------------
'''
CONCEPT:
Store two different values in a single memory slot using the formula: 
    ModifiedValue = (Frequency * K) + OriginalValue
    
Where K is any constant larger than any possible OriginalValue 
(usually the length of the array, N).

LOGIC:
- To get OriginalValue:  ModifiedValue % K
- To get Frequency:      ModifiedValue // K
'''

def pattern_modulo_encoding(nums):
    n = len(nums)
    k = n + 1 # Our constant
    
    # 1. Encode: Let's count frequencies of numbers
    for i in range(n):
        # We want to increment the 'frequency' part of the value at index `nums[i]`
        # We use % k to get the original value even after it's been modified
        val = nums[i] % k
        if val < n:
            nums[val] += k 
            
    # 2. Decode
    for i in range(n):
        original = nums[i] % k
        frequency = nums[i] // k
        print(f"Number {i} appeared {frequency} times. If frequency is zero then it means that it was never marked!")


# ---------------------------------------------------------
# IDEA 3: CYCLE SORT (The "Right Place, Right Time")
# ---------------------------------------------------------
'''
CONCEPT:
If the problem involves a range of numbers [1, n] or [0, n], we can 
sort the array in O(n) time by repeatedly swapping each number 
to its "target index."

LOGIC:
For each index `i`:
While nums[i] is in the valid range AND nums[i] != nums[target_index]:
    Swap nums[i] with nums[target_index]
    
This places at least one number in its correct spot per swap.

Why Cycle Sort is O(n) and not O(nlogn)?

* Cycle Sort "cheats" by using the value of the number as an index to know exactly where each element belongs (range [0, n]).
    * It is a place based sorting algorithm and not a comparison based sorting algorithm.
    * It is not a comparison based sorting algorithm because it does not compare the elements to sort them.
* The "Swap" Logic:
    * Uses a while loop inside a for loop, which looks like O(n^2) but is actually O(n).
    * Correct Positions: Every successful swap puts at least one number into its final, correct destination.
    * Finite Swaps: An array of size n can only have n numbers in their correct positions. Once a number is in its correct place, it is never moved again.
    * The Total Count: Swaps at one index "pre-sort" the rest of the array. No element is swapped more than once into its final position
'''
def pattern_cycle_sort(nums):
    n = len(nums)
    i = 0
    while i < n:
        # The value 'x' should ideally live at index 'x' (or x-1)
        target_idx = nums[i] 
        
        if 0 <= target_idx < n and nums[i] != nums[target_idx]:
            # Swap current element to its correct home
            nums[i], nums[target_idx] = nums[target_idx], nums[i]
            # Note: We do NOT increment i here because the new 
            # nums[i] might also need to be swapped!
        else:
            i += 1
            
    return nums

# ---------------------------------------------------------
# SUMMARY FOR NOTES
# ---------------------------------------------------------
# 1. Negative Marking: Best for simple "Exists/Doesn't Exist" checks.
# 2. Modulo Encoding: Best when you need to keep the original data 
#    AND store a count/frequency simultaneously.
# 3. Cycle Sort: Best when you need to physically reorder the array 
#    to find missing/duplicate elements.
# 4. Another way would be to use the idea of bitmasks to encode presence ( look at leetcode/ sudoku solver for this idea)