from itertools import * 
from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = set()
        nums = list(range(1, n+1))

        def helper(i, combo):
            if len(combo) == k:
                res.add(tuple(sorted(combo.copy())))
                return 

            if i == len(nums) or len(combo) > k:
                # technically speaking the combo case can never be greater 
                return

            # include
            helper(i + 1, combo + [nums[i]])

            # exclude
            helper(i + 1, combo)

        helper(0, [])
        res = [list(combo) for combo in res]
        return res

    def combine_with_itertools(self, n: int, k: int) -> List[List[int]]:
        nums = list(range(1, n+1))
        combs = list(combinations(nums, k))        
        combs = [list(comb) for comb in combs]
        return combs