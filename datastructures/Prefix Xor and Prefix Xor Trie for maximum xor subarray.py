'''
Given an array arr[] of size, N. Find the subarray with maximum XOR. A subarray is a contiguous part of the array.


Example 1:

Input:
N = 4
arr[] = {1,2,3,4}
Output: 7
Explanation: 
The subarray {3,4} has maximum xor 
value equal to 7.

Example 2:

Input:
N = 3
arr[] = {1,4,3}
Output: 7
Explanation: 
 There are 6 possible subarrays:
 subarray            XOR value
 [1]                     1
 [4]                     4
 [3]                     3
 [1, 4]                  5 (1^4)
 [4, 3]                  7 (4^3)
 [1, 4, 3]               6 (1^4^3)

 [4, 3] subarray has maximum XOR value. So, return 7.
Your Task:  
You don't need to read input or print anything. Your task is to complete the function maxSubarrayXOR() which takes the array arr[], its size N as input parameters and returns the maximum xor of any subarray.
 

Expected Time Complexity: O(N)
Expected Auxiliary Space: O(N)

 

Constraints:
1 <= N <= 10**5
1 <= arr[i] <= 10**5
'''

'''
Main idea:

. Brute forcing all subarrays and finding xor -> O(N^3)
. could use a prefix xor array to get it to -> O(N^2)
    - for all subarrays in l , r just do prefix[r+1] ^ prefix[l] to get the range prefix in O(1)
. Even better idea is to do it in O(N * d) , where d is the bit length of the max element in the array
    - in this case for 10**5 -> 17 
    - therefore answer will be O(17. N)
. Idea is that for every index r in the xor prefix array -> we just need to find the best possible l such that it is an exact complement
    - e.g. if prefix[r] == 1100 , we want to try and find 0011 so that we can maximise the xor of both
    - in case 0011 is not available greedily go for the next best thing
. Use tries to now store the xor prefix (upto depth d)
    - so that we can use it to find the best complementary match and then take xor and take max
'''
from collections import defaultdict

class Solution:
    def maxSubarrayXOR (self, N, arr):
        # construct prefix xor array & keep track of max
        max_prefix_xor = 0
        prefix = [0]
        
        for num in arr:
            val = prefix[-1] ^ num
            max_prefix_xor = max(max_prefix_xor, val)
            prefix.append(val)
            
        # utility to get range_xor (not required)
        # range_xor = lambda l,r : prefix[r + 1] ^ prefix[l]
        
        # get the bit length of the max_xor as depth of the trie
        depth = max_prefix_xor.bit_length()
        xor_prefix_trie = PrefixBitTrie(depth)
            
        # now do the query
        res = 0 
        
        # for every prefix[i] find the best complementary prefix seen thus far
        for i in range(1, len(prefix)):
            # insert the previous values
            xor_prefix_trie.insert(prefix[i-1])
        
            # get best matching prefix
            best_complementary_prefix = xor_prefix_trie.search_best_complementary(prefix[i])
            
            # take xor in this range
            res = max(res, best_complementary_prefix ^ prefix[i])
              
        return res
        
class BitNode:
    def __init__(self):
        self.children = defaultdict(int)
        self.end = False
        
    def __str__(self):
        return f"Node(children={self.children}, end={self.end})"
        
class PrefixBitTrie:
    def __init__(self, depth):
        self.depth = depth
        self.root = BitNode()
    
    def __str__(self):
        return str(self.root)
        
    def insert(self, bits):
        # each needs to be inserted based on this depth
        n = self.depth
        
        # dfs and insert
        curr = self.root
        for i in range(n-1, -1, -1):
            bit = (bits >> i) & 1
            if bit not in curr.children:
                curr.children[bit] = BitNode()
            
            curr = curr.children[bit]
            
        # mark end
        curr.end = True
    
    def search_best_complementary(self, bits):
        n = self.depth
        
        curr = self.root
        
        # definitely need to search for the prefix upto this depth 
        res = 0
        for i in range(n-1, -1, -1):
            bit = (bits >> i) & 1
            complement = bit ^ 1
            
            # make room to fill the prefix
            res = res << 1
            
            val = bit
            if complement in curr.children:
                val = complement
            elif bit in curr.children:
                val = bit
            else:
                print(f"Invalid state !")
                
            res |= val
            curr = curr.children[val]
            
        return res

if __name__ == "__main__":
    s = Solution()

    arr = [9,5,3]  
    expected = 15
    ans = s.maxSubarrayXOR(len(arr), arr)
    assert ans == expected, f"{arr=} {expected=} {ans=}"

    arr = [1,4,3]
    expected = 7
    ans = s.maxSubarrayXOR(len(arr), arr)
    assert ans == expected, f"{arr=} {expected=} {ans=}"

    arr = [1,2,3,4]
    expected = 7
    ans = s.maxSubarrayXOR(len(arr), arr)
    assert ans == expected, f"{arr=} {expected=} {ans=}"
