def threeNumberSum(array, target):
    threeSums = []
    n = len(array)

    array.sort()

    # go till the last third
    for i, curr in enumerate(array[:-2]):
        left = i + 1
        right = n - 1

        while left < right:
            currSum = curr + array[left] + array[right]

            if currSum == target:
                threeSums.append([curr, array[left], array[right]])
                left += 1
            elif currSum < target:
                left += 1
            else:
                right -= 1

    return threeSums


if __name__ == '__main__':
    array = [12, 3, 1, 2, -6, 5, -8, 6]
    target = 0
    print(threeNumberSum(array, target))
