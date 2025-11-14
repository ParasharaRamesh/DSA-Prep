'''
Leetcode 5: Longest Palindromic Substring

Problem: Find the longest palindromic substring in a given string.

Time Complexity Comparison:
- Brute force: O(N³) - check all substrings and verify if palindrome
- Expand from centers: O(N²) - for each position, expand outward
- Manacher's Algorithm: O(N) - linear time using dynamic programming insights

Refer to this video for detailed explanation: https://www.youtube.com/watch?v=nbTSfrEfo6M

================================================================================
ALGORITHM OVERVIEW
================================================================================

Manacher's Algorithm uses four key insights to achieve linear time:

1. STRING TRANSFORMATION (Handling Even/Odd Length Palindromes)
   - Insert '#' between every character to convert any string to odd length
   - Original: "aba" (length 3) → Transformed: "#a#b#a#" (length 7)
   - Original: "abba" (length 4) → Transformed: "#a#b#b#a#" (length 9)
   - This allows us to treat all palindromes as centered at a single character
   - Example: "abba" becomes "#a#b#b#a#" where the palindrome is centered at the middle '#'

2. PALINDROME RADIUS ARRAY (Avoiding Re-computation)
   - Store palindrome radius at each position in an array
   - palindrome_radius[i] = number of characters on EACH SIDE of center i (not including center)
   - Total palindrome length = 2 * palindrome_radius[i] + 1 (center + left side + right side)
   - Example: For "#a#b#a#", at index 3 (character 'b'):
     - palindrome_radius[3] = 3 (3 chars left: indices 0-2, center: index 3, 3 chars right: indices 4-6)
     - Total span: indices 0 to 6 = "#a#b#a#" (7 characters: 3+1+3)
     - Note: The center 'b' is included in the palindrome but not counted in the radius

3. MIRROR PROPERTY (The Key Optimization)
   
   This is the core insight that makes Manacher's algorithm linear instead of quadratic.
   
   INTUITION:
   When we have a large palindrome, positions on the right side mirror positions on the left side.
   If we already computed the palindrome radius at a left position, we can reuse that information
   for the corresponding right position, avoiding redundant character comparisons.
   
   DETAILED EXPLANATION:
   Suppose we've found a palindrome centered at position 'c' that extends to right boundary 'R'.
   For any position 'i' within this palindrome (i.e., c < i < R):
   - Position 'i' is on the right side of center 'c'
   - Position 'mirror = 2*c - i' is on the left side of center 'c' (the mirror of 'i')
   - Due to palindrome symmetry, the palindrome at 'i' mirrors the palindrome at 'mirror'
   - We can use palindrome_radius[mirror] as a starting estimate for palindrome_radius[i]
   
   STEP-BY-STEP EXAMPLE:
   
   String: "#a#b#a#b#a#"
   Let's index it:  0 1 2 3 4 5 6 7 8 9 10
                    # a # b # a # b # a #
   
   Suppose we've processed up to position 4 and found:
   - Center c = 4 (at character '#')
   - palindrome_radius[4] = 4 (palindrome spans from index 0 to 8: "#a#b#a#b#a#")
   - Right boundary R = 4 + 4 = 8 (rightmost position reached)
   
   Now we're at position i = 6 (character '#') and want to compute palindrome_radius[6]:
   
   Step 1: Check if i is within current palindrome's boundary
   - i = 6, R = 8
   - Since 6 < 8, position 6 is within the known palindrome
   - We can use mirror property!
   
   Step 2: Find mirror position
   - mirror = 2*c - i = 2*4 - 6 = 8 - 6 = 2
   - Position 2 is the mirror of position 6 with respect to center 4
   - Visual:   [0] [1] [2] [3] [4] [5] [6] [7] [8]
                #   a   #   b   #   a   #   b   #
                        ↑       ↑       ↑
                      mirror   center   i
                      (left)   (c=4)   (right)
   
   Step 3: Use mirror value as starting point
   - Suppose we already computed palindrome_radius[2] = 1
   - This means at position 2, there's a palindrome of radius 1
   - Due to symmetry, position 6 should have AT LEAST radius 1
   - Instead of starting from radius 0, we start from radius 1
   - This saves us 1 character comparison!
   
   Step 4: Expand from the estimated radius
   - Start expanding from radius 1 instead of 0
   - Check if characters at distance 2 match, then distance 3, etc.
   - This is the optimization: we skip comparisons we already know!

4. BOUNDARY CONSTRAINT (Why we need min())
   
   The mirror property gives us a starting point, but we must respect boundaries!
   
   PROBLEM: The mirrored palindrome might extend beyond the left boundary of the 
   current palindrome. In that case, we can't trust the full mirror value.
   
   EXAMPLE - Case 1: Mirror palindrome is fully contained (use full mirror value)
   String: "#a#b#a#b#a#"
   - Center c = 4, R = 8
   - At i = 6, mirror = 2
   - If palindrome_radius[2] = 1, and position 2-1=1 and 2+1=3 are within boundaries
   - Then palindrome_radius[6] can safely start at 1
   
   EXAMPLE - Case 2: Mirror palindrome extends beyond left boundary (use R-i)
   String: "#a#b#a#b#a#b#a#"
   - Center c = 5, palindrome_radius[5] = 5, R = 10
   - At i = 7, mirror = 2*5 - 7 = 3
   - If palindrome_radius[3] = 6, it would extend to position 3-6 = -3 (invalid!)
   - We can only guarantee (R - i) = 10 - 7 = 3 characters safely
   - So we use min(6, 3) = 3 as starting radius
   
   SOLUTION: We take min(palindrome_radius[mirror], R - i)
   - palindrome_radius[mirror]: The mirror value (if fully contained)
   - R - i: Distance from i to right boundary (maximum safe radius)
   - The minimum ensures we stay within known boundaries

================================================================================
ALGORITHM STEPS
================================================================================

For each position i in the transformed string:
1. If i is within current palindrome's right boundary:
   - Use mirror property to get initial radius estimate
   - Take min(mirror_radius, R - i) to respect boundaries
2. Expand outward from the estimated radius
3. If palindrome at i extends beyond current right boundary:
   - Update center to i and right boundary to i + radius
4. Track the longest palindrome found so far

================================================================================
WHY IT'S LINEAR TIME
================================================================================

- Each character is compared at most once during expansion
- When we use mirror property, we skip comparisons we already know
- The right boundary R always moves forward, never backward
- Total comparisons: O(N)
'''


class Solution:
    def longestPalindrome_bruteforce(self, s: str) -> str:
        """
        Brute Force Approach: Check all possible substrings.
        
        Time Complexity: O(N³)
        - O(N²) substrings to check
        - O(N) time to verify if each substring is a palindrome
        
        Space Complexity: O(1) excluding output
        """
        if len(s) <= 1:
            return s
        
        longest = s[0]
        longest_len = 1
        
        # Try all possible substrings
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                # Check if substring s[i:j+1] is a palindrome
                substring = s[i:j+1]
                if substring == substring[::-1]:  # Check if palindrome
                    if len(substring) > longest_len:
                        longest = substring
                        longest_len = len(substring)
        
        return longest
    
    def longestPalindrome_expand_centers(self, s: str) -> str:
        """
        Expand from Centers Approach: For each position, expand outward.
        
        Time Complexity: O(N²)
        - O(N) centers to check (including between characters for even-length palindromes)
        - O(N) time to expand from each center
        
        Space Complexity: O(1) excluding output
        
        Key insight: A palindrome can be centered at:
        - A character (odd length): "aba" centered at 'b'
        - Between two characters (even length): "abba" centered between the two 'b's
        """
        if len(s) <= 1:
            return s
        
        def expand_around_center(left: int, right: int) -> int:
            """
            Expand outward from center and return the length of palindrome found.
            
            Args:
                left: Left boundary (inclusive)
                right: Right boundary (inclusive)
            
            Returns:
                Length of the palindrome
            """
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Return length: (right - left - 1)
            # Example: "aba", left=0, right=2, after expansion left=-1, right=3
            # Length = 3 - (-1) - 1 = 3
            return right - left - 1
        
        start = 0
        max_len = 1
        
        for i in range(len(s)):
            # Case 1: Odd-length palindrome centered at i
            # Example: "aba" centered at index 1 ('b')
            len1 = expand_around_center(i, i)
            
            # Case 2: Even-length palindrome centered between i and i+1
            # Example: "abba" centered between indices 1 and 2
            len2 = expand_around_center(i, i + 1)
            
            # Take the longer palindrome
            current_len = max(len1, len2)
            
            if current_len > max_len:
                max_len = current_len
                # Calculate start position
                # For odd: start = i - (len-1)//2
                # For even: start = i - (len-2)//2
                # Both can be simplified to: start = i - (current_len - 1) // 2
                start = i - (current_len - 1) // 2
        
        return s[start:start + max_len]
    
    def longestPalindrome_dp(self, s: str) -> str:
        """
        Dynamic Programming Approach: Top-down memoization (recursive).
        
        Time Complexity: O(N²)
        - Each substring s[i:j+1] is checked at most once
        - O(N²) substrings total
        
        Space Complexity: O(N²) for the memoization cache + O(N) for recursion stack
        
        Approach:
        - Recursive function checks if s[i:j+1] is a palindrome
        - Memoization avoids recomputing the same subproblems
        - Track the longest palindrome found during recursion
        
        Recurrence:
        - Base case: i >= j → True (empty string or single character)
        - If s[i] != s[j] → False (first and last don't match)
        - Otherwise: is_palindrome(i, j) = is_palindrome(i+1, j-1)
        
        Example:
        String: "babad"
        is_palindrome(0, 2) for "bab":
          - s[0] == s[2] ('b' == 'b') ✓
          - Recursively check is_palindrome(1, 1) for "a" → True
          - Result: True
        """
        if len(s) <= 1:
            return s
        
        n = len(s)
        # Memoization cache: memo[i][j] = True if s[i:j+1] is a palindrome
        # None means not computed yet
        memo = [[None] * n for _ in range(n)]
        
        # Track the longest palindrome found
        start = 0
        max_len = 1
        
        def is_palindrome(i: int, j: int) -> bool:
            """
            Recursively check if s[i:j+1] is a palindrome using memoization.
            
            Args:
                i: Start index (inclusive)
                j: End index (inclusive)
            
            Returns:
                True if s[i:j+1] is a palindrome, False otherwise
            """
            # Base case: empty string or single character is always a palindrome
            if i >= j:
                return True
            
            # Check memoization cache first
            if memo[i][j] is not None:
                return memo[i][j]
            
            # Recursive case:
            # s[i:j+1] is a palindrome if:
            # 1. First and last characters match: s[i] == s[j]
            # 2. Inner substring s[i+1:j] is also a palindrome
            if s[i] == s[j]:
                result = is_palindrome(i + 1, j - 1)
            else:
                result = False
            
            # Store result in cache
            memo[i][j] = result
            
            # Update longest palindrome if this one is longer
            nonlocal start, max_len
            if result:
                current_len = j - i + 1
                if current_len > max_len:
                    start = i
                    max_len = current_len
            
            return result
        
        # Check all possible substrings
        # We check from longest to shortest to potentially find the answer faster
        # (though we still need to check all to be sure)
        for i in range(n):
            for j in range(i, n):
                is_palindrome(i, j)
        
        return s[start:start + max_len]
    
    def add_hashes(self, s: str) -> str:
        """
        Transform string by inserting '#' between every character.
        
        This converts any string (even or odd length) to odd length, allowing
        us to treat all palindromes as centered at a single character.
        
        Example:
            "aba" → "#a#b#a#" (length 3 → 7)
            "abba" → "#a#b#b#a#" (length 4 → 9)
        """
        res = "#"
        for c in s:
            res += f"{c}#"
        return res

    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring using Manacher's Algorithm (OPTIMAL).
        
        This is the default method that uses Manacher's algorithm for O(N) time.
        For other approaches, see:
        - longestPalindrome_bruteforce: O(N³)
        - longestPalindrome_expand_centers: O(N²)
        - longestPalindrome_dp: O(N²)
        
        Time Complexity: O(N) where N is the length of the string
        Space Complexity: O(N) for the palindrome_radius array
        """
        # Edge case: strings of length 0 or 1 are already palindromes
        if len(s) <= 1:
            return s

        # Track the best palindrome found so far
        # Initialize with first character (any single char is a palindrome)
        longest_palindrome = s[0]
        longest_palindrome_length = 1

        # Transform string to handle even-length palindromes uniformly
        # Example: "babad" → "#b#a#b#a#d#"
        s = self.add_hashes(s)
        n = len(s)

        # palindrome_radius[i] stores the radius of the longest palindrome centered at i
        # Example: For "#a#b#a#", palindrome_radius[3] = 3 (palindrome spans indices 0-6)
        palindrome_radius = [0] * n
        
        # Current palindrome's center and rightmost boundary (stored as absolute position)
        # Initially, no palindrome found, so center=0, radius=0
        center = 0
        radius = 0  # This stores the rightmost position (i + palindrome_radius[i]), not the radius itself

        # Process each position in the transformed string
        for i in range(n):
            # Check if current position i is within the right boundary of current palindrome
            # If yes, we can use mirror property to get a head start and avoid redundant comparisons
            # 
            # Example scenario:
            #   String: "#a#b#a#b#a#"
            #   Current center = 4, radius = 8 (rightmost position reached)
            #   For i = 6: 6 < 8, so we can use mirror property
            #   Mirror of 6 = 2*4 - 6 = 2
            #   If palindrome_radius[2] = 1, we know palindrome_radius[6] is at least 1
            if i < radius:  # i is within the current palindrome's right boundary
                # Find the mirror position of i with respect to center
                # Formula: mirror = 2*center - i
                # This works because center is the midpoint: (mirror + i) / 2 = center
                # 
                # Example: center=4, i=6 → mirror = 2*4 - 6 = 2
                #          The palindrome centered at 4 has left boundary at 0 and right at 8
                #          Position 2 (left side) mirrors position 6 (right side)
                mirror = 2 * center - i

                # Use mirror property: palindrome at i mirrors palindrome at mirror position
                # However, we must respect the boundary constraint
                # 
                # Case 1: Mirror palindrome is fully contained within current palindrome
                #   → Use palindrome_radius[mirror] as starting point
                #   Example: center=4, radius=8, i=6, mirror=2
                #            If palindrome_radius[2] = 1, and position 2+1=3 is within boundaries
                #            → palindrome_radius[6] can start at 1
                #
                # Case 2: Mirror palindrome extends beyond left boundary
                #   → Can only guarantee (radius - i) characters (distance from i to right boundary)
                #   Example: center=4, radius=8, i=6
                #            If palindrome_radius[2] = 5, it would extend to position -1 (invalid)
                #            We can only guarantee 8-6=2 characters safely
                #
                # We take the minimum to ensure we stay within known boundaries
                # Example: If palindrome_radius[mirror]=3 but radius-i=2, we use 2
                palindrome_radius[i] = min(
                    palindrome_radius[mirror],  # Mirror value (if fully contained)
                    radius - i                   # Boundary constraint (distance to right edge)
                )

            # If i is outside the current palindrome's boundary (i >= radius):
            #   - palindrome_radius[i] remains 0 (initialized value)
            #   - We'll expand from scratch, starting from radius 0
            #   - This happens when we encounter a position beyond all previously found palindromes

            # Expand outward from the current radius estimate
            # We check characters at distance (palindrome_radius[i] + 1) from center i
            # Example: If palindrome_radius[i] = 2, we check positions i-3 and i+3
            # 
            # The while loop continues as long as:
            # 1. Left boundary is valid (i - (radius+1) >= 0)
            # 2. Right boundary is valid (i + (radius+1) < n)
            # 3. Characters at both boundaries match
            while (
                i - (palindrome_radius[i] + 1) >= 0 and  # Left boundary check
                i + (palindrome_radius[i] + 1) < n and    # Right boundary check
                s[i - (palindrome_radius[i] + 1)] == s[i + (palindrome_radius[i] + 1)]  # Characters match
            ):
                # Characters match, so palindrome extends further
                # Example: "#a#b#a#" at i=3, radius=2, checking positions 0 and 6
                #          Both are '#', so increment radius to 3
                palindrome_radius[i] += 1

            # Update center and right boundary if current palindrome extends further
            # This happens when the palindrome at i reaches beyond the previously known rightmost position
            # Example: If radius=8 (rightmost known position) and i=6 with palindrome_radius[6]=3,
            #          then 6+3=9 > 8, so update center=6, radius=9
            if i + palindrome_radius[i] > radius:
                center = i
                radius = i + palindrome_radius[i]  # Update rightmost known position

            # Update best palindrome if current one is longer
            # palindrome_radius[i] represents the actual length of palindrome in transformed string
            # Example: palindrome_radius[i] = 3 means palindrome spans 7 characters (indices i-3 to i+3)
            if palindrome_radius[i] > longest_palindrome_length:
                longest_palindrome_length = palindrome_radius[i]
                # Extract palindrome substring and remove '#' characters
                # Example: s[3-3:3+3+1] = s[0:7] = "#a#b#a#" → "aba"
                longest_palindrome = s[i - palindrome_radius[i]: i + palindrome_radius[i] + 1].replace("#", "")

        return longest_palindrome

if __name__ == '__main__':
    sol = Solution()
    test_cases = ["babad", "cbbd", "abdabba", "a", "ac", "racecar"]
    
    print("=" * 80)
    print("Testing all approaches for Longest Palindromic Substring")
    print("=" * 80)
    
    for test in test_cases:
        print(f"\nInput: '{test}'")
        print("-" * 80)
        
        # Brute Force O(N³)
        result_bf = sol.longestPalindrome_bruteforce(test)
        print(f"Brute Force (O(N³)):        '{result_bf}'")
        
        # Expand from Centers O(N²)
        result_expand = sol.longestPalindrome_expand_centers(test)
        print(f"Expand Centers (O(N²)):     '{result_expand}'")
        
        # Dynamic Programming O(N²)
        result_dp = sol.longestPalindrome_dp(test)
        print(f"Dynamic Programming (O(N²)): '{result_dp}'")
        
        # Manacher's Algorithm O(N)
        result_manacher = sol.longestPalindrome(test)
        print(f"Manacher's Algorithm (O(N)): '{result_manacher}'")
        
        # Verify all methods return the same result
        results = [result_bf, result_expand, result_dp, result_manacher]
        if len(set(results)) == 1:
            print(f"[OK] All methods agree: '{result_manacher}'")
        else:
            print(f"[ERROR] Methods disagree! Results: {results}")
