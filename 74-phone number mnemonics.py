'''
In a typical phone each of the letter in the english alphabet is associated with a number

given a number string find all the strings which is possible  from that number

'''
def recur(curr, remainingPhoneNumber, map, mnemonics):
    digit = remainingPhoneNumber[0]
    chars = map[digit]

    if len(remainingPhoneNumber) == 1:
        # add all possible endings
        for char in chars:
            mnemonics.append(curr + char)
        return mnemonics

    #there are these many different ways of doing it
    for char in chars:
        mnemonics = recur(curr + char, remainingPhoneNumber[1:], map, mnemonics)

    return mnemonics


def phoneNumberMnemonics(phoneNumber):
    #trivial case
    if len(phoneNumber) == 0:
        return []

    map = {
        "0": ["0"],
        "1": ["1"],
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"]
    }

    mnemonics = []
    mnemonics = recur("", phoneNumber, map, mnemonics)

    return mnemonics

if __name__ == '__main__':
    phoneNumber = "1905"
    print(phoneNumberMnemonics(phoneNumber))