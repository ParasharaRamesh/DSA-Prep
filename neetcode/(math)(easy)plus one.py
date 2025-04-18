'''
You are given an integer array digits, where each digits[i] is the ith digit of a large integer. It is ordered from most significant to least significant digit, and it will not contain any leading zero.

Return the digits of the given integer after incrementing it by one.

Example 1:

Input: digits = [1,2,3,4]

Output: [1,2,3,5]
Explanation 1234 + 1 = 1235.

Example 2:

Input: digits = [9,9,9]

Output: [1,0,0,0]
Constraints:

1 <= digits.length <= 100
0 <= digits[i] <= 9

'''

from collections import deque

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        res = deque([])
        i = len(digits) - 2

        carry, new = divmod(digits[-1] + 1, 10)
        res.appendleft(new)


        while i >= 0:
            carry, new = divmod(digits[i] + carry, 10)
            res.appendleft(new)
            i -= 1


        if carry > 0:
            res.appendleft(carry)

        return list(res)