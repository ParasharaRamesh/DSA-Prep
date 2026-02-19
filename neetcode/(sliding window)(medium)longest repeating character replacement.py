'''
You are given a string s consisting of only uppercase english characters and an integer k. You can choose up to k characters of the string and replace them with any other uppercase English character.

After performing at most k replacements, return the length of the longest substring which contains only one distinct character.

Example 1:

Input: s = "XYYX", k = 2

Output: 4
Explanation: Either replace the 'X's with 'Y's, or replace the 'Y's with 'X's.

Example 2:

Input: s = "AAABABB", k = 1

Output: 5
Constraints:

1 <= s.length <= 1000
0 <= k <= s.length

Insight:

* grow as much as possible until there are k replacable things in every window

'''




from collections import defaultdict


class Solution:
    def characterReplacement_old(self, s: str, k: int) -> int:
        '''
        Sliding Window Approach:
        
        The key insight is that a window is valid if:
            (window_size) - (frequency of most common character) <= k
        
        This works because:
        - If we have a window of size n with the most frequent character appearing f times,
          then we need to replace (n - f) characters to make all characters the same.
        - We can do this replacement if (n - f) <= k.
        
        Algorithm:
        1. Expand the window (move 'end' pointer) as long as the window is valid.
        2. When the window becomes invalid, shrink it (move 'start' pointer) until it's valid again.
        3. Track the maximum valid window size seen.
        
        Time Complexity: O(n) where n is the length of the string
        Space Complexity: O(26) = O(1) for the character frequency map (only uppercase letters)
        '''
        max_len = 0  # Stores the maximum length of valid substring found so far
        counts = defaultdict(int)  # Frequency map of characters in the current window
        start, end = 0, 0  # Two pointers defining the sliding window [start, end]

        while end < len(s):
            # Inner loop: Expand the window as long as it remains valid
            # A window is valid when: (window_size) - (max_frequency) <= k
            # This means we can replace at most k characters to make all characters the same
            while (end < len(s)) and ((end - start + 1) - max(counts.values()) <= k):
                # Add the current character to our frequency map
                counts[s[end]] += 1
                
                # Update the maximum length with the current valid window size
                max_len = max(max_len, end - start + 1)
                
                # Expand the window by moving the end pointer
                end += 1
            
            # Window is now invalid, so shrink it from the left
            # Remove the leftmost character from the frequency map
            counts[s[start]] -= 1
            
            # Move the start pointer to shrink the window
            start += 1

        return max_len

    def characterReplacement(self, s: str, k: int) -> int:
        """Sliding window: outer loop = grow (add s[r]); inside = shrink then assign."""
        l = 0
        res = 0
        counts = defaultdict(int)

        for r in range(len(s)):
            # 1. GROW: Add the right element to state
            counts[s[r]] += 1

            # 2. SHRINK: While window is invalid, move l
            # Valid: (window_len - max_freq) <= k
            while (r - l + 1) - max(counts.values()) > k:
                counts[s[l]] -= 1
                l += 1

            # 3. ASSIGN: Window [l, r] is valid
            res = max(res, r - l + 1)

        return res
