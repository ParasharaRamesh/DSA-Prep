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
        # 🔹 Grow the window: Expand as much as possible
        while right < len(nums) and window_sum >= 0:
            window_sum += nums[right]
            max_sum = max(max_sum, window_sum)
            right += 1  # Move right forward

        # 🔹 Shrink the window if sum becomes negative
        while left < right and window_sum < 0:
            window_sum -= nums[left]  # Remove leftmost element
            left += 1  # Move left boundary forward

    return max_sum

if __name__ == '__main__':
    # Example usage:
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4,17,-9,10,1]
    print(kadanesAlgorithm(nums))
    print(kadanesAlgorithm_sliding_window(nums))
