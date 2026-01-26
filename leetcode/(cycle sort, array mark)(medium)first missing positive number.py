 '''
Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.

You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

 

Example 1:

Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.
Example 2:

Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.
Example 3:

Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.
 

Constraints:

1 <= nums.length <= 105
-2^31 <= nums[i] <= 2^31 - 1
'''

'''
Refer to algorithms/marking an array to preserve space.py for more details on this patten
APPROACH 1: CYCLE SORT (Modified)
---------------------------------
1. Filter out non-positive numbers as they don't affect the answer.
2. The answer must be in the range [1, len(nums) + 1]. Any number outside this range can be ignored.
3. We try to place each number x at its correct index (x-1). 
   - Example: Place 3 at index 2.
4. If a number is already in its correct position, we mark it as "visited" by negating it.
5. In the end, the first index `i` that does not contain the value `-(i+1)` corresponds to the missing number `i+1`.

APPROACH 2: IN-PLACE HASHING (MODULO ARITHMETIC)
------------------------------------------------
1. We append 0 to handle 1-based indexing easier (making array size n+1). 
   The answer is in range [1, n].
2. CLEANUP: Turn invalid numbers (negative or >= n) into 0. 0 is used as a placeholder for "empty/invalid".
3. MARKING (The Trick): 
   - We iterate through the array. For every number `x`, we want to mark the index `x` as "visited".
   - Instead of using a boolean array (O(N) space), we modify the number at `nums[x]`.
   - We add `n` to `nums[x]`. 
   - To retrieve the original number at any index `i` during this process, we use `nums[i] % n`.
   - To check if an index `i` was visited, we check if `nums[i] // n > 0`.
4. RESULT: The first index `i` where `nums[i] // n == 0` is the missing number.
'''
 

class Solution:
    def firstMissingPositive_cycle_sort(self, nums: List[int]) -> int:
        # Step 1: Filter out non-positive numbers and remove duplicates
        # We only care about positive integers.
        nums = list(set(filter(lambda num: num > 0, nums)))

        # Step 2: Handle trivial case
        # If no positive numbers exist, the first missing positive is 1.
        if not nums:
            return 1

        # Step 3: Optimization check
        # If the smallest positive number is > 1, then 1 is definitely missing.
        min_num = min(nums)
        if min_num > 1:
            return 1

        # The missing number must be in the range [1, len(nums) + 1]
        max_poss = len(nums) + 1

        # Step 4: Filter out numbers that are too large to be the answer
        # This reduces the search space to only potentially valid candidates.
        nums = list(filter(lambda num: 1 <= num <= max_poss, nums))

        # Step 5: Modified Cycle Sort
        # We repeatedly swap elements to their correct positions (val 3 goes to index 2).
        # We use negative marking to indicate a position is correctly filled.
        while True:
            all_neg = True

            for i in range(len(nums)):
                # If the number at this position is already marked (negative), skip it.
                if nums[i] < 0:
                    continue

                all_neg = False
                
                # The target index for value nums[i] is nums[i] - 1 (0-based indexing)
                j = nums[i] - 1

                # If the target index is out of bounds, we can't place it.
                # Mark current position as visited/processed (negative) and continue.
                if j >= len(nums):
                    nums[i] *= -1
                    continue
                
                # Swap the number to its correct position
                nums[i], nums[j] = nums[j], nums[i]

                # Mark the correct position `j` as filled (negative)
                # indicating that the number `j+1` is present in the array.
                nums[j] *= -1

            # If all numbers are marked negative, we are done sorting/placing.
            if all_neg:
                # Step 6: Find the first missing number
                # Scan the array. The first index `i` that does not hold the value `-(i+1)`
                # means the number `i+1` is missing.
                i = 0
                while i < len(nums) and i + 1 == -nums[i]:
                    i += 1

                return i + 1   
 
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        
        Uses the "Modify Array in-place" technique with Modulo Arithmetic.
        This effectively lets us store two values at one index:
        1. The original number (accessed via % n)
        2. The frequency count (accessed via // n)
        """
        # Append 0 to make the array size n+1. 
        # This helps in handling the number 'n' itself within the array bounds.
        # so that the length is n + 1
        nums.append(0)
        n = len(nums)

        # Step 1: Cleanup
        # Remove invalid numbers (negatives or numbers > n). 
        # We replace them with 0, which signifies "empty".
        for i in range(len(nums)): #delete those useless elements
            if nums[i] < 0 or nums[i] >= n:
                nums[i] = 0

        # Step 2: Mark Frequencies
        # Iterate through the array. For every number `val` we encounter:
        # We go to index `val` and add `n` to it.
        # `nums[i] % n` always gives us the original value at this index, allowing us to traverse correctly even after modification.
        for i in range(len(nums)): #use the index as the hash to record the frequency of each number
            val = nums[i] % n
            # We add `n` to the index `val`. 
            # Later, `nums[val] // n` will tell us how many times `n` was added (frequency of `val`).
            nums[val] += n
        
        # Step 3: Find Missing
        # Iterate starting from 1. 
        # If nums[i] // n == 0, it means we NEVER visited index `i`, 
        # so the number `i` was never present in the original array.
        for i in range(1, len(nums)):
            if nums[i] // n == 0:
                return i
        
        return n