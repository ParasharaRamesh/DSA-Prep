def semordnilap(words):
    # Write your code here.
    palindromes = []
    wordsDict = {x: False for x in words}
    for word in words:
        if not wordsDict[word]:
            reverseWord = word[::-1]
            if reverseWord in wordsDict and not wordsDict[reverseWord] and word != reverseWord:
                wordsDict[word] = True
                wordsDict[reverseWord] = True
                palindromes.append([word, reverseWord])

    return palindromes


if __name__ == "__main__":
    pass