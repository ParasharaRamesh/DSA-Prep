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
        nums = list(range(1, n + 1))
        combs = list(combinations(nums, k))
        combs = [list(comb) for comb in combs]
        return combs

    def combine_with_replacement_itertools(self, n: int, k: int) -> List[List[int]]:
        nums = list(range(1, n + 1))
        combs = list(combinations_with_replacement(nums, k))
        combs = [list(comb) for comb in combs]
        return combs

    def combine_with_replacement_recursive(self, n: int, k: int) -> List[List[int]]:
        nums = list(range(1, n + 1))
        res: List[List[int]] = []

        def helper(start: int, combo: List[int]) -> None:
            if len(combo) == k:
                res.append(combo.copy())
                return

            if start == len(nums):
                return

            for i in range(start, len(nums)):
                helper(i, combo + [nums[i]])

        helper(0, [])
        return res

    def combine_with_replacement_include_exclude(self, n: int, k: int) -> List[List[int]]:
        nums = list(range(1, n + 1))
        res: List[List[int]] = []

        def helper(i: int, combo: List[int]) -> None:
            if len(combo) == k:
                res.append(combo.copy())
                return

            if i == len(nums):
                return

            # include nums[i] (with replacement: i stays the same)
            helper(i, combo + [nums[i]])

            # exclude nums[i] (move forward)
            helper(i + 1, combo)

        helper(0, [])
        return res


if __name__ == "__main__":
    s = Solution()

    # Test for itertools-based combinations with replacement
    assert sorted(s.combine_with_replacement_itertools(3, 2)) == sorted(
        [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    )

    # Test for recursive combinations with replacement
    assert sorted(s.combine_with_replacement_recursive(3, 2)) == sorted(
        [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    )

    # Test for include/exclude combinations with replacement
    assert sorted(s.combine_with_replacement_include_exclude(3, 2)) == sorted(
        [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    )