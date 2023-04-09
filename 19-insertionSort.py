'''
assume first element is sorted and repeatedly insert into correct position
'''
def insertionSort(array):
    n = len(array)

    if n == 0 or n == 1:
        return array

    for boundary in range(1, n):
        for j in range(boundary, 0, -1):
            if array[j] <= array[j-1]:
                array[j], array[j-1] = array[j-1], array[j]

    return array


if __name__ == '__main__':
    print(insertionSort([2,1,3,0,9,5,11]))