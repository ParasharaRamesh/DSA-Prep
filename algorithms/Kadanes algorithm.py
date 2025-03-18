'''
Basically have a local and global sum

Keep growing the local sum little by little and put that as the global sum!
'''
def kadanesAlgorithm(array):
    globalSum = localSum = array[0]

    for x in array[1:]:
        localSum = max(x, localSum + x)
        globalSum = max(globalSum, localSum)

    return globalSum


def kadanesAlgorithm_sliding_window(nums):
    max_sum = float('-inf')  # Store the maximum sum found
    window_sum = 0  # Current window sum
    left = 0  # Left boundary of the sliding window
    right = 0  # Right boundary of the sliding window

    while right < len(nums):
        window_sum += nums[right]  # Expand window

        # Shrink window if sum is negative
        while window_sum < 0 and left <= right:
            window_sum -= nums[left]  # Remove leftmost element
            left += 1  # Shrink window from the left

        max_sum = max(max_sum, window_sum)  # Update max sum
        right += 1  # Expand right boundary

    return max_sum

if __name__ == '__main__':
    # Example usage:
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(kadanesAlgorithm(nums))  # Output: 6
    print(max_subarray_sum(nums))  # Output: 6
