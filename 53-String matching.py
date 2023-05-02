def calculateLengthOfLongestPrefixCumSuffix(word):
    n = len(word)
    i = 0
    j = 1
    matchingPrefixSuffixLength = 0

    while j < n:
        if word[i] == word[j]:
            i += 1
            matchingPrefixSuffixLength += 1
        else:
            i = 0
            matchingPrefixSuffixLength = 0

        j += 1

    return matchingPrefixSuffixLength

def computePrefix(substring):
    prefix = [0] * len(substring)

    for i in range(1, len(substring)):
        prefix[i] = calculateLengthOfLongestPrefixCumSuffix(substring[:i+1])

    return prefix

def knuthMorrisPrattAlgorithm(string, substring):
    prefix = computePrefix(substring)
    i = 0
    j = 0
    n = len(string)
    m = len(substring)

    while i < n:
        while i < n and j < m and string[i] == substring[j]:
            #keep moving together!
            i += 1
            j += 1

        if j == m:
            #match is found at index i - j
            return True
        elif j > 0:
            #if at all some part of sub string was matched!
            # reset j to point just after current longest prefix, i will stay the same
            j = prefix[j-1]
        else:
            i += 1

    return False



if __name__ == '__main__':
    main = "aefoaefcdaefcdaed"
    subs = "aefcdaed"
    # main = "caba"
    # subs = "aba"
    print(knuthMorrisPrattAlgorithm(main, subs))

