'''
3651. Minimum Cost Path with Teleportations

You are given a m x n 2D integer array grid and an integer k. You start at the top-left cell (0, 0) and your goal is to reach the bottom‐right cell (m - 1, n - 1).

There are two types of moves available:

Normal move: You can move right or down from your current cell (i, j), i.e. you can move to (i, j + 1) (right) or (i + 1, j) (down). The cost is the value of the destination cell.

Teleportation: You can teleport from any cell (i, j), to any cell (x, y) such that grid[x][y] <= grid[i][j]; the cost of this move is 0. You may teleport at most k times.

Return the minimum total cost to reach cell (m - 1, n - 1) from (0, 0).

 

Example 1:

Input: grid = [[1,3,3],[2,5,4],[4,3,5]], k = 2

Output: 7

Explanation:

Initially we are at (0, 0) and cost is 0.

Current Position	Move	New Position	Total Cost
(0, 0)	Move Down	(1, 0)	0 + 2 = 2
(1, 0)	Move Right	(1, 1)	2 + 5 = 7
(1, 1)	Teleport to (2, 2)	(2, 2)	7 + 0 = 7
The minimum cost to reach bottom-right cell is 7.

Example 2:

Input: grid = [[1,2],[2,3],[3,4]], k = 1

Output: 9

Explanation:

Initially we are at (0, 0) and cost is 0.

Current Position	Move	New Position	Total Cost
(0, 0)	Move Down	(1, 0)	0 + 2 = 2
(1, 0)	Move Right	(1, 1)	2 + 3 = 5
(1, 1)	Move Down	(2, 1)	5 + 4 = 9
The minimum cost to reach bottom-right cell is 9.

 
Constraints:

2 <= m, n <= 80
m == grid.length
n == grid[i].length
0 <= grid[i][j] <= 10^4
0 <= k <= 10

'''
from typing import List
from sortedcontainers import SortedDict
from collections import defaultdict
from heapq import *
from bisect import *
from functools import lru_cache

class Item:
    def __init__(self, val, loc, is_teleport=False):
        self.val = val
        self.loc = loc
        self.is_teleport = is_teleport

    def __repr__(self):
        return f"Item(loc={self.loc}, val={self.val}, is_teleport={self.is_teleport})"

class Solution:
    def minCost_tle_multihop_dijstra(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])

        graph = defaultdict(list)
        values_to_cells = SortedDict()

        is_valid_loc = lambda x, y: 0 <= x < m and 0 <= y < n

        # populate graph with simple edges and values to cells
        for i in range(m):
            for j in range(n):
                loc = (i, j)

                # add known edge costs
                graph[loc] = []
                if is_valid_loc(i, j + 1):
                    graph[loc].append(
                        Item(grid[i][j+1], (i, j + 1))
                    )

                if is_valid_loc(i + 1, j):
                    graph[loc].append(
                        Item(grid[i + 1][j], (i + 1, j))
                    )

                # add values ( will help in finding out those cells which are teleportaions)
                val = grid[i][j]

                if val not in values_to_cells:
                    values_to_cells[val] = [
                        Item(0, loc, True)
                    ]
                else:
                    values_to_cells[val].append(Item(0, loc, True))


        # for each key in graph find out the values using bisect_left  of the keys lesser than it and just extend that list
        values = list(values_to_cells.keys())

        for loc in graph:
            x, y = loc
            val = grid[x][y]

            ind = values_to_cells.bisect_left(val)
            if values[ind] == val:
                candidate_values = values[:ind+1]
            else:
                candidate_values = values[:ind]

            for candidate_value in candidate_values:
                items = values_to_cells[candidate_value]

                # filter out same loc in case it is present
                items = list(
                    filter(
                        lambda item: item.loc != loc,  
                        items
                    )
                )
                graph[loc].extend(items)

        # multihop dijstra
        shortest = dict()
        finalized = set()

        # populate states as inf
        for i in range(m):
            for j in range(n):
                for K in range(k+1):
                    shortest[(i, j, K)] = float("inf")

        pq = [(0, (0, 0, 0))] # val, (i, j, k) -> where k is num of teleportations
        while pq:
            val, (i, j, teleports) = heappop(pq)

            if teleports > k:
                continue

            if (i, j, teleports) in finalized:
                continue
            
            finalized.add((i, j, teleports))

            # not necessary we keep improving it anyways
            # shortest[(i, j, k)] = val

            for neighbour in graph[(i, j)]:
                is_teleport = neighbour.is_teleport
                I, J = neighbour.loc
                cost = neighbour.val
                new_teleports = teleports if not is_teleport else teleports + 1

                is_within_k = new_teleports <= k
                is_node_same_as_prev = (I, J) == (i, j)

                state = (I, J, new_teleports)

                if not is_node_same_as_prev and is_within_k and state not in finalized and val + cost <= shortest[state]:
                    shortest[state] = val + cost
                    heappush(pq, (val+cost, state))

        # amongst all the m-1, n-1, 0=>k what is the smallest?
        min_cost = float("inf")
        for K in range(k + 1):
            min_cost = min(min_cost, shortest[(m-1,n-1,K)])

        return min_cost

    def minCost_tle_memo(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        
        # We need to quickly find the best cell to teleport to.
        # This helper will find the min cost of any cell (nr, nc) 
        # in the NEXT layer where grid[nr][nc] <= threshold.
        @lru_cache(None)
        def get_best_teleport_target(threshold, k_rem):
            res = float('inf')
            for r in range(m):
                for c in range(n):
                    if grid[r][c] <= threshold:
                        res = min(res, solve(r, c, k_rem))
            return res

        @lru_cache(None)
        def solve(r, c, k_rem):
            # Base Case: Reached the destination
            if r == m - 1 and c == n - 1:
                return 0
            
            res = float('inf')
            
            # 1. Normal Move Right
            if c + 1 < n:
                res = min(res, grid[r][c+1] + solve(r, c+1, k_rem))
                
            # 2. Normal Move Down
            if r + 1 < m:
                res = min(res, grid[r+1][c] + solve(r+1, c, k_rem))
                
            # 3. Teleport (Anywhere with value <= current cell)
            if k_rem > 0:
                # Instead of looping here (which is slow), we call our helper
                res = min(res, get_best_teleport_target(grid[r][c], k_rem - 1))
                
            return res

        return solve(0, 0, k)

    # just doing binary search to get the best teleport target
    def minCost_tle_memo_2(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        inf = float('inf')

        # 1. Build your values_to_cells map first
        # We'll use a sorted list of unique values for binary searching the threshold
        val_map = SortedDict()
        for r in range(m):
            for c in range(n):
                val = grid[r][c]
                if val not in val_map:
                    val_map[val] = []
                val_map[val].append((r, c))
        
        sorted_unique_values = list(val_map.keys())

        @lru_cache(None)
        def get_best_teleport_target(threshold, k_rem):
            """
            Finds the best cell to jump to where grid[nr][nc] <= threshold
            using the locations stored in our val_map.
            """
            best = inf

            # Find all keys in our map that are <= threshold using binary search
            idx = val_map.bisect_right(threshold)
            valid_keys = sorted_unique_values[:idx]
            
            for v in valid_keys:
                for nr, nc in val_map[v]:
                    # Recurse: what is the cost starting from this new location?
                    res = solve(nr, nc, k_rem)
                    if res != inf:
                        best = min(best, res)
            return best

        @lru_cache(None)
        def solve(r, c, k_rem):
            # Base Case: We reached the bottom-right
            if r == m - 1 and c == n - 1:
                return 0
            
            res = inf
            
            # 1. Normal Move: Right
            if c + 1 < n:
                res = min(res, grid[r][c+1] + solve(r, c+1, k_rem))
                
            # 2. Normal Move: Down
            if r + 1 < m:
                res = min(res, grid[r+1][c] + solve(r+1, c, k_rem))
                
            # 3. Teleport Move: Jump to any (nr, nc) where grid[nr][nc] <= grid[r][c]
            if k_rem > 0:
                # We use the helper to find the best possible jump destination
                teleport_cost = get_best_teleport_target(grid[r][c], k_rem - 1)
                res = min(res, teleport_cost)
                
            return res

        result = solve(0, 0, k)
        return result if result != inf else -1

    # Much better optimized dijstra
    def minCost_optiomal_dijstra(self, grid: List[List[int]], max_teleports: int) -> int:
        rows, cols = len(grid), len(grid[0])
        INF = float('inf')

        '''
        1. THE STATE: (cost, r, c, teleports_used)
        We treat the grid like a multi-story building. 
        Floor 0: 0 teleports used.
        Floor 1: 1 teleport used.
        ... and so on. 
        
        To reach the goal, we can be on ANY floor at the bottom-right cell.
        '''
        best_costs = [[[INF] * (max_teleports + 1) for _ in range(cols)] for _ in range(rows)]
        best_costs[0][0][0] = 0

        # Priority Queue: (cost_so_far, current_row, current_col, teleports_already_used)
        priority_queue = [(0, 0, 0, 0)]

        '''
        2. THE TELEPORT TARGETS:
        We sort every cell in the grid by its value. 
        Why? Because when we are at a cell with value X, we only care about 
        jumping to cells with value <= X. A sorted list lets us find these easily.
        '''
        all_cells_sorted_by_val = []
        for r in range(rows):
            for c in range(cols):
                all_cells_sorted_by_val.append((grid[r][c], r, c))
        all_cells_sorted_by_val.sort()

        '''
        3. THE PROGRESS POINTERS:
        This is the most important part. We have a pointer for EACH teleport level.
        teleport_pointers[0] = how many cells we've already "activated" for the 1st jump.
        teleport_pointers[1] = how many cells we've already "activated" for the 2nd jump.
        
        Example: If we already teleported to Cell (2,2) using our 1st jump, we 
        recorded that with the cheapest possible cost. No need to ever "jump" 
        to (2,2) using the 1st jump ever again.
        '''
        teleport_pointers = [0] * max_teleports

        while priority_queue:
            current_cost, r, c, used_t = heappop(priority_queue)

            # Standard Dijkstra check: if we found a better path to this state already, skip.
            if current_cost > best_costs[r][c][used_t]:
                continue

            # Since Dijkstra pops the smallest cost first, the first time we 
            # see the target cell (at any teleport level), it's the winner.
            if r == rows - 1 and c == cols - 1:
                return current_cost

            '''
            4. OPTION A: WALK (Standard Dijkstra)
            We move to adjacent cells. This costs the value of the destination cell.
            This doesn't use up any teleport "budget".
            '''
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_cost = current_cost + grid[nr][nc]
                    if new_cost < best_costs[nr][nc][used_t]:
                        best_costs[nr][nc][used_t] = new_cost
                        heappush(priority_queue, (new_cost, nr, nc, used_t))

            '''
            5. OPTION B: TELEPORT (The Optimized Part)
            If we have a teleport left, we want to jump to cells <= our current value.
            '''
            if used_t < max_teleports:
                # We look at the pointer for the NEXT teleport level
                ptr = teleport_pointers[used_t]
                
                '''
                EXAMPLE:
                Current Cell Value: 10
                Sorted List: [ (val:2), (val:5), (val:8), (val:12), (val:15) ]
                Pointer starts at 0.
                
                We see 2, 5, and 8 are all <= 10. 
                We push them to the heap and move the pointer to index 3.
                
                Next time we arrive at a cell with Value 11, the pointer is ALREADY at 3.
                We only check from index 3 onwards (the value 12).
                We skip 2, 5, and 8 because they were already handled by someone CHEAPER.

                AS LONG AS it was in the same hop level (used_t)
                '''
                while ptr < len(all_cells_sorted_by_val) and all_cells_sorted_by_val[ptr][0] <= grid[r][c]:
                    target_val, target_r, target_c = all_cells_sorted_by_val[ptr]
                    
                    # Target teleport level will be used_t + 1
                    if current_cost < best_costs[target_r][target_c][used_t + 1]:
                        best_costs[target_r][target_c][used_t + 1] = current_cost
                        heappush(priority_queue, (current_cost, target_r, target_c, used_t + 1))
                    
                    ptr += 1
                
                # Save the progress for this teleport level!
                teleport_pointers[used_t] = ptr

        return -1

    def minCost_optimal_dp(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        INF = float('inf')

        '''
        FIRST PRINCIPLE: THE CHEAT SHEET (teleport_lookup)
        A teleport jump is "Location-Blind." You can jump to ANY cell on the map
        as long as its value is <= your current cell's value. 
        
        Because distance doesn't matter, we don't need to check 6,400 cells. 
        We only care about the single "Bestest Winner" cell in the allowed value range.
        
        teleport_lookup[t][V] answers: "If I have t hops left, what is the 
        cheapest way to reach the end if I jump to ANY cell with value <= V?"
        '''
        teleport_lookup = [{} for _ in range(k + 1)]

        @lru_cache(None)
        def solve(r, c, t):
            '''
            CORE RECURSION: solve(r, c, t)
            Intuition: "I am at (r, c) with t teleports left. What is the 
            minimum cost to get to the finish line from here?"
            '''
            # BASE CASE: We are standing on the destination. Cost is 0.
            if r == m - 1 and c == n - 1:
                return 0
            
            res = INF
            
            # OPTION 1: THE WALK (Right/Down)
            # You pay the cost of the cell you ENTER.
            if c + 1 < n:
                res = min(res, grid[r][c+1] + solve(r, c+1, t))
            if r + 1 < m:
                res = min(res, grid[r+1][c] + solve(r+1, c, t))
            
            # OPTION 2: THE TELEPORT
            # Rule: Jump to any cell where target_val <= current_val.
            # Instead of searching the whole grid (O(N^2)), we do a O(1) lookup.
            if t > 0:
                current_val = grid[r][c]
                # "Cheat Sheet" tells us the best possible solve() result 
                # among all valid target cells for this value.
                if current_val in teleport_lookup[t-1]:
                    res = min(res, teleport_lookup[t-1][current_val])
                    
            return res

        '''
        THE LAYERING ENGINE
        Why a loop? Because solve(..., t) depends on the results of solve(..., t-1).
        We calculate the floors of our "building" one by one (0 hops, then 1, then 2).
        '''
        for current_t in range(k + 1):
            
            '''
            STEP A: PRIMING THE CACHE
            Recursion is "lazy." If we don't force it to calculate the cells,
            the Cheat Sheet below will be empty. We iterate backwards (end to start)
            to help the recursion flow naturally towards the base case.
            '''
            for r in range(m - 1, -1, -1):
                for c in range(n - 1, -1, -1):
                    solve(r, c, current_t)
            
            '''
            STEP B: FINDING LOCAL CHAMPIONS (val_to_best_solve)
            DOUBT CLEARED: "Why group by value?"
            Because if 10 different cells have Value=5, we only care about the ONE 
            cell that is closest to the exit. The others are redundant for teleports.
            '''
            val_to_best_solve = {}
            for r in range(m):
                for c in range(n):
                    s_val = solve(r, c, current_t)
                    if s_val != INF:
                        v = grid[r][c]
                        # Track the "Winner" for this specific value
                        val_to_best_solve[v] = min(val_to_best_solve.get(v, INF), s_val)
            
            '''
            STEP C: THE "BESTEST" WINNER (Running Best / Suffix Min)
            DOUBT CLEARED: "Why running best?"
            If your limit is Value 10, you can jump to a Value 10 cell (Cost 100) 
            OR a Value 5 cell (Cost 40). 
            We need the 'Bestest' result in the range [0...10].
            '''
            # Get all unique values actually present in the grid
            all_grid_vals = sorted(list(set(val for row in grid for val in row)))
            
            running_best = INF
            for v in all_grid_vals:
                # If we found a local champion for this value, check if they are the 
                # new overall champion for the current range.
                if v in val_to_best_solve:
                    running_best = min(running_best, val_to_best_solve[v])
                
                # FILLING GAPS: Every grid value gets the 'Bestest' result seen so far.
                # This ensures any grid[r][c] can find its O(1) answer in the next layer.
                teleport_lookup[current_t][v] = running_best

        # FINAL CALL: The journey starts at (0,0) with the full budget of k hops.
        result = solve(0, 0, k)
        return result if result != INF else -1

if __name__ == "__main__":
    sol = Solution()

    k = 2
    grid = [[1,3,3],[2,5,4],[4,3,5]]
    expected = 7
    ans = sol.minCost(grid, k)
    assert ans == expected, f"Expected {expected}, got {ans}"

    k = 1
    grid = [[1,2],[2,3],[3,4]]
    expected = 9
    ans = sol.minCost(grid, k)
    assert ans == expected, f"Expected {expected}, got {ans}"

    k = 4
    grid = [[8,6,10],[6,12,14]]
    expected = 24
    ans = sol.minCost(grid, k)
    assert ans == expected, f"Expected {expected}, got {ans}"