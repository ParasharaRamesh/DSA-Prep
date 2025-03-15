from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = set()

        # print(f"nums is {nums}")
        for i in range(len(nums) - 2):
            j = i + 1
            k = len(nums) - 1
            target = nums[i] * -1
            # print(f"i, j, k is {(i, j, k)}, res is {res}")

            while j < k:
                if nums[j] + nums[k] == target:
                    res.add(tuple([nums[i], nums[j], nums[k]]))
                    j += 1
                elif nums[j] + nums[k] < target:
                    j += 1
                else:
                    k -= 1

        res = list(res)
        res = [list(r) for r in res]
        return res
