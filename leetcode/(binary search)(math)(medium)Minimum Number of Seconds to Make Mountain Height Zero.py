'''
Leetcode 3296

You are given an integer mountainHeight denoting the height of a mountain.

You are also given an integer array workerTimes representing the work time of workers in seconds.

The workers work simultaneously to reduce the height of the mountain. For worker i:

To decrease the mountain's height by x, it takes workerTimes[i] + workerTimes[i] * 2 + ... + workerTimes[i] * x seconds. For example:
To reduce the height of the mountain by 1, it takes workerTimes[i] seconds.
To reduce the height of the mountain by 2, it takes workerTimes[i] + workerTimes[i] * 2 seconds, and so on.
Return an integer representing the minimum number of seconds required for the workers to make the height of the mountain 0.



Example 1:

Input: mountainHeight = 4, workerTimes = [2,1,1]

Output: 3

Explanation:

One way the height of the mountain can be reduced to 0 is:

Worker 0 reduces the height by 1, taking workerTimes[0] = 2 seconds.
Worker 1 reduces the height by 2, taking workerTimes[1] + workerTimes[1] * 2 = 3 seconds.
Worker 2 reduces the height by 1, taking workerTimes[2] = 1 second.
Since they work simultaneously, the minimum time needed is max(2, 3, 1) = 3 seconds.

Example 2:

Input: mountainHeight = 10, workerTimes = [3,2,2,4]

Output: 12

Explanation:

Worker 0 reduces the height by 2, taking workerTimes[0] + workerTimes[0] * 2 = 9 seconds.
Worker 1 reduces the height by 3, taking workerTimes[1] + workerTimes[1] * 2 + workerTimes[1] * 3 = 12 seconds.
Worker 2 reduces the height by 3, taking workerTimes[2] + workerTimes[2] * 2 + workerTimes[2] * 3 = 12 seconds.
Worker 3 reduces the height by 2, taking workerTimes[3] + workerTimes[3] * 2 = 12 seconds.
The number of seconds needed is max(9, 12, 12, 12) = 12 seconds.

Example 3:

Input: mountainHeight = 5, workerTimes = [1]

Output: 15

Explanation:

There is only one worker in this example, so the answer is workerTimes[0] + workerTimes[0] * 2 + workerTimes[0] * 3 + workerTimes[0] * 4 + workerTimes[0] * 5 = 15.



Constraints:

1 <= mountainHeight <= 105
1 <= workerTimes.length <= 104
1 <= workerTimes[i] <= 106
'''

'''
Insights:

. Initial attempt was way off in that I was trying to do it in a greedy way where I assigned everyone equal height and then distributed the delta equally to the lower worker times. Failed because it was not a linear relation but an inverse relationship
. Then I tried an inverse approach where i assumed that ti * hi = k but that worked in lots of cases but failed bedcause actually ti * hi^2 = k 
. Then I tried that approach where I try to mathematically find that constant k but then it was not trivial on how to round the heights to the correct integers such that it maintained two constranits where sum of heights is maintained and the total time is minimized
. Then i saw the hint of doing binary search in answer space:

if total time is T
for worker i:
ti * hi * (hi + 1) / 2 <= T
ti * hi^2 + ti * hi - 2T <= 0

hi = (-ti + sqrt(ti^2 + 8T ti))/2ti

which means hi' = (-1 + sqrt(1 + (8*T/ti)))//2

. We can now do binary search in answer space by assuming that l = 0 and r = time if the fastest worker does all the work
now we can check if sigma(hi) >= mountainHeight -> that time T is the answer but we can try to check lower also r = T - 1
if sigma(hi) < mountainHeight -> l = T + 1

'''
class Solution:
    def minNumberOfSeconds(self, mountainHeight: int, workerTimes: List[int]) -> int:
        def possible_height_sum(T):
            total = 0

            for t in workerTimes:
                h = int((-1 + (1 + 8*T/t) ** 0.5) // 2)
                total += h
            return total


        l = 0
        r = min(workerTimes) * mountainHeight * (mountainHeight + 1) // 2

        T = float("inf")

        while l <= r:
            t = (l + r)//2

            H = possible_height_sum(t)

            if mountainHeight <= H:
                T = min(t, T)
                r = t - 1
            else:
                l = t + 1
             

        return T
