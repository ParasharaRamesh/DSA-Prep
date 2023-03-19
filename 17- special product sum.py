def productSum(array):
    return util(array, 1)


def util(array, depth):
    total = 0
    for val in array:
        if type(val) == list:
            total += (depth+1) * util(val, depth+1)
        else:
            total += val

    return total

if __name__ == '__main__':
    print(productSum([5, 2, [7, -1], 3, [6, [-13, 8], 4]]))