'''
An array with numbers representing the jump indices + means jump right and - means jump left.

Need to check if all the numbers are used once and in a cycle

'''

def hasSingleCycle(array):
    visitedCount = 0
    i = 0
    n = len(array)
    while array[i] is not None and visitedCount < n:
        #keep track of the jump
        jump = array[i]

        #mark it
        print(f"visiting {i} and marking {array[i]} to None!")
        array[i] = None

        #increment the visited count
        visitedCount += 1

        #do the jump
        i += jump
        i = i % n

    return visitedCount == len(array) and i == 0


if __name__ == '__main__':
    # array = [2, 3, 1, -4, -4, 2]
    array = [2, 2, 2]
    print(hasSingleCycle(array))