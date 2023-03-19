from collections import OrderedDict

def firstNonRepeatingCharacter(string):
    counts = OrderedDict()
    for i, char in enumerate(string):
        if char not in counts:
            counts[char] = [i]
        else:
            counts[char].append(i)

    index = -1

    for key in counts:
        if len(counts[key]) == 1:
            index = counts[key][0]
            break

    return index


if __name__ == "__main__":
    print(firstNonRepeatingCharacter("acdcabf"))