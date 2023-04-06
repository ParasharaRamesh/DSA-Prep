def longestPeak(array):
    '''
    keep going until a peak is reached and monitor the length of the longest peak till then
    '''
    longestPeakLength = 0
    i = 0
    # count current ele and move on !
    ascendingLinkCount = 0
    descendingLinkCount = 0
    inAscendingPhase = None

    while i < len(array) - 1:
        if array[i] == array[i + 1]:  # next is same
            if inAscendingPhase == None:  # if before was also same
                ascendingLinkCount = 0
                descendingLinkCount = 0
            elif inAscendingPhase:  # if before was ascending
                inAscendingPhase = None
                ascendingLinkCount = 0
                descendingLinkCount = 0
            else:  # if before it was descending
                # possibly reached the end of one peak
                longestPeakLength = max(longestPeakLength, ascendingLinkCount + descendingLinkCount + 1)
                inAscendingPhase = None
                ascendingLinkCount = 0
                descendingLinkCount = 0
        elif array[i] < array[i + 1]:  # next is ascending
            if inAscendingPhase == None:  # if before was also same
                # set it as ascending and count current
                inAscendingPhase = True
                ascendingLinkCount += 1
            elif inAscendingPhase:  # if previously it was ascending
                ascendingLinkCount += 1
            else:  # was descending earlier, so end of peak
                longestPeakLength = max(longestPeakLength, ascendingLinkCount + descendingLinkCount + 1)
                ascendingLinkCount = 1  # new start
                descendingLinkCount = 0
        else:  # next is descending
            if inAscendingPhase == None:
                ascendingLinkCount = 0
                descendingLinkCount = 0
            elif inAscendingPhase:
                inAscendingPhase = False
                descendingLinkCount = 1
                longestPeakLength = max(longestPeakLength, ascendingLinkCount + descendingLinkCount + 1)
            else:
                inAscendingPhase = False
                descendingLinkCount += 1
                longestPeakLength = max(longestPeakLength, ascendingLinkCount + descendingLinkCount + 1)

        i += 1

    return longestPeakLength


if __name__ == '__main__':
    # array = [1, 2, 3, 3, 4, 0, 10, 6, 5, -1, -3, 2, 3]
    array = [1, 3, 2]
    print(longestPeak(array))
