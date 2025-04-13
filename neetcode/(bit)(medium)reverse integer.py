'''
You are given a signed 32-bit integer x.

Return x after reversing each of its digits. After reversing, if x goes outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0 instead.

Solve the problem without using integers that are outside the signed 32-bit integer range.

Example 1:

Input: x = 1234

Output: 4321
Example 2:

Input: x = -1234

Output: -4321
Example 3:

Input: x = 1234236467

Output: 0
Constraints:

-2^31 <= x <= 2^31 - 1
'''

from math import *


class Solution:
    def reverse(self, x: int) -> int:
        s = str(x)
        is_neg = s[0] == "-"

        if is_neg:
            s = s[1:]

        s = s[::-1]

        res = int(s)

        if res != 0 and ceil(log(res, 2)) > 31:
            return 0

        return -res if is_neg else res