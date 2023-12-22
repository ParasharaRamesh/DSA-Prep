import math

#1. purely recursive solution
def recur(changeLeft, noOfCoins, denoms):
    if changeLeft < 0:
        return math.inf

    if changeLeft == 0:
        return noOfCoins

    noOfCoinsWithEachDenom = []
    for denom in denoms:
        if denom <= changeLeft:
            noOfCoinsWithEachDenom.append(recur(changeLeft - denom, noOfCoins + 1, denoms))
    if len(noOfCoinsWithEachDenom) > 0:
        return min(noOfCoinsWithEachDenom)
    else:
        return math.inf

def minNumberOfCoinsForChange_recursive(n, denoms):
    if len(denoms) == 0:
        #trivial edge case
        return -1

    if n == 0:
        return 0

    noOfCoins = recur(n, 0, denoms)
    if noOfCoins == math.inf:
        return -1
    else:
        return noOfCoins

# 2. slightly better recursive solution
def minNumberOfCoinsForChange_recur2(n, denoms):
    if len(denoms) == 0:
        #trivial edge case
        return -1

    if n == 0:
        return 0

    if n < 0:
        return math.inf

    noOfCoins = 1 + min([minNumberOfCoinsForChange(n-denom, denoms) for denom in denoms])
    if noOfCoins == math.inf:
        return -1
    else:
        return noOfCoins

#3. Memoization
def memoize(wrapper):
    cache = dict()
    def cacheIt(n, denoms):
        key = (n, tuple(denoms))
        if key in cache:
            return cache[key]

        cache[key] = wrapper(n, denoms)

        return cache[key]

    return cacheIt


@memoize
def dp(n, denoms):
    if len(denoms) == 0:
        #trivial edge case
        return math.inf

    if n == 0:
        return 0

    if n < 0:
        return math.inf

    noOfCoins = 1 + min([dp(n-denom, denoms) for denom in denoms])
    if noOfCoins == math.inf:
        return math.inf
    else:
        return noOfCoins

def minNumberOfCoinsForChange(n, denoms):
    ans = dp(n, denoms)
    if ans == math.inf:
        return -1
    return ans

if __name__ == '__main__':
    n = 7
    denoms = [2,4]
    print(minNumberOfCoinsForChange(n, denoms))