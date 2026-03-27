"""
1. What is a Prime number?

A prime number is a number greater than 1 that has exactly two divisors:
1 and itself.

Examples:
2, 3, 5, 7, 11...

Non-primes (composites):
4 = 2 * 2
6 = 2 * 3
8 = 2 * 2 * 2

Key idea:
Every composite number can be broken down into prime factors.
This is called PRIME FACTORIZATION.

To check if a number n is prime:

We only need to check divisibility up to sqrt(n), because:
If n = a * b, then at least one of a or b must be <= sqrt(n).

So instead of checking 1 to n-1, we check:
2 to sqrt(n)

Time complexity: O(sqrt(n))
"""

def is_prime(n):
    """
    Return True if n is prime, else False.
    
    Steps:
    1. Handle n < 2
    2. Loop from 2 to sqrt(n)
    3. If divisible -> not prime
    """
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True

assert not is_prime(0)   # False
assert not is_prime(1)   # False
assert is_prime(2)   # True
assert not is_prime(4)   # False
assert not is_prime(9)   # False
assert is_prime(17)  # True

"""
2. Sieve of Eratosthenes:

Goal:
Find all primes up to n efficiently.

Steps:
1. Create a boolean array is_prime[0..n], initialize all to True
2. Mark 0 and 1 as False
3. For i from 2 to sqrt(n):
    If is_prime[i] is True:
        Mark all multiples of i starting from i*i as False

Why start from i*i?
Because smaller multiples are already marked by smaller primes.
 e.g. if i == 5 => 5 * 2 ( already covered by 2 ) , 5 * 3 (already covered by 3), 5 * 4(already covered by 2)

Time Complexity: O(n log log n)

    We mark multiples of each prime p:
        n/p operations

    Total work:
        n * (1/2 + 1/3 + 1/5 + 1/7 + ...)

    This sum over primes ≈ log(log n)

    So total complexity:
        O(n log log n)

    This is faster than O(n log n) because we only process primes,
    and primes become less frequent as numbers grow.
"""
def sieve(n):
    """
    Return list of all primes <= n
    """
    # 1: create boolean list of size n+1 (all True initially)
    N = n + 1 # n + 1 because we start from 0 and 0 based indexing is easier
    is_prime = [True] * N 

    # 2: mark 0 and 1 as False
    is_prime[0] = False
    is_prime[1] = False

    # 3: loop i from 2 to sqrt(n)
    for i in range(2, int(n**0.5) + 1):
        # if the current number is not prime -> already marked -> just skip it!
        if not is_prime[i]:
            continue

        #5: mark multiples starting from i*i
        multiplier = i 
        for j in range(multiplier*i, N, multiplier): # go in jumps of multiplier starting from i^2
            is_prime[j] = False

    # 6. for collecting all indices where value is True
    primes = []

    for i, is_p in enumerate(is_prime):
        if is_p:
            primes.append(i)

    return primes

expected = [2, 3, 5, 7]
ans = sieve(10)
assert ans == expected, f"{expected=} but {ans=}"

expected = [2, 3, 5, 7, 11, 13, 17, 19]
ans = sieve(20)
assert ans == expected, f"{expected=} but {ans=}"

"""
3. Smallest Prime Factor (SPF):

. Instead of trying out all numbers from 2 -> sqrt(n) to see if it is a prime factor we do it a different way
. Instead of figuring out what are the factors for this number, if we instead knew what is the smallest prime factor for every number we can do the following :
    - just keep referencing this spf cache and keep removing the smallest factor and then check the spf[n/smallest factor]
    - shrinks the number in logarithmic time by removing the smallest prime factor at every step

E.g. 

For every number n, store the smallest prime number that divides it.

Number:  2  3  4  5  6  7  8  9 10
SPF:     2  3  2  5  2  7  2  3  2

for n = 12 we can do :
    12 → spf[12] = 2
        12 / 2 = 6

    6 → spf[6] = 2
        6 / 2 = 3

    3 → spf[3] = 3
        3 / 3 = 1

This results in an spf array where i is prime only if spf[i] == i, because that number in itself is the smallest prime which divides it!

Using SPF, we can compute prime factorization in O(log n):

While n > 1:
    factor = spf[n]
    n = n // factor

Each step reduces n, so total steps are logarithmic.
"""
def build_spf(n):
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

expected = [1, 1, 2, 3, 2, 5, 2, 7, 2, 3, 2]
ans = build_spf(10)
assert ans == expected, f"{expected=} but {ans=}"

"""
4. Using the spf array to get all prime factors in logarithmic time

We repeatedly divide n by its smallest prime factor.

Since n reduces by at least a factor of 2 each step,
the number of steps is at most log₂(n).

So time complexity = O(log n)

NOTE: building the spf array as a precomputation step is still O(n loglogn), but with this cached we can answer q queries in O(n loglogn) + O(q logn)

"""
def prime_factors_spf(n):
    spf = build_spf(n)

    prime_factors = []

    while n > 1:
        smallest_prime = spf[n]
        prime_factors.append(smallest_prime)

        n //= smallest_prime

    return prime_factors

expected = [2, 2, 3]
ans = prime_factors_spf(12)
assert ans == expected, f"{expected=} but {ans=}"

expected = [7, 7]
ans = prime_factors_spf(49)
assert ans == expected, f"{expected=} but {ans=}"

expected = [13]
ans = prime_factors_spf(13)
assert ans == expected, f"{expected=} but {ans=}"

"""
5. To find all unique prime factors across a list of numbers:

1. Build SPF up to max(numbers)
2. For each number:
    - Use SPF to get its prime factors
3. Insert factors into a set to ensure uniqueness

Efficient for multiple queries due to preprocessing.

Time Complexity:
- SPF build: O(n log log n)
- Factorization: O(k log n), where k = number of elements
"""

def unique_prime_factors(numbers):
    """
    Return sorted list of unique prime factors across all numbers
    """

    # 1: handle empty list
    if not numbers:
        return []

    # 2: find max number
    N = max(numbers)

    # 3: build SPF once
    spf = build_spf(N)

    # 4: create a set to store unique primes
    primes = set()

    #  5: loop through each number
    for n in numbers:
        # skip numbers < 2 (which also includes negative numbers)
        if n < 2:
            continue

        # 6: get prime factors using SPF
        while n > 1:
            smallest_prime = spf[n]

            primes.add(smallest_prime)

            n //= smallest_prime


    # 7: return sorted result
    return list(sorted(primes))

expected = [2, 3, 5]
ans = unique_prime_factors([12, 15, 20])
assert ans == expected, f"{expected=} but {ans=}"

expected = [2, 7]
ans = unique_prime_factors([14, 28])
assert ans == expected, f"{expected=} but {ans=}"

expected = []
ans = unique_prime_factors([0, 1, -10])
assert ans == expected, f"{expected=} but {ans=}"
