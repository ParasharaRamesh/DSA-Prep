class Solution:
    def findComplement(self, num: int) -> int:
        mask = (1 << num.bit_length()) - 1
        comp = ~num
        return mask & comp

    def twosComplement(self, num: int) -> int:
        #option 1: 1s complement + 1
        a =  self.findComplement(num) + 1

        #option 2: -x => (1111.....1)(2s complement of x). get mask and & with number
        mask = (1 << num.bit_length()) - 1
        b = mask & -num

        assert a == b
        return b

if __name__ == '__main__':
    s = Solution()
    print(s.twosComplement(5))