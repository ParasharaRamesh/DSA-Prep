from typing import List


class Solution:
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

if __name__ == '__main__':
    s = Solution()
    print(s.permute([1,2,3]))