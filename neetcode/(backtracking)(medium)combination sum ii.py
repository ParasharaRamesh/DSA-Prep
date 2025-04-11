'''
You are given an array of integers candidates, which may contain duplicates, and a target integer target. Your task is to return a list of all unique combinations of candidates where the chosen numbers sum to target.

Each element from candidates may be chosen at most once within a combination. The solution set must not contain duplicate combinations.

You may return the combinations in any order and the order of the numbers in each combination can be in any order.

Example 1:

Input: candidates = [9,2,2,4,6,1,5], target = 8

Output: [
  [1,2,5],
  [2,2,4],
  [2,6]
]
Example 2:

Input: candidates = [1,2,3,4,5], target = 7

Output: [
  [1,2,4],
  [2,5],
  [3,4]
]
Constraints:

1 <= candidates.length <= 100
1 <= candidates[i] <= 50
1 <= target <= 30

'''
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combos = set()

        def helper(i, total, combo):
            if total == target:
                combos.add(tuple(combo))
                return
            elif total > target or i == len(candidates):
                return

            # include
            helper(i + 1, total + candidates[i], combo + [candidates[i]])

            #backtracking include approach
            # combo.append(candidates[i])
            # helper(i+1, left - candidates[i], combo)
            # combo.pop()

            # exclude ( can just pick the next element which is not that )
            while i + 1 < len(candidates) and candidates[i] == candidates[i+1]:
                i += 1

            helper(i + 1, total, combo)


        helper(0, 0, [])

        return list(
            map(
                lambda combo: list(combo),
                combos
            )
        )

if __name__ == '__main__':
    s = Solution()
    print(s.combinationSum2([1,2,3,4,5], 7)) #expected [[1,2,4],[2,5],[3,4]]
    print(s.combinationSum2([9,2,2,4,6,1,5], 8)) #expected [[1,2,5],[2,2,4],[2,6]]