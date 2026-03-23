'''
You are given a 0-indexed binary string s and two integers minJump and maxJump. In the beginning, you are standing at index 0, which is equal to '0'. You can move from index i to index j if the following conditions are fulfilled:

i + minJump <= j <= min(i + maxJump, s.length - 1), and
s[j] == '0'.
Return true if you can reach index s.length - 1 in s, or false otherwise.

 

Example 1:

Input: s = "011010", minJump = 2, maxJump = 3
Output: true
Explanation:
In the first step, move from index 0 to index 3. 
In the second step, move from index 3 to index 5.

Example 2:

Input: s = "01101110", minJump = 2, maxJump = 3
Output: false
 

Constraints:

2 <= s.length <= 105
s[i] is either '0' or '1'.
s[0] == '0'
1 <= minJump <= maxJump < s.length

'''

from bisect import *
from collections import *
from functools import cache

class Solution:
    '''
    . Similar to jump game ii, I track the reachability
    . Initially I had tried with just one variable but then quickly realized I need to keep track of both min_reachability and max_reachability
    . I then set the i index to the min_reach
    . Setting to min_reach gave tle so I made a subtle optimization ( WHICH EVENTUALLY TURNED OUT TO BE WRONG! )
        - instead of naively setting it to min_reach I wanted to set i to such an index j E [i + minjump , i + maxjump] such that when attempting to do a min jump from j it would be out of the reach of this range
        - went through each reachable index in reverse and tried picking the first index which could jump out of this range
        - but that idea was wrong with one of the test cases 
    . Therefore the only best thing which can be done in this case is to set it to the min_reach index which makes things very slow
    . Time complexity: O(n^2)
      Explanation: for each current `i`, the code scans all indices in `[i + minJump, min(i + maxJump, n-1)]` to compute `min_reach`/`max_reach`; in the worst case that scan is O(n) and the outer loop can run O(n) times.
    . Space complexity: O(1)
      Explanation: it only uses a constant number of variables (`i`, bounds, and min/max reach) and does not store extra arrays/lists proportional to `n`.
    '''
    def canReach_tle_simulation(self, s: str, minJump: int, maxJump: int) -> bool:
        if s[-1] != "0":
            # trivial case as landing should always be zero
            return False

        n = len(s)
        i = 0

        while i < n and s[i] == "0":
            l = i + minJump
            if l >= n:
                # cannot go beyond this
                break
            
            r = min(i + maxJump, n - 1)

            min_reach = float("inf") 
            max_reach = float("-inf")

            for j in range(l, r+1):
                if s[j] == "0":
                    min_reach = min(min_reach, j)
                    max_reach = max(max_reach, j) 
                    
            # print(f"from {i=} | check {l} -> {r} | {min_reach=} {max_reach=}")

            if min_reach == float("inf") and max_reach == float("-inf"):
                # print(f"min reach still has not changed! breaking")
                break

            if min_reach <= n - 1 <= max_reach:
                # print(f"reachable as {n-1} is within {min_reach=} {max_reach=}")
                return True

            i = min_reach
            # print(f"setting i to {min_reach}")

        return False


    '''
    . Dynamic programming approach
    . consider all zeros reachable when jumping min and max jump and go down the recursion path while caching to see if it is possible
    . Time complexity: O(n^2)
      Explanation: memoization ensures each `f(i)` is computed once, but each computation still iterates across the full jump interval to build `reach`, which can sum to O(n^2) in the worst case.
    . Space complexity: O(n)
      Explanation: `@cache` stores results for up to `n` indices; recursion depth can also reach O(n).
    '''
    def canReach_memoization_mle(self, s: str, minJump: int, maxJump: int) -> bool:
        if s[-1] != "0":
            # trivial case as landing should always be zero
            return False

        n = len(s)

        @cache
        def f(i):
            if i == n - 1:
                return True

            if i >= n:
                return False

            if s[i] == "1":
                return False
            
            l = i + minJump
            if l >= n:
                # cannot go beyond this
                print(f"min jump from {i} becomes {l}. Breaking!")
                return False
            
            r = min(i + maxJump, n - 1)
            if r == n - 1:
                print(f" directly reachable")
                return True


            reach = []
            for j in range(l, r+1):
                if s[j] == "0":
                    reach.append(j)

            if not reach:
                return False

            if reach[0] <= n - 1 <= reach[-1]:
                return True

            for k in reach:
                if f(k):
                    return True

            return False

        return f(0)


    '''
    . Same approach as above just that it is tabulation since the recursion limit exceeded in the top down dp approach
    . Time complexity: O(n^2)
      Explanation: for each `i` it scans `[i + minJump, min(i + maxJump, n-1)]` to build `reach`, and may then scan `reach` again until it finds a reachable cached state; worst-case total work is O(n^2).
    . Space complexity: O(n)
      Explanation: `cache` stores one boolean per index (O(n)); `reach` is temporary inside the loop iteration.
    '''
    def canReach_tabulation_tle(self, s: str, minJump: int, maxJump: int) -> bool:
        if s[-1] != "0":
            # trivial case as landing should always be zero
            return False

        n = len(s)

        cache = defaultdict(bool)
        cache[n-1] = True

        for i in range(n-2, -1, -1):
            if s[i] == "1":
                cache[i] = False
                continue

            l = i + minJump
            if l >= n:
                cache[i] = False
                continue
            
            r = min(i + maxJump, n - 1)
            if r == n - 1:
                cache[i] = True
                continue

            reach = []
            for j in range(l, r+1):
                if s[j] == "0":
                    reach.append(j)

            if not reach:
                cache[i] = False
                continue

            if reach[0] <= n - 1 <= reach[-1]:
                cache[i] = True
                continue

            flag = False
            for k in reach:
                if cache[k]:
                    cache[i] = True
                    flag = True
                    break
                    
            if flag:
                continue

            cache[i] = False

        return cache[0] 

    '''
    . Since we can only jump from indices where the char is 0, that forms an edge of sorts
    . We construct this jump graph and then perform bfs on it
    . we first keep track of all of the zeros and then get the l and r range using bisect
    . This gave memory limit exceeded because of the size of the graph and the visited set
    . Time complexity: O(n^2)
      Explanation: in the worst case there are O(n) zero indices, and each zero can have edges to O(n) other zero indices within `[minJump, maxJump]`, making graph construction and BFS traverse O(V+E)=O(n^2).
    . Space complexity: O(n^2)
      Explanation: `graph` stores adjacency lists for all those edges, so memory is dominated by O(n^2) stored connections (which leads to MLE).

    '''
    def canReach_mle_bfs(self, s: str, minJump: int, maxJump: int) -> bool:
        if s[-1] != "0":
            return False

        n = len(s)

        # get all indices of 0s 
        zeros = []
        for i in range(n):
            if s[i] == '0':
                zeros.append(i)
        
        num_zeros = len(zeros)

        # construct the graph
        graph = defaultdict(list)

        for i in zeros:
            l = bisect_left(zeros, i + minJump)
            r = bisect_right(zeros, i + maxJump)
            connections = zeros[l:r]
            graph[i].extend(connections)

        # run bfs on the graph
        frontier = deque([0])
        visited = set()
        visited.add(0)

        while frontier:
            node = frontier.popleft()

            for neigh in graph[node]:
                if neigh not in visited:
                    if neigh == n-1:
                        return True
                        
                    visited.add(neigh)
                    frontier.append(neigh)

        return False

    '''
    Best solution which works on leetcode without MLE or TLE

    . similar to the bfs approach above just that we dont explicitly construct the graph
    . we construct it along the way without keeping track of visited
    . for a range of [start, end] -> add to the deque whichever ones are 0s
    . along the way check if we reach the ending
    . Time complexity: O(n)
      Explanation: `farthest` only increases; `start = max(i + minJump, farthest + 1)` ensures indices already covered by previous popped nodes are not re-scanned. Thus, each index is considered at most once overall.
    . Space complexity: O(n)
      Explanation: the deque can store up to O(n) indices in the worst case (all reachable zeros), and the rest is O(1) auxiliary space.
    ''' 
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        q = deque([0])
        farthest = 0

        while q:
            i = q.popleft()
            start = max(i + minJump, farthest + 1)
            end = min(i + maxJump, len(s)-1)

            for j in range(start, end + 1):
                if s[j] == "0":
                    q.append(j)
                    if j == len(s) - 1:
                        return True
            farthest = end

        return False