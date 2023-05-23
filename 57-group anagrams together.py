from collections import Counter

def groupAnagrams(words):
    result = []
    counters = {}

    for word in words:
        wordCount = Counter(word)
        counts = list(wordCount.items())

        #sort in alphabetical order
        counts.sort(key= lambda x: x[0])

        #fix the sorted order
        counts = tuple(counts)

        #nested tuple is hashable!
        if counts not in counters:
            counters[counts] = [word]
        else:
            counters[counts].append(word)

    for count, anagrams in counters.items():
        result.append(anagrams)

    return result


if __name__ == '__main__':
    words = ["yo", "act", "flop", "tac", "foo", "cat", "oy", "olfp"]
    print(groupAnagrams(words))