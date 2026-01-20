'''

NOTES:

. Difference arrays are essentially the "inverse" operation of prefix sums. While prefix sums allow you to query a range sum in O(1), difference arrays allow you to perform range updates in O(1).
. Any range update is easy to implement using difference arrays instead of segment trees for the following reasons:
    1. Simplicity of implementation
    2. O(1) updates and then final O(N) prefix sum to get the final array
    3. If we want offline processing its better to use difference arrays instead of segment trees.
        - offline => batch of updates to perform first and then we get the final state of the array at the very end 
        - online => if we have queries to perform as we are updating. e.g. update -> query -> update -> query -> update -> update -> query

'''
def apply_updates_using_diff_array(original_arr, updates):
    """
    Model A: Transform the array into its difference representation,
    apply updates, and then reconstruct it.
    """
    n = len(original_arr)
    if n == 0: return []

    # 1. Create the difference array from the original data
    # diff[i] = A[i] - A[i-1]
    diff = [0] * n
    diff[0] = original_arr[0]
    for i in range(1, n):
        diff[i] = original_arr[i] - original_arr[i-1]

    # 2. Apply updates in O(1)
    for L, R, v in updates:
        diff[L] += v
        if R + 1 < n:
            diff[R + 1] -= v

    # 3. Restore the original array using prefix sums (Telescoping sum)
    # The first element is already correct, we build the rest
    for i in range(1, n):
        diff[i] = diff[i] + diff[i-1]
    
    return diff


def apply_updates_using_accumulated_change(original_arr, updates):
    """
    Model B: Create a separate 'change log' array. 
    Calculate the total impact of all updates first, then merge.
    """
    n = len(original_arr)
    # change_log[i] tracks the START and END of adjustments
    change_log = [0] * (n + 1)

    # 1. Record changes in O(1)
    for L, R, v in updates:
        change_log[L] += v
        change_log[R + 1] -= v

    # 2. Convert change_log into actual adjustment values using prefix sum
    # and apply them to the original array
    current_running_change = 0
    for i in range(n):
        current_running_change += change_log[i]
        original_arr[i] += current_running_change

    return original_arr

# look at the corporate flight bookings problem on leetcode and its solution here if you want an example