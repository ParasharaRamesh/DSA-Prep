'''
A string s is called happy if it satisfies the following conditions:

s only contains the letters 'a', 'b', and 'c'.
s does not contain any of "aaa", "bbb", or "ccc" as a substring.
s contains at most a occurrences of the letter 'a'.
s contains at most b occurrences of the letter 'b'.
s contains at most c occurrences of the letter 'c'.
You are given three integers a, b, and c, return the longest possible happy string. If there are multiple longest happy strings, return any of them. If there is no such string, return the empty string "".

A substring is a contiguous sequence of characters within a string.

Example 1:

Input: a = 3, b = 4, c = 2

Output: "bababcabc"
Example 2:

Input: a = 0, b = 1, c = 5

Output: "ccbcc"
Constraints:

0 <= a, b, c <= 100
a + b + c > 0
'''

'''
Thoughts:

. atmost constraint + cant follow 3 times
. start with the highest and go in a greedy way?
. max heap ?
    - keep picking max , put in ans -> decrement count -> put in max
    - keep track of last_char + its longest count
    - if we pick that char as max value, pop, and use the next one and put both back into the heap
        - at this point if the next one is empty then we know we can just completely stop!
. what are examples where it is ""?
    - ? return as default lets see
'''

from heapq import *

class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        res = ""
        max_heap = []

        if a > 0:
            heappush(max_heap, (-a, "a"))
        if b > 0:
            heappush(max_heap, (-b, "b"))
        if c > 0:
            heappush(max_heap, (-c, "c"))

        last_char = None
        last_char_count = 0

        while max_heap:
            count, char = heappop(max_heap)
            count *= -1

            #init case
            if not last_char:
                last_char = char
                last_char_count += 1

                res += char

                count -= 1
                if count > 0:
                    heappush(max_heap, (-count, char))
                continue

            #Case where there are 3: pop twice and check
            if last_char_count == 2 and char == last_char:
                if not max_heap:
                    # directly return answer
                    break

                next_count, next_char = heappop(max_heap)
                next_count *= -1

                last_char = next_char
                last_char_count = 1

                res += next_char
                next_count -= 1

                if next_count > 0:
                    heappush(max_heap, (-next_count, next_char))

                #push old value again
                if count > 0:
                    heappush(max_heap, (-count, char))

                continue

            # greedy picking (its not violating 3 time pick yet!)
            if char == last_char:
                last_char_count += 1
            else:
                last_char = char
                last_char_count = 1

            res += char
            count -= 1

            if count > 0:
                heappush(max_heap, (-count, char))

        return res


if __name__ == '__main__':
    s = Solution()

    a = 7
    b = 1
    c = 0
    expected = "aabaa"
    actual = s.longestDiverseString(a, b, c)
    assert actual == expected, f"{expected = } & {actual = }"

    a = 0
    b = 1
    c = 5
    expected = "ccbcc"
    actual = s.longestDiverseString(a, b, c)
    assert expected == actual, f"{expected = } & {actual = }"

    a = 3
    b = 4
    c = 2
    expected = "bababcabc"
    actual = s.longestDiverseString(a, b, c)
    assert expected == actual, f"{expected = } & {actual = }"

    a = 1
    b = 1
    c = 7
    expected = ["ccaccbcc", "ccbccacc"]
    actual = s.longestDiverseString(a, b, c)
    assert actual in expected, f"{expected = } & {actual = }"
