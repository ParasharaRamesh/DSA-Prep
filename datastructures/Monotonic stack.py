'''

What is it?

. A monotonic stack is a stack (LIFO structure) that maintains its elements in a monotonically increasing or decreasing order.
. A monotonically increasing stack ensures that each element is greater than or equal to the previous one. => next/previous smaller elements
. A monotonically decreasing stack ensures that each element is less than or equal to the previous one. => next/previous greater elements

When is it useful?

. You need to find next greater/next smaller/previous greater/previous smaller elements.
. You need an efficient way (better than brute force O(n^2) to process ranges or sub-arrays.
. Since each element is pushed and popped at most once, monotonic stack solutions run in O(n) time complexity.
. Constraints mentioning array size up to 10^5 or higher (indicating O(n²) won't work). (due to 10^8 computations limit)
'''

# MONTONIC DECREASING ARRAY - for anything to do with greater
def next_greater(arr):
    '''
    Finds the immediately next greater element for each element, i.e the first element to the right that is greater than the current element
    '''
    res = [-1] * len(arr)
    stack = [] # can maintain indices or both indices and values

    for i, x in enumerate(arr):
        # if at all something violates monotonically decreasing stack then keep popping and add to the results
        while stack and stack[-1][1] < x:
            pi, px = stack.pop()
            res[pi] = x
        # add as long as it is monotonically decreasing
        stack.append((i, x))

    return res


def previous_greater(arr):
    '''
    Finds the immediately previous greater element for each element, i.e the first element to the left that is greater than the current element
    '''
    res = [-1] * len(arr)
    stack = [] # just indices

    # previous greater = next greater in reverse order
    for i in range(len(arr)-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            previous_ind = stack.pop()
            res[previous_ind] = arr[i]

        #add to maintain montonoically decreasing
        stack.append(i)

    return res


# MONTONIC INCREASING ARRAY - for anything to do with smaller
def next_smaller(arr):
    '''
    Finds the immediately next smaller element for each element, i.e the first element to the right that is smaller than the current element
    '''
    res = [-1] * len(arr)
    stack = [] # can maintain indices or both indices and values

    for i, x in enumerate(arr):
        # if at all something violates monotonically increasing stack then keep popping and add to the results
        while stack and stack[-1][1] > x:
            pi, px = stack.pop()
            res[pi] = x
        # add as long as it is monotonically increasing
        stack.append((i, x))

    return res


def previous_smaller(arr):
    '''
    Finds the immediately previous smaller element for each element, i.e the first element to the left that is smaller than the current element
    '''
    res = [-1] * len(arr)
    stack = [] # just indices

    # previous smaller = next smaller in reverse order
    for i in range(len(arr)-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            previous_ind = stack.pop()
            res[previous_ind] = arr[i]

        #add to maintain montonoically increasing
        stack.append(i)

    return res


if __name__ == '__main__':
    arr = [2,1,5,3,7,6]
    print(next_greater(arr)) # should be [5,5,7,7,-1.-1]
    print(previous_greater(arr)) # should be [-1,2,-1,5,-1,7]
    print(next_smaller(arr)) # should be [1, -1, 3, -1, 6, -1]
    print(previous_smaller(arr)) # should be [-1, -1, 1, 1, 3, 3]