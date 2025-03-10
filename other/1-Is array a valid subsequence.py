def isValidSubsequence(array, sequence):
    n = len(array)
    m = len(sequence)

    currArr = 0 # for array
    currSeq = 0 #for sequence


    # for each element in sequence check if it is present in array , if so proceed and remember the previous place
    while (currArr < n) and (currSeq < m) and (m-1-currSeq <= n-1-currArr):
        seqEle = sequence[currSeq]

        #stops when currArr is at the position where it is equal
        while  currArr < n and array[currArr] != seqEle:
            currArr += 1

        if currArr == n:
            return False

        #processed both seq and arr
        currSeq += 1
        currArr += 1

    allProcessedInSequence = (currSeq == m)

    return allProcessedInSequence



if __name__ == "__main__":
    print(isValidSubsequence([5, 1, 22, 25, 6, -1, 8, 10], [1, 6, -1, -1, 10]))
