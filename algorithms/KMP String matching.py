#BRUTE FORCE AND INEFFICIENT
def calculateLengthOfLongestPrefixCumSuffix(word):
    n = len(word)
    i = 0
    j = 1
    matchingPrefixSuffixLength = 0

    while j < n:
        if word[i] == word[j]:
            i += 1
            matchingPrefixSuffixLength += 1
        else:
            i = 0
            matchingPrefixSuffixLength = 0

        j += 1

    return matchingPrefixSuffixLength

def computePrefix(substring):
    prefix = [0] * len(substring)

    for i in range(1, len(substring)):
        prefix[i] = calculateLengthOfLongestPrefixCumSuffix(substring[:i+1])

    return prefix

# THIS Is apparently the better approach
def compute_kmp_prefix(substring):
    """
    We build the LPS (Longest Proper Prefix which is also a Suffix) array.

    What lps[i] means (this is the most important sentence):

        lps[i] = the length of the longest string X such that:
                 X is a prefix of substring[0 : i+1]
                 X is also a suffix of substring[0 : i+1]

    In pictures:

        substring[0:i+1] =  X  .........  X
                            ^            ^
                            |            |
                         prefix        suffix

    The algorithm does NOT try all possible prefixes every time.
    Instead, it maintains a *hypothesis* about how large the border is,
    and intelligently shrinks that hypothesis when it breaks.
    """

    m = len(substring)

    # lps[i] will eventually store the correct border length
    # for substring[0 : i+1]
    lps = [0] * m

    # ---------------------------------------------------------
    # `length` is our CURRENT HYPOTHESIS:
    #
    #   "I believe substring[0:length] is the longest border
    #    for the prefix ending at index i-1."
    #
    # At the start (i = 1), the prefix is one character long,
    # so the longest proper border must be 0.
    # ---------------------------------------------------------
    length = 0

    # We start from i = 1 because:
    # - A single character has no proper prefix
    # - So lps[0] is always 0 by definition
    i = 1

    # ---------------------------------------------------------
    # LOOP INVARIANT (always true when entering the loop):
    #
    # 1) lps[0 .. i-1] are already correct
    # 2) `length` == lps[i-1]
    #
    # Meaning:
    #   We already know the best border for substring[0:i],
    #   and now we want to extend or fix it for substring[0:i+1].
    # ---------------------------------------------------------
    while i < m:

        # -----------------------------------------------------
        # CASE 1: The hypothesis survives
        #
        # We check whether the next character can EXTEND
        # the current border hypothesis.
        #
        # Visually:
        #
        #   X.....X   ?=   next character
        #   ^
        #   substring[length]
        # -----------------------------------------------------
        if substring[i] == substring[length]:

            # The hypothesis was correct and can be extended.
            # The border grows by exactly one character.
            length += 1

            # Store the result for this prefix
            lps[i] = length

            # Move forward: we are done with this position
            i += 1

        else:
            # -------------------------------------------------
            # CASE 2: The hypothesis FAILS
            #
            # substring[i] != substring[length]
            #
            # Meaning:
            #   The border of size `length` does NOT work anymore.
            #
            # But we do NOT immediately give up.
            # Instead, we ask:
            #
            #   "Is there a smaller border INSIDE the current one
            #    that might still work?"
            # -------------------------------------------------

            if length != 0:
            # ---------------------------------------------------------
                # We are in a MISMATCH, but our current border hypothesis
                # still has non-zero length.
                #
                # Current situation (zoomed-out view):
                #
                #   substring[0 : i+1] looks like
                #
                #       XX.............XXY
                #                       ^
                #                       mismatch at i
                #
                #   where:
                #     - "XX" is the current border (prefix == suffix)
                #     - length = len("XX")
                #
                # The border "XX" is now invalid.
                #
                # ---------------------------------------------------------
                # Key insight:
                #   Any *new* valid border MUST be completely contained
                #   inside the old one.
                #
                # So instead of restarting from scratch, we:
                #
                #   1) Zoom into the prefix "XX"
                #
                #          XX
                #
                #   2) Ask: does THIS prefix have a smaller border inside it?
                #
                #          X....X
                #
                #   3) The length of that inner border is already known:
                #
                #          lps[length - 1]
                #
                # ---------------------------------------------------------
                # We now SHRINK our hypothesis to that inner border:
                #
                #       length = lps[length - 1]
                #
                # This gives us the next-largest possible border candidate.
                #
                # IMPORTANT:
                #   We do NOT increment `i` here.
                #
                #   We want to retry the SAME character substring[i]
                #   against this shorter border in the next iteration.
                #
                # If this border also fails, the process repeats.
                # ---------------------------------------------------------

                length = lps[length - 1]
                
            else:
                # ---------------------------------------------
                # CASE 3: Hypothesis cannot be shrunk anymore
                #
                # length == 0 means:
                #   There is NO proper prefix left to try.
                #
                # Therefore:
                #   substring[0:i+1] has NO border at all.
                # ---------------------------------------------

                lps[i] = 0
                i += 1

    return lps


def knuthMorrisPrattAlgorithm(string, substring):
    prefix = computePrefix(substring)
    i = 0
    j = 0
    n = len(string)
    m = len(substring)

    while i < n:
        while i < n and j < m and string[i] == substring[j]:
            #keep moving together!
            i += 1
            j += 1

        if j == m:
            #match is found at index i - j
            return True
        elif j > 0:
            #if at all some part of sub string was matched!
            # reset j to point just after current longest prefix, i will stay the same
            # remember the part which matched so far in the substring can be visualized as [prefix, blah..suffix](miss)
            #  but the suffix is the same as the prefix, so we can reset j to point just after current longest prefix => index of 'blah'
            j = prefix[j-1]
        else:
            i += 1

    return False



if __name__ == '__main__':
    main = "aefoaefcdaefcdaed"
    subs = "aefcdaed"
    # main = "caba"
    # subs = "aba"
    print(knuthMorrisPrattAlgorithm(main, subs))

