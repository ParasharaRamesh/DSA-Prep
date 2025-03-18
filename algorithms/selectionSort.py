'''
find the minimum from left boundary till end and keep increasing it

'''
def selectionSort(array):
    n = len(array)

    if n == 0 or n == 1:
        return array

    for boundary in range(0, n-1): #left boundary of already sorted
        for j in range(n -1, boundary, -1): #from boundary to the right to get the minimum
            if array[j] <= array[j-1]:
                array[j-1], array[j] = array[j], array[j-1]

    return array


if __name__ == '__main__':
    array = [3,4,1,6,5,2,2,0,10,29]
    print(selectionSort(array))