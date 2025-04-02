'''
You are given an integer n. Return all well-formed parentheses strings that you can generate with n pairs of parentheses.

Example 1:

Input: n = 1

Output: ["()"]
Example 2:

Input: n = 3

Output: ["((()))","(()())","(())()","()(())","()()()"]
You may return the answer in any order.

Constraints:

1 <= n <= 7

'''
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        combos = []

        def helper(num_open, num_close, stack, curr):
            if num_open == 0 and num_close == 0:
                if len(stack) == 0:
                    combos.append(curr)
                return

            if num_open > 0:
                helper(num_open - 1, num_close, stack + ["("], curr + "(")

            if num_close > 0 and stack and stack[-1] == "(":
                stack.pop()
                helper(num_open, num_close - 1, stack, curr + ")")

        helper(n - 1, n, ["("], "(")
        return combos