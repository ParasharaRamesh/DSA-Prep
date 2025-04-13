'''
Given a 32-bit unsigned integer n, reverse the bits of the binary representation of n and return the result.

Example 1:

Input: n = 00000000000000000000000000010101

Output:    2818572288 (10101000000000000000000000000000)
Explanation: Reversing 00000000000000000000000000010101, which represents the unsigned integer 21, gives us 10101000000000000000000000000000 which represents the unsigned integer 2818572288.
'''


class Solution:
    def reverseBits(self, n: int) -> int:
        stack = []
        while n > 0:
            stack.append(n & 1)
            n = n >> 1

        stack = stack + [0] * (32 - len(stack))
        res = 0

        for i, num in enumerate(reversed(stack)):
            res += num * (2 ** i)

        return res

    def reverseBits_optimal(self, n: int) -> int:
        res = 0
        for i in range(32):
            bit = (n >> i) & 1
            res += (bit << (31 - i))
        return res