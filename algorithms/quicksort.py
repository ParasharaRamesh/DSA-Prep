from random import *


'''
Boundary partition:

Imagine a wall (at a particular index) which we keep incrementing from the left side.
Eventually everything to the left of the wall (including the wall) will have elements lesser than the pivot ,
everything to the right of that wall will have elements greater than the pivot

so eventually we will get a state where

[...lesser than equal to pivot](greater than pivot](pivot)
                              b

In the end we just have to put the pivot into place, so we just swap b+1 and pivot.

Initially the boundary starts at -1, the pivot is the rightmost element.
we keep growing the boundary as long as we see elements smaller than the pivot and then we try to fit that smaller element into the newly growing boundary space

'''


def lumato_partition(arr, low, high):
    pivot = arr[high]

    # initially we set boundary to one position before low, because we don't know how many elements are going to be lesser
    boundary_index = low - 1

    # we go only till the last element before the pivot (i.e. excluding the pivot)
    for i in range(low, high):
        if arr[i] <= pivot:
            # grow the boundary first
            boundary_index += 1

            # now that we have grown the boundary, we know that the current element at i needs to go to the newly created boundary index, so we just swap them
            arr[i], arr[boundary_index] = arr[boundary_index], arr[i]

    # Place the pivot at the position after the boundary because that is where it is supposed to go eventually
    arr[high], arr[boundary_index + 1] = arr[boundary_index + 1], arr[high]
    return boundary_index + 1


'''
This is a 2 pointer approach where the left pointer keeps moving until we find an element greater than the pivot and the right pointer moves until we find an element lesser than the pivot, 
once we find both if the order of the 2 pointers are still maintained we swap them
'''


def hoare_partition(arr, low, high):
    pivot = arr[high]

    l = low
    r = high - 1
    while True:
        # find first element greater than pivot
        while l <= r and arr[l] <= pivot:
            l += 1

        # find first element lesser than pivot
        while l <= r and arr[r] > pivot:
            r -= 1

        if l >= r:
            break

        # swap and advance pointers
        arr[l], arr[r] = arr[r], arr[l]

    # put the pivot in the correct place because now l >= r, so l might be greater than the pivot index
    arr[l], arr[high] = arr[high], arr[l]
    return l


def quicksort(arr, use_lumato_partition=True):
    # base case
    if len(arr) <= 1:
        return arr

    if use_lumato_partition:
        pivot_index = lumato_partition(arr, 0, len(arr) - 1)
    else:
        pivot_index = hoare_partition(arr, 0, len(arr) - 1)

    pivot = arr[pivot_index]

    # we dont need to sort including the pivot again
    # sort the first half excluding the pivot
    left_partition = quicksort(arr[:pivot_index], use_lumato_partition)

    # sort the next half excluding the pivot
    right_partition = quicksort(arr[pivot_index + 1:], use_lumato_partition)

    return left_partition + [pivot] + right_partition


if __name__ == '__main__':
    pass
    # arr = [8, 4, 1, 6, 9, 7, 2, 0, 3, 5]
    # pivot_index = lumato_partition(arr, 0, len(arr) - 1)
    # print(pivot_index, arr)
    # print(quicksort(arr, True))

    # arr = [randint(0, 100) for _ in range(20)]
    # pivot_index = hoare_partition(arr, 0, len(arr) - 1)
    # print(pivot_index, arr)
    # print(quicksort(arr, False))
