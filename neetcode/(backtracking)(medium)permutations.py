from reprlib import recursive_repr
from typing import List


class Solution:
    #This is the recursive solution
    def permute(self, nums: List[int]) -> List[List[int]]:
        if len(nums) == 0:
            return []

        if len(nums) == 1:
            return [nums]


        permutations_without_first = self.permute(nums[1:])

        # add the first character in between
        res = []

        for perm in permutations_without_first:
            for i in range(len(perm) + 1):
                p = perm[:i] + [nums[0]] + perm[i:]
                res.append(p)

        return res

    # Backtracking solution
    def permute_backtracking(self, nums: List[int]) -> List[List[int]]:
        res = []

        def helper(i):
            # if you have reached the end append to the list of permutations
            if i == len(nums):
                res.append(nums.copy())
                return 

            # if not take each 
            for j in range(i, len(nums)):
                # try the jth char in the ith place
                nums[i], nums[j] = nums[j], nums[i]
                # go into recursion
                helper(i+1)
                # revert the backtracking
                nums[i], nums[j] = nums[j], nums[i]
            
        helper(0)
        return res

    # Johsnson trotter algorithm (only if the elements are comparable )
    def permute_jt(self, nums: List[int]) -> List[List[int]]:
        perms = []

        #start in a sorted manner
        curr = list(sorted(nums.copy()))
        perms.append(curr)

        # keep finding the next permutation
        while True:
            curr = self.next_permutation(curr)
            if not curr:
                break
            perms.append(curr)
        return perms

    # finds the next permutation in lexicographical order
    def next_permutation(self, curr):
        """
        Generate the next lexicographically greater permutation of `curr`.
        Returns None if `curr` is the highest permutation.
        """
        next_perm = curr.copy()

        # Step 1: scan from the right to locate the pivot index `i`.
        # We care about finding the longest decreasing suffix
        # The pivot is where the ascending trend (moving right-to-left) breaks.
        # Example: in [1, 3, 5, 4, 2], we stop at 3 (index 1) because 3 < 5.
        i = len(next_perm) - 2
        while i >= 0 and next_perm[i] >= next_perm[i + 1]:
            i -= 1

        if i < 0:
            # Example: [5, 4, 3, 2, 1] has no pivot; we are already at the last permutation.
            return None

        # Step 2: find the smallest element larger than the pivot in the suffix.
        # Continuing the example: pivot=3, so we walk from the end to find 4—the first value > 3.
        j = len(next_perm) - 1
        while next_perm[j] <= next_perm[i]:
            j -= 1

        # Step 3: swap the pivot and its successor.
        # Our running example becomes [1, 4, 5, 3, 2] after swapping 3 and 4.
        next_perm[i], next_perm[j] = next_perm[j], next_perm[i]

        # Step 4: reverse the suffix to restore the lowest order for the tail.
        # The suffix [5, 3, 2] was descending; reversing gives [2, 3, 5], final result [1, 4, 2, 3, 5].
        next_perm[i + 1:] = next_perm[i + 1:][::-1]

        return next_perm


if __name__ == '__main__':
    s = Solution()
    elements = [1,2,3]
    recursive = s.permute(elements)
    print(f"{recursive = }")
    backtrack = s.permute_backtracking(elements)
    print(f"{backtrack = }")
    jts = s.permute_jt(elements)
    print(f"{jts = }")
