'''
Given an integer n, count the number of 1's in the binary representation of every number in the range [0, n].

Return an array output where output[i] is the number of 1's in the binary representation of i.

Example 1:

Input: n = 4

Output: [0,1,1,2,1]
Explanation:
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100

Constraints:

0 <= n <= 1000
'''
from typing import List

class Solution:
    def count(self, n):
        res = 0
        while n > 0:
            res += (n & 1)
            n = n >> 1

        return res

    def countBits_naive(self, n: int) -> List[int]:
        return [self.count(num) for num in range(0, n + 1)]

    def countBits(self, n: int) -> List[int]:
        res = [0] * (n + 1)

        for i in range(1, n + 1):
            pow2 = i.bit_length() - 1

            #recursion is dp[n] = 1 + dp[n-2**(MSB - 1)]
            res[i] = 1 + res[i - (1 << pow2)]

        return res

    