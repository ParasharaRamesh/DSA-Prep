'''
You are given a 2D integer array intervals, where intervals[i] = [left_i, right_i] represents the ith interval starting at left_i and ending at right_i (inclusive).

You are also given an integer array of query points queries. The result of query[j] is the length of the shortest interval i such that left_i <= queries[j] <= right_i. If no such interval exists, the result of this query is -1.

Return an array output where output[j] is the result of query[j].

Note: The length of an interval is calculated as right_i - left_i + 1.

Example 1:

Input: intervals = [[1,3],[2,3],[3,7],[6,6]], queries = [2,3,1,7,6,8]

Output: [2,2,3,5,1,-1]
Explanation:

Query = 2: The interval [2,3] is the smallest one containing 2, it's length is 2.
Query = 3: The interval [2,3] is the smallest one containing 3, it's length is 2.
Query = 1: The interval [1,3] is the smallest one containing 1, it's length is 3.
Query = 7: The interval [3,7] is the smallest one containing 7, it's length is 5.
Query = 6: The interval [6,6] is the smallest one containing 6, it's length is 1.
Query = 8: There is no interval containing 8.

Constraints:

1 <= intervals.length <= 10**5
1 <= queries.length <= 10**5
intervals[i].length == 2
1 <= lefti <= righti <= 10**7
1 <= queries[j] <= 10**7

Thoughts:

1. slightly better than brute force:( but wont work !)
* sort it (Ilog(I) = 10^5*15 -> 10^6
* for each query:
    - binary search and find one index
    - from there grow to left and right and find all intervals which include that query number
    - pick the smallest from that
    = q * (log(q) + q) = 10 ^ 10 (TLE)

2. Using heaps:
    - keep some bookkeeping for the query to all of its original indices
    - sort both the intervals and the queries
    - for each query:
        . iterate through the intervals and add all the ones to the heap where the qyery >= start value
            - this will give us the set of intervals amongst which a subset will contain the query.
            - If we had restricted instead we might not have included all of the intervals
        . now from the heap keep popping as long the interval's end is before the query ( remove all of the invalid stuff from the min heap)
        . pick the minimum from that and add to the result
        . however dont pop it, as this minimum might apply to more queries also. Only remove when you are sure that the end value is < current query.
'''

from typing import List
from heapq import *
from collections import defaultdict

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # book keeping
        query_to_index = defaultdict(list)
        for i, query in enumerate(queries):
            query_to_index[query].append(i)


        result = [-1] * len(queries)

        # sort both
        intervals.sort(key=lambda x: x[0])

        queries = list(set(queries))
        queries.sort()

        # init heap
        min_size_heap = []

        # interval pointer
        i = 0

        for query in queries:
            # add all relevant ones to the heap
            while i < len(intervals) and intervals[i][0] <= query:
                start, end = intervals[i]
                size = end - start + 1

                # min heap with first priority as size ( as we want smaller sizes) , second priority as the ending value as we want to pick the one which ends earlier
                item = (size, end, intervals[i])
                heappush(min_size_heap, item)
                i += 1

            # from heap pop all the ones which are out of range and have the end value smaller than query, meaning they are no longer relevant ( to even other future queries too because queries were already sorted)
            while min_size_heap and min_size_heap[0][1] < query:
                heappop(min_size_heap)

            # add the size to the result list
            if min_size_heap:
                indices = query_to_index[query]
                for ind in indices:
                    result[ind] = min_size_heap[0][0]

        return result


if __name__ == '__main__':
    s = Solution()

    intervals = [[4, 5], [5, 8], [1, 9], [8, 10], [1, 6]]
    queries = [7, 9, 3, 9, 3]
    expected = [4, 3, 6, 3, 6]
    res = s.minInterval(intervals, queries)
    assert res == expected, f"expected {expected} but got {res}"

    intervals = [[1, 4], [2, 4], [3, 6], [4, 4]]
    queries = [2, 3, 4, 5]
    expected = [3, 3, 1, 4]
    res = s.minInterval(intervals, queries)
    assert res == expected, f"expected {expected} but got {res}"

    intervals = [[2, 3], [2, 5], [1, 8], [20, 25]]
    queries = [2, 19, 5, 22]
    expected = [2, -1, 4, 6]
    res = s.minInterval(intervals, queries)
    assert res == expected, f"expected {expected} but got {res}"

    intervals = [[1, 3], [2, 3], [3, 7], [6, 6]]
    queries = [2, 3, 1, 7, 6, 8]
    expected = [2, 2, 3, 5, 1, -1]
    res = s.minInterval(intervals, queries)
    assert res == expected, f"expected {expected} but got {res}"
