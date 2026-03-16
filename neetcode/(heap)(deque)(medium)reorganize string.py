'''
You are given a string s, rearrange the characters of s so that any two adjacent characters are not the same.

You can return any possible rearrangement of s or return "" if not posssible.

Example 1:

Input: s = "axyy"

Output: "xyay"
Example 2:

Input: s = "abbccdd"

Output: "abcdbcd"
Example 3:

Input: s = "ccccd"

Output: ""
Constraints:

1 <= s.length <= 500.
s is made up of lowercase English characters.

'''
from collections import *
from heapq import *

class Solution:
    def reorganizeString(self, s: str) -> str:
        cnts = Counter(s)
        pending = deque([])

        heap = []

        for c, cnt in cnts.items():
            heappush(heap, (-cnt, c))


        res = ""
        t = 0

        # print(f"max {heap=}")

        while heap or pending:
            # print("\n" + "_" * 60)
            # print(f"{res=} {t=} | checking pending..")
            while pending and pending[0][0] < t - 1:
                p_t, p_cnt, p_c = pending.popleft()
                heappush(heap, (-p_cnt, p_c))
                # print(f"pushed to max heap -> {(-p_cnt, p_c)}")
            # print(f"after pending | {pending=} max {heap=}")

            if heap:
                cnt, c = heappop(heap)
                cnt *= -1

                # print(f"heappopped {(cnt, c)}")
                
                if len(res) > 0 and res[-1] == c:
                    # print(f"impossible")
                    return ""

                res += c
                # print(f"added {c} -> {res=}")

                if cnt - 1 > 0:
                    item = (t, cnt-1, c)
                    # print(f"enQ {item=} to pending")
                    pending.append(item)
            else:
                # add everything to the heap again
                while pending:
                    p_t, p_cnt, p_c = pending.popleft()
                    if p_t >= t - 1:
                        # print(f"impossible 2")
                        return ""

                    heappush(heap, (-p_cnt, p_c))
                    # print(f"2.pushed to max heap -> {(-p_cnt, p_c)}")

            t += 1

        return res



        
