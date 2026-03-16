'''
There are n rooms numbered from 0 to n - 1. You are given a 2D integer array meetings where meetings[i] = [start[i], end[i]] means that a meeting will be held during the half-closed time interval [start[i], end[i]). All the values of start[i] are unique.

Meetings are allocated to rooms in the following manner:

Each meeting will take place in the unused room with the lowest number.
If there are no available rooms, the meeting will be delayed until a room becomes free. The delayed meeting should have the same duration as the original meeting.
When a room becomes unused, meetings that have an earlier original start time should be given the room.
Return the number of the room that held the most meetings. If there are multiple rooms, return the room with the lowest number.

A half-closed interval [a, b) is the interval between a and b including a and not including b.

Example 1:

Input: n = 2, meetings = [[1,10],[2,10],[3,10],[4,10]]

Output: 0
Explanation:

At time 1, the room with number 0 is available, the first meeting is allocated to it.
At time 2, the room with number 1 is available, the second meeting is allocated to it.
At time 10, the rooms with numbers 0 and 1 becomes unused, the third meeting is allocated to room number 0 and fourth meeting is allocated to room number 1.
The room with most meetings held and have lowest number is 0.

Example 2:

Input: n = 3, meetings = [[1,20],[2,10],[3,5],[6,8],[4,9]]

Output: 1
Explanation:

At time 1, all three rooms are not being used. The first meeting starts in room 0.
At time 2, rooms 1 and 2 are not being used. The second meeting starts in room 1.
At time 3, only room 2 is not being used. The third meeting starts in room 2.
At time 4, all three rooms are being used. The fourth meeting is delayed.
At time 5, the meeting in room 2 finishes. The fourth meeting starts in room 2 for the time period [5,10).
At time 6, all three rooms are being used. The fifth meeting is delayed.
At time 10, the meetings in rooms 1 and 2 finish. The fifth meeting starts in room 1 for the time period [10,12).
Room 0 held 1 meeting while rooms 1 and 2 each held 2 meetings, so we return 1 as it is lowest.

Constraints:

1 <= n <= 100
1 <= meetings.length <= 100,000
meetings[i].length == 2
0 <= start[i] < end[i] <= 500,000
All the values of start[i] are unique.

'''

from collections import *
from heapq import *

class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        if len(meetings) == 1:
            return 0

        meetings.sort()

        usage = [0] * n
        in_use = []
        available = list(range(n))

        for s, e in meetings:
            t = s
            # print("\n" + "_"* 70)
            # print(f"@{t=} | {s=} {e=} | {usage=} | {in_use=} | {available=}")

            # anything which finished add it back to available pool
            while in_use and in_use[0][0] <= t:
                _, ind = heappop(in_use)
                heappush(available, ind)
            # print(f"after adding finished | {in_use=} | {available=}")

            if available:
                room_ind = heappop(available)
                usage[room_ind] += 1
                heappush(in_use, (e, room_ind))
                # print(f"{room_ind} was available | {usage=} | in use till {e} => {in_use=}")
            else:
                # get the earliest room which finishes
                earliest_end, room_ind = heappop(in_use)
                new_end = earliest_end + e - s
                usage[room_ind] += 1
                heappush(in_use, (new_end, room_ind))
                # print(f"nothing available | {room_ind} was available at {earliest_end} => {new_end=} | {usage=} | {in_use=}")

        # find max
        # print(f"{usage=}")
        res = 0
        for i in range(1, n):
            if usage[i] > usage[res]:
                res = i

        return res
