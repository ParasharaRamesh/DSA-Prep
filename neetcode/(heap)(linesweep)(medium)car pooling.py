'''
There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer capacity and a integer array trips where trips[i] = [numPassengers[i], from[i], to[i]] indicates that the ith trip has numPassengers[i] passengers and the locations to pick them up and drop them off are from[i] and to[i] respectively. The locations are given as the number of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise.

Example 1:

Input: trips = [[4,1,2],[3,2,4]], capacity = 4

Output: true
Example 2:

Input: trips = [[2,1,3],[3,2,4]], capacity = 4

Output: false
Constraints:

1 <= trips.length <= 1000
trips[i].length == 3
1 <= numPassengers[i] <= 100
0 <= from[i] < to[i] <= 1000
1 <= capacity <= 100,000

'''
from sortedcontainers import SortedDict

class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        events = SortedDict()

        for c, i, j in trips:
            if i not in events:
                events[i] = 0

            if j not in events:
                events[j] = 0

            events[i] += c
            events[j] -= c

        curr = 0
        for x in events:
            delta = events[x]

            curr += delta

            if curr > capacity:
                return False

        return True
