'''
You are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space.

For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

Example 1:

Input: asteroids = [2,4,-4,-1]

Output: [2]
Example 2:

Input: asteroids = [5,5]

Output: [5,5]
Example 3:

Input: asteroids = [7,-3,9]

Output: [7,9]
Constraints:

2 <= asteroids.length <= 10,000.
-1000 <= asteroids[i] <= 1000
asteroids[i] != 0

'''

from typing import List

class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []

        for asteroid in asteroids:
            retain = True
            while stack:
                if stack[-1] * asteroid > 0:
                    retain = True
                    break

                if stack[-1] < 0:
                    retain = True
                    break 

                if stack[-1] == -1 * asteroid:
                    stack.pop()
                    retain = False
                    break

                if abs(stack[-1]) < abs(asteroid):
                    retain = True
                    stack.pop()
                    continue

                retain = False
                break

            if retain:
                stack.append(asteroid)

        return stack

if __name__ == "__main__":       
    a = Solution()

    asteroids = [-2,-2,1,-2]
    expected = [-2 , -2, -2]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [5, 10, -5]
    expected = [5, 10]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [8, -8]
    expected = []
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [10, 2, -5]
    expected = [10]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [3,5,-6,2,-1,4]
    expected = [-6, 2, 4]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [2,4,-4,-1]
    expected = [2]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [5, 5]
    expected = [5, 5]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"

    asteroids = [7,-3,9]
    expected = [7, 9]
    ans = a.asteroidCollision(asteroids)
    assert ans == expected, f"{expected =} {ans = }"