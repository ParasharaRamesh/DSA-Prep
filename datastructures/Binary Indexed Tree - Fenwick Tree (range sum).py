'''
Binary Indexed Tree (Fenwick Tree):

* USUALLY USED WHEN THE OPERATIONS ARE INVERTABLE AND PREFIX LIKE ( E.G. SUM, PRODUCT)
* HARD TO USE THIS FOR RANGE MINIMUM QUERIES! ( can use 2 different BIT's in reverse to get this )

* better to use 1 based indexing. BIT[0] stores no important information
* idea is that each index of this tree stores some partial range related answer
* given a number x:
    * x & -x => returns the first set bit (000...10000.)
    * doing x - (x&-x) => removes the first set bit from x (e.g. in 13 -> 1101 it will become 1100)
    * same can also be achieved by doing x & (x-1)
* BIT[i] = stores partial range answer from [j+1 -> i] where j = i&(i-1) (or) i - (i&-i) {j is the binary number i but with the right most set bit removed)

* lets say we need the sum of the first 10 elements, we can refer to the BIT array which was already constructed
BIT[10] => 0b1010 => [1000 + 1 -> 1010] => sum from [9,10]
BIT[8] => 0b1000 => [0000 + 1 -> 1000] => sum from [1,8]
BIT[1] => sum from [1,1]

adding these 3 numbers will give us the answer. Just literally depends on the number of set bits in the number we care for.

if we want from range (l,r) => bit_sum(r) - bit_sum(l-1)

* how to update the BIT though?
- logically if say the ith index now has a new value, then all of the places which has that partial range (sum) needs to be updated
- how to find all of those though? just find the last set bit of the index i and keep adding that to the number
new_x = x + (x & -x) => keep doing this until out of range. Since the new_x will also contain the values in the range from x
e.g 13 => 1101
add last set bit
1101 + 0001 => 1110 (14) 14 would have stored the values from [12 + 1 -> 14] therefore it needs to be updated
* add last set bit to 14 again 1110 + 0010 => 10000 [16] => 16 would have stored from [0 + 1 -> 16] anyways therefore since that range contains 14 it also needs to be updated

* How to construct it though?
- use the same logic for updating and just update from [1 -> n] ( do 1 based indexing ) [start with 0]
- this way each element will get added to the BIT[i] along with all of the other indexes where that range is included later on

'''

class BIT:
    def __init__(self, arr):
        self.arr = arr
        self.bit = [0] * (len(arr) + 1)  # 1 based indexing so we need n+1 size, 0th index doesn't matter / is useless in this case

        # constructing the BIT
        for i, x in enumerate(arr):
            # from 1 -> n
            self.update(i, x)

    def update(self, i, val):
        # in the index i we try to put the val along wih all the other places it will be used
        n = len(self.arr)

        # BIT is a 1 indexed array
        i += 1
        while i <= n:
            # was initially 0 so we are adding val
            self.bit[i] += val

            # we also have to add it to all of the other later indices which include this 'i' in its range
            i += i & -i

    def query(self, i):
        # 1 indexed array
        i += 1

        # in this case the sum from 0 -> i using the bit array
        res = 0
        while i > 0:
            res += self.bit[i]

            i -= (i & -i)  # will remove the last set bit
            # i = i & (i-1) # this is also an alternative

        return res

    def range_query(self, l, r):
        return self.query(r) - self.query(l - 1)


if __name__ == '__main__':
    arr = [0, 1, 2, 3, 4, 5, 6]
    fenwick = BIT(arr)
    print(fenwick.query(2))
    print(fenwick.query(3))
    print(fenwick.query(4))
    print(fenwick.range_query(3, 5))
