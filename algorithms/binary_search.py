from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return -1

    def leftmost(self, nums: List[int], target: int) -> int:
        # Find the leftmost occurrence or insertion index
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                # Case 1: Match, but keep going left
                r = m - 1
            elif nums[m] < target:
                # Case 2: Go right
                l = m + 1
            else:  # nums[m] > target
                # Case 3: Go left
                r = m - 1
        return l  # l is the insertion index or first occurrence

    def rightmost(self, nums: List[int], target: int) -> int:
        # Find the rightmost occurrence or insertion index
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                # Case 1: Match, but keep going right
                l = m + 1
            elif nums[m] < target:
                # Case 2: Go right
                l = m + 1
            else:  # nums[m] > target
                # Case 3: Go left
                r = m - 1
        # If found, r points to last occurrence; otherwise, l is insertion index
        return r if r >= 0 and nums[r] == target else l

    # --- tests ---

    @staticmethod
    def _test_leftmost_rightmost():
        sol = Solution()

        def test_leftmost(nums, target, expected):
            got = sol.leftmost(nums, target)
            assert got == expected, f"leftmost({nums}, {target}): got {got}, expected {expected}"

        def test_rightmost(nums, target, expected):
            got = sol.rightmost(nums, target)
            assert got == expected, f"rightmost({nums}, {target}): got {got}, expected {expected}"

        # leftmost: first occurrence or insertion index
        test_leftmost([1, 2, 2, 2, 3], 2, 1)
        test_leftmost([1, 2, 2, 2, 3], 1, 0)
        test_leftmost([1, 2, 2, 2, 3], 3, 4)
        test_leftmost([1, 2, 2, 2, 3], 0, 0)
        test_leftmost([1, 2, 2, 2, 3], 4, 5)
        test_leftmost([2, 2, 2], 2, 0)
        test_leftmost([], 1, 0)
        test_leftmost([1], 1, 0)
        test_leftmost([1], 0, 0)
        test_leftmost([1], 2, 1)

        # rightmost: last occurrence or insertion index
        test_rightmost([1, 2, 2, 2, 3], 2, 3)
        test_rightmost([1, 2, 2, 2, 3], 1, 0)
        test_rightmost([1, 2, 2, 2, 3], 3, 4)
        test_rightmost([1, 2, 2, 2, 3], 0, 0)
        test_rightmost([1, 2, 2, 2, 3], 4, 5)
        test_rightmost([2, 2, 2], 2, 2)
        test_rightmost([], 1, 0)
        test_rightmost([1], 1, 0)
        test_rightmost([1], 0, 0)
        test_rightmost([1], 2, 1)

        print("All leftmost/rightmost tests passed.")

if __name__ == "__main__":
    Solution._test_leftmost_rightmost()
