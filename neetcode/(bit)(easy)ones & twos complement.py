class Solution:
    def onesComplement(self, num: int) -> int:
        # option 1: use bit mask
        mask = (1 << num.bit_length()) - 1
        comp = ~num
        a = mask & comp

        # option 2: find nearest power of two ( either take log and ceil or just bitlength -1) and do xor
        nearest = (1 << num.bit_length()) - 1
        b = nearest ^ num

        assert a == b
        return a
    def twosComplement(self, num: int) -> int:
        #option 1: 1s complement + 1
        a = self.onesComplement(num) + 1

        #option 2: -x => (1111.....1)(2s complement of x). get mask and & with number
        mask = (1 << num.bit_length()) - 1
        b = mask & -num

        assert a == b
        return b

if __name__ == '__main__':
    s = Solution()
    print(s.onesComplement(5))
    print(s.onesComplement(59))
    print(s.twosComplement(5))