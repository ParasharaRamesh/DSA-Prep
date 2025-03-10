'''
Basically have a local and global sum

Keep growing the local sum little by little and put that as the global sum!
'''
def kadanesAlgorithm(array):
    globalSum = localSum = array[0]

    for x in array[1:]:
        localSum = max(x, localSum + x)
        globalSum = max(globalSum, localSum)

    return globalSum