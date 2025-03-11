# DP memoization approach
def memoize(fn):
    cache = dict()
    def cacheIt(array):
        args = tuple(array)
        if args not in cache:
            cache[args] = fn(array)
        return cache[args]
    return cacheIt


@memoize
def maxSubsetSumNoAdjacent_DPMemoize(array):
    if len(array) == 0:
        return 0

    if len(array) == 1:
        return array[0]

    return max(
        array[0] + maxSubsetSumNoAdjacent_DPMemoize(array[2:]),
        maxSubsetSumNoAdjacent_DPMemoize(array[1:])
    )


#better approach with O(1) space and O(N) time complexity... just keep track of two numbers as we dont need the whole O(N) space
def maxSubsetSumNoAdjacent(array):
    prev = 0
    prevPrev = 0
    maxSum = 0
    for i in range(len(array)):
        maxSum = max(
            prev,
            prevPrev + array[i]
        )
        prevPrev = prev
        prev = maxSum

    return maxSum


if __name__ == '__main__':
    arr = [75, 105, 120, 75, 90, 135]
    # print(maxSubsetSumNoAdjacent(tuple(arr)))
    print(maxSubsetSumNoAdjacent(arr))