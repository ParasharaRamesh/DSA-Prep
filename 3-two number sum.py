from collections import Counter


def twoNumberSum(array, targetSum):
    count = Counter(array)
    result = []

    countKeys = list(count.keys())
    for c in countKeys:
        other = targetSum - c
        if other in count:
            if other == c:
                if count[other] > 1:
                    return [c, other]
                else:
                    count.pop(c)
                    continue
            elif count[other] > 0:
                return [c, other]
        else:
            count.pop(c)
    return []

