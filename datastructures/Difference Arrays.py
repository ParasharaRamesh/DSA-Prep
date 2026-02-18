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

def apply_2d_updates(original_matrix, updates):
    """
    Model B (2D): Create a separate 'change log' matrix.
    Calculate the total impact of all updates first, then merge with original matrix.
    
    original_matrix: 2D list of the original values
    updates: list of [r1, c1, r2, c2, val]
    """
    matrix_m = len(original_matrix)
    matrix_n = len(original_matrix[0]) if matrix_m > 0 else 0
    
    # 1. Initialize a difference array with extra padding (M+1 x N+1)
    # This padding handles the boundary for (r2+1) and (c2+1) automatically.
    diff = [[0] * (matrix_n + 1) for _ in range(matrix_m + 1)]

    # 2. Record all updates in O(1) each
    # 4 point update ( refer to notes on why this is correct )
    for r1, c1, r2, c2, val in updates:
        diff[r1][c1] += val
        diff[r1][c2 + 1] -= val
        diff[r2 + 1][c1] -= val
        diff[r2 + 1][c2 + 1] += val

    # 3. Compute the 2D Prefix Sum on the diff matrix to get accumulated changes
    # This is analogous to the 1D accumulated change variant
    accumulated_changes = [[0] * matrix_n for _ in range(matrix_m)]
    
    for r in range(matrix_m):
        for c in range(matrix_n):
            # To find the accumulated change at (r, c), we use the 2D prefix sum formula:
            # Current = Top + Left - TopLeft + Self_Difference
            top = accumulated_changes[r-1][c] if r > 0 else 0
            left = accumulated_changes[r][c-1] if c > 0 else 0
            top_left = accumulated_changes[r-1][c-1] if (r > 0 and c > 0) else 0
            
            accumulated_changes[r][c] = top + left - top_left + diff[r][c]
    
    # 4. Add the accumulated changes to the original matrix (analogous to 1D variant)
    for r in range(matrix_m):
        for c in range(matrix_n):
            original_matrix[r][c] += accumulated_changes[r][c]
            
    return original_matrix