'''
You are given an array of strings tokens that represents a valid arithmetic expression in Reverse Polish Notation.

Return the integer that represents the evaluation of the expression.

The operands may be integers or the results of other operations.
The operators include '+', '-', '*', and '/'.
Assume that division between integers always truncates toward zero.
Example 1:

Input: tokens = ["1","2","+","3","*","4","-"]

Output: 5

Explanation: ((1 + 2) * 3) - 4 = 5
Constraints:

1 <= tokens.length <= 1000.
tokens[i] is "+", "-", "*", or "/", or a string representing an integer in the range [-100, 100].


'''
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        ops = {
            "+": lambda x, y: int(x) + int(y),
            "-": lambda x, y: int(x) - int(y),
            "*": lambda x, y: int(x) * int(y),
            "/": lambda x, y: int(int(x) / int(y))
        }
        stack = []
        is_number = lambda t: t not in ops

        for token in tokens:
            if is_number(token):
                stack.append(token)
                # print(f"stack after pushing number {token} => {stack}")
            else:
                second = stack.pop()
                first = stack.pop()
                stack.append(str(ops[token](first, second)))
                # print(f"{first} {token} {second} = {ops[token](first, second)}, stack is now {stack}")

        return int(stack.pop())