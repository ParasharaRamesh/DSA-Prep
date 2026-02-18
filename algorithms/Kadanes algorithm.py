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
    max_sum = float('-inf')  # best subarray sum seen so far
    window_sum = 0           # current window sum (our "state")
    left = 0                 # left boundary of the sliding window

    for right in range(len(nums)):
        # 1. GROW: add the right element into the window/state
        window_sum += nums[right]

        # 2. EVALUATE: this window [left, right] is a valid candidate
        #    (for Kadane, even negative sums can be the best answer)
        max_sum = max(max_sum, window_sum)

        # 3. SHRINK: while the window is "invalid" for Kadane
        #    (i.e., sum < 0, so it can never help future subarrays),
        #    move left and remove elements from the state
        while left <= right and window_sum < 0:
            window_sum -= nums[left]
            left += 1

    return max_sum

if __name__ == '__main__':
    # Example usage:
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4,17,-9,10,1]
    print(kadanesAlgorithm(nums))
    print(kadanesAlgorithm_sliding_window(nums))
