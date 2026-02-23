'''
You are given an encoded string s, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. There will not be input like 3a, 2[4], a[a] or a[2].

The test cases are generated so that the length of the output will never exceed 100,000.

Example 1:

Input: s = "2[a3[b]]c"

Output: "abbbabbbc"
Example 2:

Input: s = "axb3[z]4[c]"

Output: "axbzzzcccc"
Example 3:

Input: s = "ab2[c]3[d]1[x]"

Output: "abccdddx"
Constraints:

1 <= s.length <= 30
s is made up of lowercase English letters, digits, and square brackets '[]'.
All the integers in s are in the range [1, 300].
s is guaranteed to be a valid input.

'''
'''
Thoughts: 

. do stack simulation and get dict opening_bracket_index -> closing_bracket_index
. go through s and keep adding to result
. if you notice a number then next one is definitely opening bracket and call recursive helper to expand 

'''
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        open_to_close = dict()

        for i, c in enumerate(s):
            if c != "[" and c != "]":
                continue

            if c == "[":
                stack.append((i, c))
                continue

            # c is a closing bracket for sure
            if stack[-1][-1] == "[":
                open_i ,_ = stack.pop()
                open_to_close[open_i] = i
                continue

            stack.append((i, c))

        # inclusive
        def helper(i, j):
            if i > j:
                return ""

            if i == j:
                return s[i]

            # print(f"evaluating {i} -> {j} = {s[i:j+1]}")
            res = ""

            k = i

            while k <= j:
                # print(f"{k=} -> {s[k]=} | before {res=} ")

                if s[k].isalpha():
                    res += s[k]
                    k += 1
                    continue
                
                num = ""
                _k = k
                while s[_k].isdigit():
                    num += s[_k]
                    _k += 1

                # _k is the index of the open bracket
                # print(f"collected {num=}")
                num = int(num)
                res += num * helper(_k + 1, open_to_close[_k] - 1)
                k = open_to_close[_k] + 1

            return res

        return helper(0, len(s) - 1)           

        