from itertools import product
from typing import List, Tuple
from functools import lru_cache
from collections import deque

#TLE on all solutions here! :(

class Solution:
    # tabulation approach
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        # if no piles exist then return 0
        if not piles:
            return 0

        # in all other cases you can store the values
        cache = dict()

        # state should be ((pileIndices,..), k)
        # push the base cases whereever k is 0
        lengthRangePiles = list(map(lambda pile: list(range(len(pile) + 1)), piles)) #len+1 to consider cases when that particular pile is already done!
        allPossibleIndices = list(product(*lengthRangePiles))

        del lengthRangePiles

        for baseCase in allPossibleIndices:
            state = (tuple(baseCase), 0)
            cache[state] = 0

        # do the tabularization

        # traverse through all possibilities

        # for each k_ from [1,k]
        for k_ in range(1, k + 1):
            # for each possibileIndices from n piles, go in reverse from each pile having 1 element to all piles full!
            for possibleIndices in reversed(allPossibleIndices):
                maxForCurrK = float("-inf")
                currState = (possibleIndices, k_)

                # for that particular indices state; in jth pile remove top, i.e. move that index forward and reduce k
                for j in range(len(piles)):
                    if possibleIndices[j] < len(piles[j]):
                        # jth pile's curr index
                        top = piles[j][possibleIndices[j]]

                        # compute new indices after incrementing jth pile
                        existingIndices = list(possibleIndices)
                        existingIndices[j] += 1
                        existingIndices = tuple(existingIndices)

                        # reuse old dp state
                        cachedOldState = (existingIndices, k_ - 1)
                        cachedOldValue = cache[cachedOldState]

                        # tabulate!
                        maxForCurrK = max(
                            maxForCurrK,
                            top + cachedOldValue
                        )
                    else:
                        #we are already at the end of the stack so cant do anything
                        # reuse old dp state as we cant change the state of the piles, but can decrease the coins
                        cachedOldState = (tuple(possibleIndices), k_ - 1)
                        cachedOldValue = cache[cachedOldState]

                        # tabulate! top has no value here!
                        maxForCurrK = max(
                            maxForCurrK,
                            cachedOldValue
                        )

                # found the best possible from current state tabulate it now
                cache[currState] = maxForCurrK

        finalState = (tuple([0] * len(piles)), k)

        return cache[finalState]

    # memoization approach { time limit exceeded, due to stack overflow :( }
    def maxValueOfCoins_memoization(self, piles: List[List[int]], k: int) -> int:
        return self.solve(self.changeToNestedTuple(piles), k)

    @lru_cache(maxsize=None)
    def solve(self, piles, k):
        # base case
        if k == 0 or not piles:
            return 0

        # init
        maxValue = float("-inf")
        pileIndex = 0

        # check all piles and try removing from each
        while pileIndex < len(piles):
            topInThatPile, newPilesIfRemoved = self.removeTopFromPile(pileIndex, piles)
            if topInThatPile:
                newMax = topInThatPile + self.solve(newPilesIfRemoved, k - 1)
                maxValue = max(newMax, maxValue)
            pileIndex += 1

        return maxValue

    # necessary to use tuples in order to cache
    def removeTopFromPile(self, i: int, piles: Tuple[Tuple[int]]) -> Tuple[Tuple[int]]:
        # convert to nested deque for manipulation
        piles = self.changeToNestedDeque(piles)

        ele = None
        if piles[i]:
            ele = piles[i].popleft()

        # convert back to tuple
        return ele, self.changeToNestedTuple(piles)

    def changeToNestedTuple(self, l):
        return tuple(map(lambda x: tuple(x), l))

    def changeToNestedDeque(self, t):
        return deque(map(lambda x: deque(x), t))


if __name__ == '__main__':
    s = Solution()

    # test case 1 (101)
    # piles = [[1, 100, 3], [7, 8, 9]]
    # k = 2

    # test case 2 (706)
    piles = [[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]]
    k = 7

    print(s.maxValueOfCoins(piles, k))
