'''
You are given a string s which contains only three types of characters: '(', ')' and '*'.

Return true if s is valid, otherwise return false.

A string is valid if it follows all of the following rules:

Every left parenthesis '(' must have a corresponding right parenthesis ')'.
Every right parenthesis ')' must have a corresponding left parenthesis '('.
Left parenthesis '(' must go before the corresponding right parenthesis ')'.
A '*' could be treated as a right parenthesis ')' character or a left parenthesis '(' character, or as an empty string "".
Example 1:

Input: s = "((**)"

Output: true
Explanation: One of the '*' could be a ')' and the other could be an empty string.

Example 2:

Input: s = "(((*)"

Output: false
Explanation: The string is not valid because there is an extra '(' at the beginning, regardless of the extra '*'.

Constraints:

1 <= s.length <= 100
'''


class Solution:
    '''
    Two stack greedy solution:

    . Maintain two stacks with indices of open brackets and another with indices of asterisks
    . Algorithm works in 2 phases:

    Phase 1:
    - Iterate through the entire string, push indices of open and asterisks into respective stacks.
    - In case of closing bracket, try to pop first from the open stack and if that's empty then from the asterisk stack.
    - This is because here we consider asterisk as a starting/open bracket and try to match it with the appropriate closing bracket.
    - If both are empty clearly it is not valid, return False early

    Phase 2:
    - In case there are any open brackets left ( because they need to be matched with the appropriate closed bracket ), then we consider the asterisk as closing bracket in this case.
    - we iterate through both stacks at same time and pop both.
        * Here we would basically be going from the last open & last asterisk all the way to the first open and first asterisk ( since we are popping in a stack => reverse order)
        * At every point the open bracket index must be lesser than the asterisk index.
        * In the case it is not , we can return False and exit early.
    - After this loop, there could still be open brackets left which cannot be matched with any asterisk ( i.e. pseudo closing bracket ).
    - If there is anything in the open stack => False, else if it is empty => True
    '''

    def checkValidString_two_stack_greedy(self, s: str) -> bool:
        # Stacks to store indices of open brackets and asterisks
        open_brackets = []
        asterisks = []

        for i, ch in enumerate(s):
            # If current character is an open bracket, push its index onto the stack
            if ch == "(":
                open_brackets.append(i)
            # If current character is an asterisk, push its index onto the stack
            elif ch == "*":
                asterisks.append(i)
            # current character is a closing bracket ')'
            else:
                # If there are open brackets available, use them to balance the closing bracket
                if open_brackets:
                    open_brackets.pop()
                elif asterisks:
                    # treat * as opening bracket in this case
                    # If no open brackets are available, use an asterisk to balance the closing bracket
                    asterisks.pop()
                else:
                    # unmatched ')' and no '*' to balance it.
                    return False

        # Check if there are remaining open brackets and asterisks that can balance them. In this case * acts as closing bracket
        while open_brackets and asterisks:
            # If an open bracket appears after an asterisk, it cannot be balanced, return false
            if open_brackets.pop() > asterisks.pop():
                return False  # '*' before '(' which cannot be balanced.

        # If all open brackets are matched and there are no unmatched open brackets left, return true
        return not open_brackets

    '''
    Greedy space optimal:
    . Solution hinges on the fact that we keep track of only no of open brackets, but since the * is there it can either increase it or decrease it.
    . Therefore keep track of left_min and left_max => no of open brackets in worst case and best case
        - left_min = minimum number of unclosed ( possible so far
        - left_max = maximum number of unclosed ( possible so far
    . If there is an open bracket, increment both
    . If there is a close bracket, decrement both
    . In case there is an asterisk:
        - decrement left_min => i.e. we are assuming that all * is a right bracket ), therefore decrementing no of open brackets
        - increment left_max => i.e. we are assuming that all * is a left bracket (, therefore we are incremementing no of open brackets
    . At the end of the iteration there are is one early stopping condition:
        - if left_max < 0:
            . This means that despite assuming that all * is ( optimistically, the left_max value going below 0 => there are more ) closing brackets than opening, therefore we can return False rightaway
            . Since we are going left -> right i.e. forward, there is no way once there is an ) imbalance we can ever balance it because )( is not considered as balanced!
            . Therefore we can surely return False right away
    . Similarly we can check for left_min going below 0 and reset it to 0:
        - why reset? because this is the case where (almost) every star is considered as a ). 
        - Note this is common to both * and the ) case, since in both cases, left_min can go below 0
        - * case:
            - In case it goes below 0 it means that we are assuming that there are too many stars considered as ), but surely some of it can be considered as ( or even empty!
            - More specifically, at the tipping point when it goes below 0; it means that so far considering everything as ) balanced things out nicely. 
            - Therefore the next * could be both empty '' (in which case we leave left_min as is at 0) or is a new (.. (which means that left_min can be reset to 1). 
            - But since left_min tracks the min possible no of openings, better to reset it to 0!
        - ) case (why reset to 0 here!?):
            - But the best-case path (max path) hasn’t failed yet — left_max may still be ≥ 0. So we don’t give up yet — we continue in the hope that future * might bail us out.
            - This means that out of all the *s seen before, in the worst case ( min case ) where every * is considered as a ), then when it comes to the tipping point 0, it is perfectly balanced. 
            - Two things could have happened as for why the left_min can still be 0 when when almost everything was a closing bracket ) (i.e. why the reset):
                a. one of the older * could have been a ( => somewhere before there would have been a +1 which we are doing -1 now
                b. one of the older * could have been empty => which means at that point left_min would have never been decremented, so we still have that +1 from before => therefore when we do the -1 now it can be 0 and balanced!
    '''
    def checkValidString(self, s: str) -> bool:
        left_min, left_max = 0, 0

        for c in s:
            if c == '(':
                # fixed outcome : increment no of open (left) brackets
                left_min += 1
                left_max += 1
            elif c == ")":
                # fixed outcome: decrement no of open (left) brackets
                left_min -= 1
                left_max -= 1
            else:
                # min can decrease because * might be a right bracket
                left_min -= 1
                # in case * is empty, then the no of left remains the same or rather left_min <= left <= left_max
                # max can increase because * might be a left bracket
                left_max += 1

            #invalid case therefore can directly return False
            if left_max < 0:
                return False

            # after every character: check if the left_min or max has fallen below zero
            if left_min < 0:
                # reset to zero because this represents the case that there are more closed(right brackets) than open(left brackets)
                left_min = 0

        return left_min <= 0 <= left_max


if __name__ == '__main__':
    sol = Solution()

    s = "***)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "((**)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "*((*)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "**((*)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "*)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "()"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(*"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(*)"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(*)*"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(*))"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(((*)"
    expected = False
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "((((()(()()()*()(((((*)()*(**(())))))(())()())(((())())())))))))(((((())*)))()))(()((*()*(*)))(*)()"
    expected = True
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(((((*(()((((*((**(((()()*)()()()*((((**)())*)*)))))))(())(()))())((*()()(((()((()*(())*(()**)()(())"
    expected = False
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"

    s = "(((()))())))*))())()(**(((())(()(*()((((())))*())(())*(*(()(*)))()*())**((()(()))())(*(*))*))())"
    expected = False
    res = sol.checkValidString(s)
    assert res == expected, f"{expected = }, {res = }"
