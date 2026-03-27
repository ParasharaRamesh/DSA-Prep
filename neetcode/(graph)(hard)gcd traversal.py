'''
You are given a 0-indexed integer array nums, and you are allowed to traverse between its indices. You can traverse between index i and index j, i != j, if and only if gcd(nums[i], nums[j]) > 1, where gcd is the greatest common divisor.

Your task is to determine if for every pair of indices i and j in nums, where i < j, there exists a sequence of traversals that can take us from i to j.

Return true if it is possible to traverse between all such pairs of indices, or false otherwise.

 

Example 1:

Input: nums = [2,3,6]
Output: true
Explanation: In this example, there are 3 possible pairs of indices: (0, 1), (0, 2), and (1, 2).
To go from index 0 to index 1, we can use the sequence of traversals 0 -> 2 -> 1, where we move from index 0 to index 2 because gcd(nums[0], nums[2]) = gcd(2, 6) = 2 > 1, and then move from index 2 to index 1 because gcd(nums[2], nums[1]) = gcd(6, 3) = 3 > 1.
To go from index 0 to index 2, we can just go directly because gcd(nums[0], nums[2]) = gcd(2, 6) = 2 > 1. Likewise, to go from index 1 to index 2, we can just go directly because gcd(nums[1], nums[2]) = gcd(3, 6) = 3 > 1.
Example 2:

Input: nums = [3,9,5]
Output: false
Explanation: No sequence of traversals can take us from index 0 to index 2 in this example. So, we return false.
Example 3:

Input: nums = [4,3,12,8]
Output: true
Explanation: There are 6 possible pairs of indices to traverse between: (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), and (2, 3). A valid sequence of traversals exists for each pair, so we return true.
 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 105

'''

from typing import List
from math import gcd

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.size = {}

    def create_set(self, value):
        """
        Create a standalone set for value if it does not exist yet.
        * Make all values point to None initially -> topmost nodes
        """
        if value not in self.parent:
            self.parent[value] = None
            self.size[value] = 1

    def find(self, value):
        """
        Find the root representative without path compression.
        * Traverse up the tree until we reach the topmost node (None)
        * Return the parent/root. Which is that node which has a parent pointer as None (almost like linked list traversal)
        """
        if value not in self.parent:
            return None
        curr = value
        while self.parent[curr] is not None:
            curr = self.parent[curr]
        return curr

    def union(self, a, b):
        """Merge by size: attach smaller-size tree under larger-size tree."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a is None or root_b is None or root_a == root_b:
            return

        size_a = self.size.get(root_a, 0)
        size_b = self.size.get(root_b, 0)

        if size_a <= size_b:
            # make a's parent as b because a is smaller
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        elif size_a > size_b:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]

    def get_size(self, node) :
        """getting the size of the connected component node belongs to"""
        parent = self.find(node)
        return self.size[parent]

class Solution:
    '''
    Do union find on a graph where:
        a. we have numbers on one side
        b. we have all of the unique prime factors across all numbers on the other side
        c. we do union for a number with all of its unique prime factors
    
    On this after doing union operation if we are left with a single connected component then it is possible
    Same as checking if the size of the connected component is the same as the number of individual ids inside the union find datastructure
    '''
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True
            
        if all([num == 1 for num in nums]):
            return False

        # construct the graph between primes to numbers and then use union find to see if there is just one connected component
        uf = UnionFind()
        num_to_primes = self.prime_factors_for_numbers(nums)

        for num in num_to_primes:
            uf.create_set(num)
            primes = num_to_primes[num]

            for prime in primes:
                uf.create_set(prime)
                uf.union(num, prime)

        return uf.get_size(nums[0]) == len(uf.parent)


    def prime_factors_for_numbers(self, numbers):
        """
        Return a dictionary mapping each number in the list to its distinct prime factors.

        Uses a sieve to precompute smallest prime factors up to the maximum number,
        then factorises each number in O(log n) time per number.

        Parameters:
            numbers (list of int): List of integers (may include 0, 1, negative, etc.)

        Returns:
            dict: {number: list_of_distinct_primes}
        """
        if not numbers:
            return {}

        max_val = max(numbers)
        
        # Step 1: Build smallest prime factor (SPF) array
        spf = self.build_spf(max_val)

        # Step 2: Factorise each number using SPF
        result = {}
        for n in numbers:
            if n < 2:
                result[n] = []          # No prime factors
                continue

            factors = set()
            x = n
            while x > 1:
                p = spf[x]
                factors.add(p)
                # reduce it completely
                while x % p == 0:
                    x //= p
            result[n] = sorted(factors)   # optional sorting for readability

        return result

    def build_spf(self, n):
        """
        Return SPF array where spf[i] = smallest prime factor of i
        """

        #1: create array spf[i] = i
        spf = list(range(n+1))

        #2: set spf[0] and spf[1]
        spf[0] = 1 # because it cannot be 0 as you cant divide by zero

        # 3: loop i from 2 to sqrt(n)
        for i in range(2, int(n**0.5) + 1):
            if spf[i] != i:
                # it is already marked therefore skip it
                continue

            # 4: here spf[i] = i (means prime)

            # 5: for multiples j of i:
                # only update if not already updated
                # (this ensures smallest factor)
            """
            We assign SPF only once per number.

            Since we process primes in increasing order,
            the first prime that reaches a number is its smallest prime factor.

            So we never need to compare or overwrite.
            """ 
            multiplier = i
            for j in range(i*multiplier, n+1, multiplier):
                # this should set it so that we always retain the smallest prime factor
                # spf[j] = min(i, spf[j])

                # or you can also do it this way 
                if spf[j] == j: # if it is yet to be marked
                    spf[j] = i #just mark it once with the current prime number , this way 12 will be marked by 2 once and not by 3 again

        return spf