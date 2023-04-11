from collections import defaultdict
from itertools import combinations

def getAllPairSums(array):
    allPairSums = defaultdict(list)
    visited = []
    for i, x in enumerate(array):
        for j, y in enumerate(array):
            pair = [i, j]
            if i != j and set(pair) not in visited:
                pairSum = x + y
                visited.append(set(pair))
                allPairSums[pairSum].append(pair)

    return allPairSums


def getFourSum(pairOfIndices, otherPairOfIndices, array):
    return set([array[pairOfIndices[0]],
            array[pairOfIndices[1]],
            array[otherPairOfIndices[0]],
            array[otherPairOfIndices[1]]])


def fourNumberSum(array, targetSum):
    # get extra space of O(N2)
    allPairSums = getAllPairSums(array)

    # for each pair check if the targetSum - pairSum exists
    fourSums = []
    for pairSum in allPairSums:
        otherSum = targetSum - pairSum
        if otherSum in allPairSums:
            if otherSum != pairSum:
                # case 1: the other pair exists and is not the same as pair sum. then find all products where there is no intersection
                for pair in allPairSums[pairSum]:
                    for otherPair in allPairSums[otherSum]:
                        intersection = set(pair) & set(otherPair)
                        fourSumSet = getFourSum(pair, otherPair, array)
                        if len(intersection) == 0 and fourSumSet not in fourSums:
                            fourSums.append(fourSumSet)
            elif len(allPairSums[pairSum]) > 1:
                # case 2: the other pair is the same as this one and there can be some combinations. If there is only one such pair can ignore
                # get NC2
                possibilities = combinations(allPairSums[pairSum], 2)

                # filter out everything where there is an intersection
                possibileFourSums = list(
                    filter(
                        lambda possibility: len(set(possibility[0]) & set(possibility[1])) == 0,
                        possibilities
                    )
                )

                for possibleFourSum in possibileFourSums:
                    fourSumSet = getFourSum(possibleFourSum[0], possibleFourSum[1], array)
                    if fourSumSet not in fourSums:
                        fourSums.append(fourSumSet)

    return list(map(lambda x: list(x), fourSums))


if __name__ == '__main__':
    array = [7, 6, 4, -1, 1, 2]
    target = 16
    print(fourNumberSum(array, target))
