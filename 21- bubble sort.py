def bubbleSort(array):
    n = len(array)

    if n == 0 or n == 1:
        return array

    for rightBoundary in range(n-1 , 0, -1):
        for j in range(0, rightBoundary):
            if array[j] >= array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

    return array


if __name__ == '__main__':
    array = [2, 4, 2, 43, 3, 5, 1]
    print(bubbleSort(array))
