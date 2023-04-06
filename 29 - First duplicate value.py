from collections import OrderedDict
from functools import reduce

def compareAllRanges(duplicates):
    duplicateItems = duplicates.items()  # [k, [0,1]]
    minDuplicate = reduce(compareAndFindMinBetweenTwoDuplicates, duplicateItems)
    return minDuplicate[0] #get the element

def compareAndFindMinBetweenTwoDuplicates(duplicate1, duplicate2):
    # should also return in form of [k, [occ0, occ1]]
    oneSmall = None
    oneEnd = None
    twoSmall = None
    twoEnd = None

    ele1 = None
    ele2 = None

    # call one of the ranges as 'one' and 'two'
    if duplicate1[1][0] < duplicate2[1][0]:
        oneSmall = duplicate1[1][0]
        oneEnd = duplicate1[1][1]
        twoSmall = duplicate2[1][0]
        twoEnd = duplicate2[1][1]

        ele1 = duplicate1[0]
        ele2 = duplicate2[0]
    else:
        oneSmall = duplicate2[1][0]
        oneEnd = duplicate2[1][1]
        twoSmall = duplicate1[1][0]
        twoEnd = duplicate1[1][1]

        ele1 = duplicate2[0]
        ele2 = duplicate1[0]

    # compare them
    if oneEnd < twoSmall:
        return [ele1, [oneSmall, oneEnd]]
    elif oneEnd < twoEnd:
        return [ele1, [oneSmall, oneEnd]]
    else:
        return [ele2, [twoSmall, twoEnd]]

def firstDuplicateValue(array):
    # get indices of occurence
    count = OrderedDict()
    for i, x in enumerate(array):
        if x not in count:
            count[x] = [i]
        else:
            count[x].append(i)

    # if there are no duplicates might as well return -1
    duplicates = dict()

    areThereDuplicates = False
    for k in count:
        if len(count[k]) > 1:
            areThereDuplicates = True
            duplicates[k] = count[k]

    if not areThereDuplicates:
        return -1

    # now amongst duplicates modify it such a way that no more than 2 elements exist in the array,
    for k in duplicates:
        if len(duplicates[k]) > 2:
            duplicates[k] = duplicates[k][:2]  # only keep first two and discard rest!

    return compareAllRanges(duplicates)


if __name__ == '__main__':
    # array = [2, 1, 5, 3, 3, 2, 4]  # 3
    array = [2, 1, 2, 5, 3, 3, 2, 4]  # 2
    print(firstDuplicateValue(array))
