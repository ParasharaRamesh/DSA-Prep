'''
Design an algorithm to encode a list of strings to a single string. The encoded string is then decoded back to the original list of strings.

Please implement encode and decode

Example 1:

Input: ["neet","code","love","you"]

Output:["neet","code","love","you"]
Example 2:

Input: ["we","say",":","yes"]

Output: ["we","say",":","yes"]
Constraints:

0 <= strs.length < 100
0 <= strs[i].length < 200
strs[i] contains only UTF-8 characters.

'''
from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return "#"

        res = ""

        for i, s in enumerate(strs):
            for j, ch in enumerate(s):
                res += f"{ord(ch)},"
            res = res[:-1] + "|"

        # print(res[:-1])
        return res[:-1]

    def decode(self, s: str) -> List[str]:
        if s == "#":
            return []

        res = []
        words = s.split("|")

        for word in words:
            ords = word.split(",")
            w = ""

            for o in ords:
                if o != "":
                    w += chr(int(o))
            res.append(w)

        # print(res)
        return res

