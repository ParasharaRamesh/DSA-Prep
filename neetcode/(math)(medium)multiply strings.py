'''
You are given two strings num1 and num2 that represent non-negative integers.

Return the product of num1 and num2 in the form of a string.

Assume that neither num1 nor num2 contain any leading zero, unless they are the number 0 itself.

Note: You can not use any built-in library to convert the inputs directly into integers.

Example 1:

Input: num1 = "3", num2 = "4"

Output: "12"
Example 2:

Input: num1 = "111", num2 = "222"

Output: "24642"
Constraints:

1 <= num1.length, num2.length <= 200
num1 and num2 consist of digits only.
'''


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        res = ""

        # try to multiply num1 with each digit of num2 and add it
        for i, digit in enumerate(reversed(num2)):
            digit_multiplication = self.multiply_digit(num1, digit)
            suffix_zeros = "0" * i
            digit_multiplication += suffix_zeros
            res = self.add(res, digit_multiplication)

        if all([d == "0" for d in res]):
            return "0"

        return res

    def multiply_digit(self, num, digit):
        if digit == "0":
            return "0"

        if digit == "1":
            return num

        res = ""

        digit = int(digit)
        carry = 0

        for nd in reversed(num):
            nd = int(nd)

            carry_mul, mul = divmod(nd * digit, 10)
            carry_sum, mul = divmod(carry + mul, 10)

            carry = carry_mul + carry_sum

            res += str(mul)

        if carry > 0:
            res += str(carry)

        res = res[::-1]

        if all([d == "0" for d in res]):
            return "0"

        # trim leading zeros
        while res and res[0] == "0":
            res = res[1:]

        return res

    def add(self, num1, num2):
        # trivial case of adding zeros
        if all([d == "0" for d in num1]):
            return num2

        if all([d == "0" for d in num2]):
            return num1

        # make both strings of same length
        diff = abs(len(num1) - len(num2))
        if len(num1) < len(num2):
            num1 = "0" * diff + num1
        elif len(num2) < len(num1):
            num2 = "0" * diff + num2

        res = ""
        carry = 0
        for d1, d2 in zip(reversed(num1), reversed(num2)):
            d1 = int(d1)
            d2 = int(d2)
            carry, add = divmod(d1 + d2 + carry, 10)
            res += str(add)

        if carry > 0:
            res += str(carry)

        res = res[::-1]

        if all([d == "0" for d in res]):
            return "0"

        # trim leading zeros
        while res and res[0] == "0":
            res = res[1:]

        return res


if __name__ == '__main__':
    s = Solution()

    # test add
    # print(s.add("9", "1"))
    # print(s.add("3", "4"))
    # print(s.add("9", "11"))
    # print(s.add("90", "00"))
    # print(s.add("0000", "10"))

    # test mul digit
    # print(s.multiply_digit("123", "4"))
    # print(s.multiply_digit("99", "2"))

    # test multiply
    # print(s.multiply("111", "222")) # 24642
    # print(s.multiply("10", "22")) # 220
    # print(s.multiply("150", "15")) # 2250
    # print(s.multiply("0", "9"))
    # print(s.multiply("0", "9"))

    # print(s.multiply_digit("1234", "4"))
    # print(s.multiply_digit("1234", "3"))
    # print(s.multiply_digit("1234", "2"))
    # print(s.multiply_digit("1234", "1"))


    print(s.multiply("1234", "4321")) #5332114
