def runLengthEncoding(string):
    currChar = string[0] if len(string) > 0 else None
    currCount = 0
    rle = ""

    for char in string:
        if char != currChar or currCount == 9:
            #print the old rle first
            rle += f"{currCount}{currChar}"

            #now change it
            currChar = char
            currCount = 1
        else:
            currCount += 1

    #last grouping too!
    if currChar:
        rle += f"{currCount}{currChar}"

    return rle

if __name__ == '__main__':
    #1a1A1a1A5a1A3a4A1B3b4B
    string = "aAaAaaaaaAaaaAAAABbbbBBBB"
    # string = "aaabbb"
    print(runLengthEncoding(string))