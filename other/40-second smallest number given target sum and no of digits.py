'''
NOT OPTIMAL SOLUTION AS RECURSION DEPTH EXCEEDS FOR LARGE INPUTS!!

Instead of starting with 1 in the beginning can do with 9 in the end !


'''

from collections import deque

class Solution:
    def secondSmallest(self, S, D):
        smallestNumberList = self.findSmallest(S, D)
        return self.modifySmallestToGetSecondSmallest(smallestNumberList) if smallestNumberList else -1

    def findSmallest(self, target, noOfDigits):
        # some kind of backtracking and check if noOfDigitsLeft * 9 exceeds rest of target
        smallestNumberList = [0] * noOfDigits
        smallestNumberList[0] = 1

        isPossible = self.findSmallestUtil(target, noOfDigits, smallestNumberList, 0)

        return smallestNumberList if isPossible else []

    def findSmallestUtil(self, target, noOfDigits, state, stateIndex):
        if target >= noOfDigits * 9:
            return False

        if noOfDigits == 1:
            if target <= 9:
                state[stateIndex] = target
                return True
            else:
                return False

        if (target - state[stateIndex]) <= (noOfDigits - 1) * 9:
            # if remaining target is doable
            return self.findSmallestUtil(target - state[stateIndex], noOfDigits - 1, state, stateIndex + 1)
        else:
            #tried incrementing it once already for current stateIndex
            while state[stateIndex] < 9:
                #try once more
                state[stateIndex] = self.incrementDigit(state[stateIndex])

                #from target subtract the stateIndex's value as that has been incremented that many times!
                isPossible = self.findSmallestUtil(target - state[stateIndex], noOfDigits - 1, state, stateIndex + 1)

                #if it is possible just return and finish it, else continue
                if isPossible:
                    return True

        #tried it completely got exhausted!
        return False

    def incrementDigit(self, digit):
        if digit == 9:
            return 0
        else:
            return digit + 1

    def modifySmallestToGetSecondSmallest(self, smallestDigits):
        # go from backside and traverse till 9's finish and modify those 2
        i = len(smallestDigits) - 1
        areThereNinesInTheEnd = False

        while i >= 0:
            if smallestDigits[i] == 9:
                areThereNinesInTheEnd = True
                i -= 1
            else:
                break

        #if not possible return -1
        if i == -1:
            return -1

        # modify smallest digits list
        if areThereNinesInTheEnd:
            # modify i and i + 1th places
            smallestDigits[i] += 1
            smallestDigits[i + 1] -= 1
        else:
            # modify i -1 and ith place
            smallestDigits[i - 1] += 1
            smallestDigits[i] -= 1

        return self.convertDigitListIntoNumber(smallestDigits)

    def getIndividualDigits(self, number):
        digits = deque()

        while number > 0:
            number, digit = divmod(number, 10)
            digits.appendleft(digit)

        return list(digits)

    def convertDigitListIntoNumber(self, digits):
        num = 0
        for i, digit in enumerate(digits[::-1]):
            num += digit * (10 ** i)
        return num


if __name__ == '__main__':
    s = Solution()

    # target = 20
    # noOfDigits = 3
    #expected answer 389 as smallest is 299

    target = 69874
    noOfDigits = 79636
    # smallest is 1099 therefore ans 1189

    print(s.secondSmallest(target, noOfDigits))

