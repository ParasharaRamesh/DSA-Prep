def validIPAddresses(string):
    validIps = []
    validate(string, "", 3, validIps)
    return validIps

def isValidIpChunk(string):
    if not string:
        return False

    n = len(string)
    startsWithZero = int(string[0]) == 0
    isInRange = 0 <= int(string) <= 255
    hasUptoThreeChars = n <= 3

    return isInRange and ((startsWithZero and n == 1) or (not startsWithZero and hasUptoThreeChars))

def validate(pending, currFormedIp, remainingDots, validIps):
    if remainingDots == 0:
        if isValidIpChunk(pending):
            validIps.append(currFormedIp + f".{pending}")
        return

    i = 0
    while i < 3:
        chunk = pending[:i + 1]
        if isValidIpChunk(chunk):
            chunkToAdd = currFormedIp + f".{chunk}" if remainingDots < 3 else chunk
            validate(pending[i + 1:], chunkToAdd, remainingDots - 1, validIps)
        i += 1


if __name__ == '__main__':
    str = "1928610"
    print(validIPAddresses(str))
