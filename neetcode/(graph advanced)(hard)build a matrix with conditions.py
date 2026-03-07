'''
You are given a positive integer k. You are also given:

a 2D integer array rowConditions of size n where rowConditions[i] = [above[i], below[i]], and
a 2D integer array colConditions of size m where colConditions[i] = [left[i], right[i]].
The two arrays contain integers from 1 to k.

You have to build a k x k matrix that contains each of the numbers from 1 to k exactly once. The remaining cells should have the value 0.

The matrix should also satisfy the following conditions:

The number above[i] should appear in a row that is strictly above the row at which the number below[i] appears for all i from 0 to n - 1.
The number left[i] should appear in a column that is strictly left of the column at which the number right[i] appears for all i from 0 to m - 1.
Return any matrix that satisfies the conditions. If no answer exists, return an empty matrix.

Example 1:

Input: k = 3, rowConditions = [[2,1],[1,3]], colConditions = [[3,1],[2,3]]

Output: [[2,0,0],[0,0,1],[0,3,0]]
Example 2:

Input: k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]

Output: []
Constraints:

2 <= k <= 400
1 <= rowConditions.length, colConditions.length <= 10,000
rowConditions[i].length == colConditions[i].length == 2
1 <= above[i], below[i], left[i], right[i] <= k
above[i] != below[i]
left[i] != right[i]

'''

from collections import defaultdict

class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        row_order = self.toposort(k, rowConditions)
        if not row_order:
            return []

        col_order = self.toposort(k, colConditions)
        if not col_order:
            return []

        res = [[0 for i in range(k)] for j in range(k)]
        
        num_to_row = dict()
        for i, num in enumerate(row_order):
            num_to_row[num] = i 

        for j, num in enumerate(col_order):
            i = num_to_row[num]
            res[i][j] = num 

        return res

    def toposort(self, k, conditions: List[List[int]]) -> Optional[List[int]]:
        order = []
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for x, y in conditions:
            graph[x].append(y)
            indegree[y] += 1

        def process(node):
            nonlocal order 
            order.append(node)

            indegree[node] -= 1

            for neigh in graph[node]:
                indegree[neigh] -= 1

                if indegree[neigh] == 0:
                    process(neigh)

        for i in range(1, k+1):
            if indegree[i] == 0:
                process(i)

        print(order)
        return order if len(order) == k else None
