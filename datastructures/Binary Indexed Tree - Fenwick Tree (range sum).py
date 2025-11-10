'''
Binary Indexed Tree (Fenwick Tree) — Range Sum Queries with Point Updates
-----------------------------------------------------------------------

What it is:
- A compact data structure that maintains partial prefix aggregates so we can:
  - Get prefix sums in O(log N)
  - Apply point updates in O(log N)
- Typically implemented with 1-based indexing. `BIT[0]` is unused.

When to use:
- You need fast prefix queries plus point updates (e.g., sums, products).
- The operation is invertible/has a group-like structure so that:
  range(l, r) = prefix(r) - prefix(l - 1)   (for sums)
- Good for streaming updates, online queries, and memory efficiency.

Why it works (intuition):
- Each index `i` in `BIT` stores an aggregate for a range whose length equals
  the value of its least significant set bit (LSSB). This partitions the array
  into canonical, power-of-two-sized blocks.
- By “jumping” across these blocks via bit tricks, both queries and updates
  touch only O(log N) blocks.

Key bit tricks (for any positive integer x):
- `x & -x`  => extracts the least significant set bit (LSSB).
- `x - (x & -x)`  => removes the LSSB (equivalent to `x & (x - 1)`).

What `BIT[i]` stores:
- `BIT[i]` holds the aggregate (e.g., sum) over the range `(i - (i & -i) + 1) .. i`.
    * i.e. the range from i (without the LSSB) to i
- Equivalently, if `j = i & (i - 1)`, then `BIT[i]` covers `(j + 1) .. i`.

How query works (prefix sum up to i):
- Repeatedly add `BIT[i]` to the answer and strip off the LSSB from `i`:
  i = i - (i & -i)
- This walks over O(log N) disjoint blocks that exactly cover `[1 .. i]`.

How update works (add val at index i):
- Repeatedly add `val` to `BIT[i]` and move to the next index that includes `i`
  in its stored range:
  i = i + (i & -i)
- This climbs to O(log N) supersets that must reflect the updated position.

How to build:
- Start with an all-zero `BIT` and perform the same `update` for each element.
- Time: O(N log N) in the simple approach. There are O(N) build tricks too,
  but the simple method is easier to remember and sufficient in interviews.

Complexity:
- Query: O(log N)
- Update: O(log N)
- Space: O(N)

Limitations:
- Not ideal for range minima/maxima without additional tricks.
- For range updates and range queries, we typically use two BITs or switch to
  a segment tree depending on the required operation.

Worked example (step-by-step trace)
-----------------------------------
Let arr = [a0, a1, a2, a3, a4, a5, a6, a7, ...] and BIT is 1-based.
For clarity, consider indexes up to 16 (since powers of two align ranges nicely).

Coverage intuition:
- BIT[1]  covers (1 .. 1)             size 1   (LSB=1)
- BIT[2]  covers (1 .. 2)             size 2   (LSB=2)
- BIT[3]  covers (3 .. 3)             size 1   (LSB=1)
- BIT[4]  covers (1 .. 4)             size 4   (LSB=4)
- BIT[5]  covers (5 .. 5)             size 1
- BIT[6]  covers (5 .. 6)             size 2
- BIT[7]  covers (7 .. 7)             size 1
- BIT[8]  covers (1 .. 8)             size 8
- BIT[9]  covers (9 .. 9)             size 1
- BIT[10] covers (9 .. 10)            size 2
- BIT[11] covers (11 .. 11)           size 1
- BIT[12] covers (9 .. 12)            size 4
- BIT[13] covers (13 .. 13)           size 1
- BIT[14] covers (13 .. 14)           size 2
- BIT[15] covers (15 .. 15)           size 1
- BIT[16] covers (1 .. 16)            size 16

Trace: prefix query for i = 9 (0-based) i.e., 1-based idx = 10
- We call query(9), so internally i = 10 (1-based).
- Binary: 10 = 0b1010. LSB(10) = 2.
  Step 1: add BIT[10] which covers (9 .. 10)  -> contributes a9 + a10
  Move i = 10 - 2 = 8.
- Now i = 8 (0b1000). LSB(8) = 8.
  Step 2: add BIT[8] which covers (1 .. 8)    -> contributes a1 + ... + a8
  Move i = 8 - 8 = 0.
- i becomes 0 => stop. Total = a1 + ... + a10, as desired.

Trace: point update at external index 9 (0-based) i.e., 1-based idx = 10
- We call update(9, val), internally i = 10 (1-based).
- Binary: 10 = 0b1010. LSB(10) = 2.
  Step 1: BIT[10] += val   (updates range 9..10)
  Move i = 10 + 2 = 12.
- i = 12 (0b1100). LSB(12) = 4.
  Step 2: BIT[12] += val   (updates range 9..12)
  Move i = 12 + 4 = 16.
- i = 16 (0b10000). LSB(16) = 16.
  Step 3: BIT[16] += val   (updates range 1..16)
  Move i = 16 + 16 = 32 -> beyond N => stop.

Takeaway:
- Query walks downward by removing LSB: i -= (i & -i).
- Update walks upward by adding LSB:   i += (i & -i).
'''

class BIT:
    def __init__(self, arr):
        self.arr = arr
        # 1-based indexing: BIT[0] is a dummy slot
        self.bit = [0] * (len(arr) + 1)

        # Construct the BIT by applying point updates for each element.
        # This is the straightforward O(N log N) build.
        for i, x in enumerate(arr):
            # Update position i (0-based for the external API)
            self.update(i, x)

    def update(self, i, val):
        # Add `val` at index `i` (0-based external indexing).
        # Internally we walk indices that "cover" this position and include it in their range.
        n = len(self.arr)

        # Convert to 1-based index for the BIT internals.
        i += 1
        while i <= n:
            # Add contribution to this block's aggregate
            self.bit[i] += val

            # Jump to the next index that includes this position in its covered range
            i += i & -i

    def query(self, i):
        # Compute prefix sum over [0 .. i] (0-based external indexing).
        # Internally we repeatedly "strip" the least significant set bit from i.
        i += 1

        # Aggregate answer over disjoint canonical blocks
        res = 0
        while i > 0:
            res += self.bit[i]

            # Move to the parent by removing the LSSB
            i -= (i & -i)
            # Equivalent alternative:
            # i = i & (i - 1)

        return res

    def range_query(self, l, r):
        # Sum over [l .. r] via two prefix sums (assumes l <= r).
        return self.query(r) - self.query(l - 1)


if __name__ == '__main__':
    # Demonstration:
    # We'll build a BIT over an example array and compare a few prefix and range queries.
    arr = [0, 1, 2, 3, 4, 5, 6]
    fenwick = BIT(arr)
    # Prefix sums:
    # query(2) = arr[0] + arr[1] + arr[2] = 0 + 1 + 2 = 3
    print(fenwick.query(2))  # expected 3
    # query(3) = 0 + 1 + 2 + 3 = 6
    print(fenwick.query(3))  # expected 6
    # query(4) = 0 + 1 + 2 + 3 + 4 = 10
    print(fenwick.query(4))  # expected 10

    # Range sum [l .. r] via two prefix sums:
    # range_query(3, 5) = (0+1+2+3+4+5) - (0+1+2) = 15 - 3 = 12
    print(fenwick.range_query(3, 5))  # expected 12
