def isMonotonic(array):
    if len(array) == 0:
        return True

    isAscending = None

    for i in range(1, len(array)):
        if array[i - 1] < array[i]:
            if isAscending == None:
                isAscending = True
            elif not isAscending:
                return False
        elif array[i - 1] > array[i]:
            if isAscending == None:
                isAscending = False
            elif isAscending:
                return False

    return True


if __name__ == '__main__':
    # array = []
    # array = [4,4,4]
    # array = [1,3,4,5]
    # array = [3,3,4,2]
    array = [3,3,2,1]
    print(isMonotonic(array))
