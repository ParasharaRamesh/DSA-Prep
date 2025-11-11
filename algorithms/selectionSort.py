'''
find the minimum from left boundary till end and keep increasing it

'''
def selection_sort(arr):
    # n is the number of elements in the list
    n = len(arr)

    # Traverse through all elements of the list
    for i in range(n):
        # Assume the current element is the minimum (index i)
        min_idx = i

        # Find the actual minimum element in the remaining unsorted portion
        # The inner loop runs from i+1 to the end of the list
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap the found minimum element with the element at the current position 'i'
        # This places the smallest element into its correct, sorted position
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def selection_sort_pythonic(arr):
    """
    Selection Sort implementation using min() and list slicing.
    Note: This approach might be less efficient than the traditional
    implementation due to the repeated searching with arr.index().
    """
    n = len(arr)

    # Outer loop to iterate through all positions
    for i in range(n):
        # 1. Use list slicing and min() to find the minimum value
        #    in the unsorted portion (from index i to the end).
        unsorted_slice = arr[i:]
        if not unsorted_slice:
            break

        min_value = min(unsorted_slice)

        # 2. Use list.index() to find the index of this minimum value
        #    in the *full list*, starting the search from position i.
        min_idx = arr.index(min_value, i)

        # 3. Swap the element at the current position i with the minimum element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

if __name__ == '__main__':
    array = [3,4,1,6,5,2,2,0,10,29]
    print(selection_sort(array))