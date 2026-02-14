'''
We stack glasses in a pyramid, where the first row has 1 glass, the second row has 2 glasses, and so on until the 100th row.  Each glass holds one cup of champagne.

Then, some champagne is poured into the first glass at the top.  When the topmost glass is full, any excess liquid poured will fall equally to the glass immediately to the left and right of it.  When those glasses become full, any excess champagne will fall equally to the left and right of those glasses, and so on.  (A glass at the bottom row has its excess champagne fall on the floor.)

For example, after one cup of champagne is poured, the top most glass is full.  After two cups of champagne are poured, the two glasses on the second row are half full.  After three cups of champagne are poured, those two cups become full - there are 3 full glasses total now.  After four cups of champagne are poured, the third row has the middle glass half full, and the two outside glasses are a quarter full, as pictured below.



Now after pouring some non-negative integer cups of champagne, return how full the jth glass in the ith row is (both i and j are 0-indexed.)

 

Example 1:

Input: poured = 1, query_row = 1, query_glass = 1
Output: 0.00000
Explanation: We poured 1 cup of champange to the top glass of the tower (which is indexed as (0, 0)). There will be no excess liquid so all the glasses under the top glass will remain empty.
Example 2:

Input: poured = 2, query_row = 1, query_glass = 1
Output: 0.50000
Explanation: We poured 2 cups of champange to the top glass of the tower (which is indexed as (0, 0)). There is one cup of excess liquid. The glass indexed as (1, 0) and the glass indexed as (1, 1) will share the excess liquid equally, and each will get half cup of champange.
Example 3:

Input: poured = 100000009, query_row = 33, query_glass = 17
Output: 1.00000
 

Constraints:

0 <= poured <= 109
0 <= query_glass <= query_row < 100
'''
from functools import cache

class Solution:
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        '''
            . f represents the total amount of water flowing through the r,c th cup
            . at each cup it can get half of the surplus flowing from the left cup above it + the half of the surplus flowing from the right cup above it 

        '''
        @cache
        def f(r, c):
            # you start pouring from the first cup
            if r == 0 and c == 0:
                return poured

            # any cup with the column value out of range has no contribution
            if c < 0 or c > r:
                return 0

            '''
                . pascal triangle recursion is f(i, j) = g(f(i-1, j-1)) + g(f(i-1, j)) (as long as j is valid!)
                . surplus will be (F - 1) / 2, because the cup above only gives half of the surplus and if it is overflowing we need to subtract 1 from it.
                . max with 0 because we cannot have negative contribution
            '''
            left = max(0, (f(r-1, c-1) - 1)/2)
            right = max(0, (f(r-1, c) - 1)/2)

            # total is left contribution + right contribution
            return left + right

        # f represents total flow so we take min(1, F) because if it overflows its just 1
        return min(1, f(query_row, query_glass))
