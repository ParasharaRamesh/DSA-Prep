'''
3752. Lexicographically Smallest Negated Permutation that Sums to Target

You are given a positive integer n and an integer target.

Return the lexicographically smallest array of integers of size n such that:

The sum of its elements equals target.
The absolute values of its elements form a permutation of size n.
If no such array exists, return an empty array.

A permutation of size n is a rearrangement of integers 1, 2, ..., n.

 

Example 1:

Input: n = 3, target = 0

Output: [-3,1,2]

Explanation:

The arrays that sum to 0 and whose absolute values form a permutation of size 3 are:

[-3, 1, 2]
[-3, 2, 1]
[-2, -1, 3]
[-2, 3, -1]
[-1, -2, 3]
[-1, 3, -2]
[1, -3, 2]
[1, 2, -3]
[2, -3, 1]
[2, 1, -3]
[3, -2, -1]
[3, -1, -2]
The lexicographically smallest one is [-3, 1, 2].

Example 2:

Input: n = 1, target = 10000000000

Output: []

Explanation:

There are no arrays that sum to 10000000000 and whose absolute values form a permutation of size 1. Therefore, the answer is [].



Constraints:

1 <= n <= 105
-1010 <= target <= 1010
'''
class Solution:
    def lexSmallestNegatedPerm(self, n: int, target: int) -> List[int]:
        S = n * (n + 1) // 2

        # any number not in range
        if not (-S <= target <= S):
            return []
        
        # all numbers in AP -S, -S + 2, -S + 4.... S are all valid
        # which means that target + 2.k = S so we can use that to eliminate
        if (S - target) % 2 != 0:
            return []

        '''
        . Now we know that the target is possible for sure
        . Lets say we flip some number x E [1, n] to negative then the total sum becomes S - 2x. I.e. its contributing factor is 2x
        . we know that target + 2k = S; which means that k = (S-target)/2 => the sum of those numbers which we flip should be k 
        . we greedily go from n -> 1 and see which numbers we can flip to get the sum to k 
        '''
        k = (S - target) // 2

        # go in reverse from n -> 1 and see if a higher number can be flipped greedily as that is lexographically smaller
        numbers = list(range(1, n+1))
        curr_sum = 0

        for num in range(n, 0, -1):
            if curr_sum + num <= k:
                curr_sum += num
                numbers[num-1] *= -1

        # sort the numbers to return the correct order
        numbers.sort()

        return numbers
        
