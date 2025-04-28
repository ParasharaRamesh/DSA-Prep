from functools import lru_cache

@lru_cache(maxsize=None)
def longestCommonSubsequence(str1, str2):
    if not str1 or not str2:
        return []

    equalCase = []
    chooseOneIgnoreTwo = []
    chooseTwoIgnoreOne = []
    # ignoreBoth = []

    if str1[0] == str2[0]:
        #include the common character
        equalCase.append(str1[0])
        #extend with rest
        equalCase.extend(longestCommonSubsequence(str1[1:], str2[1:]))
    else:
        #extend with other possibilities
        chooseOneIgnoreTwo.extend(longestCommonSubsequence(str1[1:], str2))
        chooseTwoIgnoreOne.extend(longestCommonSubsequence(str1, str2[1:]))
        # ignoreBoth.extend(longestCommonSubsequence(str1[1:], str2[1:]))

    #ignore both case is not needed!
    possibilities = [
        [len(equalCase), equalCase],
        [len(chooseOneIgnoreTwo), chooseOneIgnoreTwo],
        [len(chooseTwoIgnoreOne), chooseTwoIgnoreOne]
        # [len(ignoreBoth), ignoreBoth]
    ]

    return max(possibilities)[1]

if __name__ == '__main__':
    str1 = "abcdefghijklmnopqrstuvwxyz"
    str2 = "!fdaa m p t x z req"
    print(longestCommonSubsequence(str1, str2))