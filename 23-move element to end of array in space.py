def findNewEndIndex(array, toMove, currEnd):
    # find end index
    while currEnd >= 0 and array[currEnd] == toMove:
        currEnd -= 1

    return currEnd

def moveElementToEnd(array, toMove):
    start = 0
    end = findNewEndIndex(array, toMove, len(array) - 1)

    while start < end:
        if array[start] == toMove:
            #swap it
            array[start], array[end] = array[end], array[start]

            end = findNewEndIndex(array, toMove, end)

            start += 1
        else:
            start += 1

    return array


if __name__ == "__main__":
    array = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 5, 5, 5, 5, 5, 5]
    toMove = 5
    print(moveElementToEnd(array, toMove))