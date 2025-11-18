'''
Problem Statement:

. Given an array of N elements, the goal is to find the Majority Element. This is defined as the element that appears more than floor(N/2) times.
    - Example:Array A = [3, 3, 4, 2, 4, 4, 2, 4, 4]. N=9. floor(N/2) = 4.The number 4 appears 5 times, which is > 4. Thus, 4 is the majority element.

Approaches:

1. A simple, naive way to solve this is to use a hash map (or dictionary) to store the count of every element. This works, but requires O(N) extra space, which can be inefficient for very large arrays.
2. A more efficient way to solve this is to use the Boyer-Moore Majority Voting Algorithm. This algorithm works in O(N) time and O(1) space.

Intuition: 

. The core intuition is based on the idea of mutual destruction or pairing.
. Imagine the majority element has its own army, and all other elements (the minorities) form a single opposing army. Because the majority element appears more than half the time, its army is guaranteed to be larger than all the other armies combined.
. The algorithm works by having every instance of a minority element cancel out one instance of the majority element (or any other element).
. Every time a minority element is seen, it destroys one count of the current leader.
. Since the majority element is guaranteed to have more occurrences than all other elements combined, it is mathematically impossible for its count to be completely wiped out by the end of the process. The last remaining candidate MUST be the majority element (if one exists).
'''
from collections import Counter, defaultdict
from typing import Any, Dict

# Finding elements > floor(N/2) times
def get_majority_element(arr):
    # --- PASS 1: Finding the Candidate (Your Code) ---
    candidate = None
    count = 0 

    for num in arr:
        if count == 0:
            # New campaign: set current element as candidate
            candidate = num
            count = 1  # Start count at 1 when setting a new candidate
        elif candidate == num:
            # Support: same element, increment count
            count += 1
        else:
            # Cancellation: mutual cancel out
            count -= 1

    # Handle the empty array case explicitly
    if candidate is None:
        return None 

    # --- PASS 2: Verification ---
    # Check if the found candidate truly appears more than N/2 times as we dont know if the candidate is the majority element
    
    # Calculate the actual count of the candidate
    actual_count = 0
    for num in arr:
        if num == candidate:
            actual_count += 1
    
    # Check the majority condition
    N = len(arr)
    if actual_count > N // 2:
        return candidate
    else:
        # No true majority element exists
        return None

'''
Intuition: 

1. The Core Principle(k-1 is the Magic Number):
. In the original Boyer-Moore algorithm (k=2), we were looking for an element M that appeared > floor(N/2) times. We used one candidate slot.
- The key insight: If an element M truly appears more than floor(N/2) times, its count will be greater than all the other elements combined. 
- This means that M's "army" is strong enough to withstand being cancelled out by all its opponents.
- In the generalized case, we look for elements that appear more than floor(N/k) times.
- Constraint: There can be at most k-1 elements that appear more than floor(N/k) times. If there were k or more, then the total count of these would exceed N, which is impossible.
- Therefore, we only need to keep track of up to k-1 potential candidates.
- Rule: To find elements that appear more than floor(N/k) times, we need k-1 candidate/count pairs.

2. The Cancellation Mechanism ⚔️

- In the standard case when k=2:
    - An opponent cancels out one vote of the current candidate.
- In the generalized case (where we track k-1 candidates), the cancellation rule is extended:
    - When an element x is encountered that is not one of the current k-1 candidates, it indicates a "minority" element.
    - This instance of x is used to cancel one vote from each currently tracked candidate.
- In other words:
    - One instance of a minority element cancels out one vote from each of the up to k-1 leading candidates.
- Why does this work?
    - For example, if k=3, we track two candidates, say C1 and C2. The true frequent elements are M1 and M2.
    - When a minority element x appears, it cancels one vote each from C1 and C2.
    - If M1 and M2 both have counts larger than floor(N/3), their combined strength is still greater than that of all the minority elements combined.
    - Even though M1 and M2 may lose votes faster than they would in the simple k=2 case, their initially large counts ensure that they will typically remain among the k-1 candidates left standing at the end.
'''

# Generalized version of the algorithm to find elements > floor(N/k) times
def get_majority_element_generalized(arr, k):
    """
    Finds all elements that appear more than floor(N / k) times in the array.
    This is the generalized Boyer-Moore Majority Vote algorithm, using k-1 candidates.

    Args:
        arr: The input list of elements.
        k: The threshold divisor (e.g., k=3 finds elements > N/3 times).
    
    Returns:
        A list of elements that meet the frequency threshold.
    """
    N = len(arr)
    if N == 0 or k <= 1:
        return []

    # The algorithm requires k-1 candidate slots.
    capacity = k - 1
    
    # Stores the current candidates and their counts from the cancellation process.
    # We use a standard dictionary (dict) to represent the k-1 slots.
    candidate_counts: Dict[Any, int] = {}
    
    # --- PASS 1: The Voting and Cancellation Phase (O(N) Time, O(k) Space) ---
    for num in arr:
        # Check if the current element is one of the active candidates
        if num in candidate_counts:
            # Case 1: Match - Increment the count for the supporting element
            candidate_counts[num] += 1
            
        # Check if we have an open slot
        elif len(candidate_counts) < capacity:
            # Case 2: New Slot - Set the current element as a new candidate
            candidate_counts[num] = 1
            
        # All slots are full, and the current element is a minority/opponent
        else:
            # Case 3: Cancellation - Decrement the count of ALL active candidates.
            # We must iterate over a copy of the keys to avoid changing the dictionary during iteration.
            
            candidates_to_remove = []
            
            for candidate in list(candidate_counts.keys()): # Iterate over keys copy
                candidate_counts[candidate] -= 1
                
                # Check for candidates whose count dropped to zero.
                if candidate_counts[candidate] == 0:
                    candidates_to_remove.append(candidate)
            
            # Remove candidates whose count reached zero outside of the primary iteration.
            for candidate in candidates_to_remove:
                del candidate_counts[candidate]


    # --- PASS 2: Verification Phase (O(N) Time, O(k) Space) ---
    # The first pass only provides potential candidates; we must verify their actual frequency.
    
    # Threshold check: strictly greater than floor(N/k)
    threshold = N // k 
    result = []
    
    # 1. Recalculate the true count of the surviving candidates
    # We use a standard dictionary for O(k) space count, or a list/tuple if k is small.
    # Since we only check the survivors, we initialize a map of actual counts.
    final_counts: Dict[Any, int] = {c: 0 for c in candidate_counts.keys()}
    
    # Iterate through the original array again to get the true counts of the survivors
    for num in arr:
        if num in final_counts:
            final_counts[num] += 1
            
    # 2. Check the condition
    for candidate, actual_count in final_counts.items():
        if actual_count > threshold:
            result.append(candidate)
            
    return result


if __name__ == "__main__":
    # test cases
    test_cases = [
        [3, 3, 4, 2, 4, 4, 2, 4, 4],
        [1, 1, 1, 1, 1],
        [2, 2, 1, 1, 2],
        [1, 2, 3, 4, 4, 4, 4],
        [1, 1, 2, 2, 3, 3, 3],
        [6],
        [1,2,1,2,1]
    ]

    for test in test_cases:
        print(f"Test case: {test}")
        expected = Counter(test).most_common(1)[0][0]
        print(f"Majority element: {get_majority_element(test)}, Expected: {expected}")
        assert get_majority_element(test) == expected, f"Expected {expected}, got {get_majority_element(test)}"
        print("-" * 80)