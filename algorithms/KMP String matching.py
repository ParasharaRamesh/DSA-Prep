#BRUTE FORCE AND INEFFICIENT
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

# THIS Is apparently the better approach
def compute_kmp_prefix(substring):
    m = len(substring)
    lps = [0] * m  # Longest Proper Prefix which is also a Suffix

    length = 0  # length of the previous longest prefix suffix
    i = 1  # index for the substring ( start at 1 because lps[0] is anyways 0!)

    while i < m:
        if substring[i] == substring[length]:
            # Case 1: Match found. Extend the previous LPS length.
            length += 1
            lps[i] = length
            i += 1
        else:
            # Case 2: Mismatch.
            if length != 0:
                # Fall back! Reset 'length' to the LPS length of the previous character (i-1)
                # The value lps[length - 1] is the next shortest border we can try.
                length = lps[length - 1]
                # NOTE: We do NOT increment 'i' here, we re-check with the new 'length' in the next iteration.
            else:
                # Case 3: length is 0 (no prefix/suffix match found).
                # Set LPS for the current character to 0 and move to the next character.
                lps[i] = 0
                i += 1

    return lps

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

