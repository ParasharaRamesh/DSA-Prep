from bisect import bisect


def smallestDifference(a, b):
    # sort it out!
    a.sort()
    b.sort()

    one = None
    two = None

    # find out the ordering of the two windows
    if a[0] <= b[0]:
        one = a
        two = b
    else:
        one = b
        two = a

    ans = None

    # this naming is for ease of use
    if one[-1] <= two[0]:
        # case 1s, 1e, 2s, 2e
        ans = [one[-1], two[0]]
    else:
        # every other case
        # for each element in 2 find the bisection possibility and add it
        possibilities = []

        for item in two:
            possibilities.extend(getMinDiffPossiblePairs(one, item))

        # now amongst all possibilities find the min possbility
        ans = findMinPossibility(possibilities)

    #final ans based on getting first from a and second from b
    return ans if (one == a) else list(reversed(ans))


def getMinDiffPossiblePairs(array, item):
    index = bisect(array, item)

    # it is either that index
    if index == len(array):
        # matching item is in the end so only one possibility
        return [[abs(array[index - 1] - item), [array[index - 1], item]]]
    elif index == 0:
        # matching item is in the beggining so only possibility
        return [[abs(array[index] - item), [array[index], item]]]
    else:
        # two possibilities
        return [
            [abs(array[index - 1] - item), [array[index - 1], item]],
            [abs(array[index] - item), [array[index], item]]
        ]


def findMinPossibility(possibilities):
    minDiff = possibilities[0][0]
    ans = possibilities[0][1]
    for diff, possibility in possibilities[1:]:
        if diff <= minDiff:
            minDiff = diff
            ans = possibility
    return ans


if __name__ == '__main__':
    one = [-1, 5, 10, 20, 28, 3]  # -> [-1, 3, 5, 10, 20, 28]

    two = [26, 134, 135, 15, 17]  # -> [15, 17, 26, 134, 135]
    print(smallestDifference(one, two))
