from functools import lru_cache
from itertools import *


def nonConstructibleChange(coins):
    # if no coins change is 1
    if len(coins) == 0:
        return 1

    #the range where the value can lie
    low = 1
    high = sum(coins) + 1

    coinsT = tuple(coins)

    for i in range(low, high + 1):
        constructible = isConstructible(coinsT, i)
        if not constructible:
            return i

    return 1

@lru_cache(maxsize=None)
def isConstructible(coins, change):
    if change == 0:
        return True

    if change < 0:
        return False

    if len(coins) == 0:
        return False

    restCoins = coins[1:]
    restChange = change - coins[0]

    withFirst = isConstructible(restCoins, restChange)
    withoutFirst = isConstructible(restCoins, change)

    return  withFirst or withoutFirst

def powerset(iterable):
    s = list(iterable)
    ps = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    sums = dict()
    for l in ps:
        total = sum(l)
        if total not in sums:
            sums[total] = [l]
        else:
            sums[total].append(l)
    return sums


if __name__ == "__main__":
    l = [5, 6, 1, 1, 2, 3, 4, 9] #exp 32, mine 23
    print(nonConstructibleChange(l))

    print(isConstructible(tuple(l), 23))

    # sums = powerset(l)
    # a=1
