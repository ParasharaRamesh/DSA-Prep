'''
There are n cars traveling to the same destination on a one-lane highway.

You are given two arrays of integers position and speed, both of length n.

position[i] is the position of the ith car (in miles)
speed[i] is the speed of the ith car (in miles per hour)
The destination is at position target miles.

A car can not pass another car ahead of it. It can only catch up to another car and then drive at the same speed as the car ahead of it.

A car fleet is a non-empty set of cars driving at the same position and same speed. A single car is also considered a car fleet.

If a car catches up to a car fleet the moment the fleet reaches the destination, then the car is considered to be part of the fleet.

Return the number of different car fleets that will arrive at the destination.

Example 1:

Input: target = 10, position = [1,4], speed = [3,2]

Output: 1
Explanation: The cars starting at 1 (speed 3) and 4 (speed 2) become a fleet, meeting each other at 10, the destination.

Example 2:

Input: target = 10, position = [4,1,0,7], speed = [2,2,1,1]

Output: 3
Explanation: The cars starting at 4 and 7 become a fleet at position 10. The cars starting at 1 and 0 never catch up to the car ahead of them. Thus, there are 3 car fleets that will arrive at the destination.

Constraints:

n == position.length == speed.length.
1 <= n <= 1000
0 < target <= 1000
0 < speed[i] <= 100
0 <= position[i] < target
All the values of position are unique.

Insights:

. when visualizing the cars in position only a car from behind can come and join a car ahead and become a fleet => sort position in descending order first
. have a stack of times and keep adding the times to it
. if stack[-1] >= time of curr car => the car ahead is taking a lot longer no of steps to reach the target and the car behind just needs fewer number of steps to reach target so it can pretty quickly join it
    - the moment you join just keep the earlier time in the stack as that is the # of time taken by the slowest car in the fleet
. if stack[-1] < time => the car ahead reaches the target sooner than the cars behind so can treat it as seperate fleets.

'''

from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        xv = list(zip(position, speed))
        xv.sort(reverse=True, key=lambda x: x[0]) # sort on descending position

        fleets = 0
        time_stack = []
        for x,v in xv:
            t = (target - x) / v

            if not time_stack:
                time_stack.append(t)
            elif time_stack[-1] >= t:
                continue # do nothing as the new car will join this fleet.
            else:
                time_stack.clear()
                time_stack.append(t)
                fleets += 1

        if len(time_stack) > 0:
            fleets += 1

        return fleets


if __name__ == '__main__':
    s = Solution()


    target = 10
    position = [0,4,2]
    speed = [2,1,3]
    res = s.carFleet(target, position, speed)
    print(res, res == 1)

    target = 12
    position = [10,8,0,5,3]
    speed = [2,4,1,1,3]
    res = s.carFleet(target, position, speed)
    print(res, res == 3)

    target = 100
    position = [0,2,4]
    speed = [4,2,1]
    res = s.carFleet(target, position, speed)
    print(res, res == 1)

    target = 10
    position = [1,4]
    speed = [3,2]
    res = s.carFleet(target, position, speed)
    print(res, res == 1)

    target = 10
    position = [4,1,0,7]
    speed = [2,2,1,1]
    res = s.carFleet(target, position, speed)
    print(res, res == 3)