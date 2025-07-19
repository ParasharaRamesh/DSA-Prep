'''
You are controlling a robot that is located somewhere in a room. The room is modeled as an m x n binary grid where 0 represents a wall and 1 represents an empty slot.

The robot starts at an unknown location in the room that is guaranteed to be empty, and you do not have access to the grid, but you can move the robot using the given API Robot.

You are tasked to use the robot to clean the entire room (i.e., clean every empty cell in the room). The robot with the four given APIs can move forward, turn left, or turn right. Each turn is 90 degrees.

When the robot tries to move into a wall cell, its bumper sensor detects the obstacle, and it stays on the current cell.

Design an algorithm to clean the entire room using the following APIs:

interface Robot {
  // returns true if next cell is open and robot moves into the cell.
  // returns false if next cell is obstacle and robot stays on the current cell.
  boolean move();

  // Robot will stay on the same cell after calling turnLeft/turnRight.
  // Each turn will be 90 degrees.
  void turnLeft();
  void turnRight();

  // Clean the current cell.
  void clean();
}
Note that the initial direction of the robot will be facing up. You can assume all four edges of the grid are all surrounded by a wall.



Custom testing:

The input is only given to initialize the room and the robot's position internally. You must solve this problem "blindfolded". In other words, you must control the robot using only the four mentioned APIs without knowing the room layout and the initial robot's position.



Example 1:


Input: room = [
    [1,1,1,1,1,0,1,1],
    [1,1,1,1,1,0,1,1],
    [1,0,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,0],
    [1,1,1,1,1,1,1,1]
    ], row = 1, col = 3

Output: Robot cleaned all rooms.
Explanation: All grids in the room are marked by either 0 or 1.
0 means the cell is blocked, while 1 means the cell is accessible.
The robot initially starts at the position of row=1, col=3.
From the top left corner, its position is one row below and three columns right.
Example 2:

Input: room = [
    [1]
], row = 0, col = 0
Output: Robot cleaned all rooms.


Constraints:

m == room.length
n == room[i].length
1 <= m <= 100
1 <= n <= 200
room[i][j] is either 0 or 1.
0 <= row < m
0 <= col < n
room[row][col] == 1
All the empty cells can be visited from the starting position.
'''


# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# implemented it for testing purposes
# """
class Robot:
    def __init__(self, grid, i, j):
        self.grid = grid
        self.m = len(grid)
        self.n = len(grid[0])

        self.i = i
        self.j = j
        self.direction = "U"

    def is_inbounds(self, x, y):
        return 0 <= x < self.m and 0 <= y < self.n

    def _calculate_next_pos(self):
        if self.direction == "U":
            return (self.i - 1, self.j)

        if self.direction == "D":
            return (self.i + 1, self.j)

        if self.direction == "L":
            return (self.i, self.j - 1)

        if self.direction == "R":
            return (self.i, self.j + 1)

    def move(self):
        """
        Returns true if the cell in front is open and robot moves into the cell.
        Returns false if the cell in front is blocked and robot stays in the current cell.
        :rtype bool
        """
        ni, nj = self._calculate_next_pos()

        if not self.is_inbounds(ni, nj) or self.grid[ni][nj] == 0:
            # blocked (out of bounds or wall)
            return False

        # move there
        self.i, self.j = ni, nj
        return True

    def turnLeft(self):
        """
        Robot will stay in the same cell after calling turnLeft/turnRight.
        Each turn will be 90 degrees.
        :rtype void
        """
        if self.direction == "U":
            self.direction = "L"
        elif self.direction == "L":
            self.direction = "D"
        elif self.direction == "D":
            self.direction = "R"
        elif self.direction == "R":
            self.direction = "U"

    def turnRight(self):
        """
        Robot will stay in the same cell after calling turnLeft/turnRight.
        Each turn will be 90 degrees.
        :rtype void
        """
        if self.direction == "U":
            self.direction = "R"
        elif self.direction == "R":
            self.direction = "D"
        elif self.direction == "D":
            self.direction = "L"
        elif self.direction == "L":
            self.direction = "U"

    def clean(self):
        """
        Clean the current cell.
        :rtype void
        """
        if self.grid[self.i][self.j] in [1, 2]:
            self.grid[self.i][self.j] = 2  # 2 means cleaned
            return

        raise Exception(f"({self.i}, {self.j}) is a wall and cannot be cleaned!")

    def is_all_cleaned(self):
        all_dirty = []
        for _i in range(self.m):
            for _j in range(self.n):
                if self.grid[_i][_j] == 1:  # still a cell which is yet to be moved and hasnt been cleaned yet
                    all_dirty.append((_i, _j))

        if len(all_dirty) > 0:
            print(f"all dirty cell locations still dirty are {all_dirty}")

        return len(all_dirty) == 0


'''
Thoughts:

. Constraints too big to do backtracking?
. Can do something like flood fill + dfs
. robot is at (0,0) in the start
. can track cells already cleaned (move + clean is better as atomic operation)
. recursively go in each direction if it is possible to move and it is not a visited cell
    - somehow after each thing finishes it needs to come back to cell where it started from otherwise robot cannot explore.
    - how to come back? 
        . store parent cell it came from? but how to use it?
        . after operation , find out where the parent cell was orient towards it and finish

'''


class Solution:
    # main function
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        # constants
        self.UP = (-1, 0)
        self.DOWN = (1, 0)
        self.LEFT = (0, -1)
        self.RIGHT = (0, 1)

        self.curr_pos = (0, 0)

        self.cleaned_cells = set()
        self.direction = "U"

        self.explore(robot, (0, 0), None)

    # utility functions
    def orient_left(self, robot):
        if self.direction == "U":
            robot.turnLeft()
        elif self.direction == "D":
            robot.turnRight()
        elif self.direction == "R":
            robot.turnRight()
            robot.turnRight()
        self.direction = "L"

    def orient_right(self, robot):
        if self.direction == "U":
            robot.turnRight()
        elif self.direction == "D":
            robot.turnLeft()
        elif self.direction == "L":
            robot.turnRight()
            robot.turnRight()
        self.direction = "R"

    def orient_up(self, robot):
        if self.direction == "D":
            robot.turnRight()
            robot.turnRight()
        elif self.direction == "R":
            robot.turnLeft()
        elif self.direction == "L":
            robot.turnRight()
        self.direction = "U"

    def orient_down(self, robot):
        if self.direction == "U":
            robot.turnRight()
            robot.turnRight()
        elif self.direction == "R":
            robot.turnRight()
        elif self.direction == "L":
            robot.turnLeft()
        self.direction = "D"

    def move_to_parent(self, robot, pos, parent_pos):
        # ideally parent_pos is only going to be a diff of 1 away
        assert abs(parent_pos[0] - pos[0]) + abs(
            parent_pos[1] - pos[1]) == 1, f"Cant move back to parent! {parent_pos = }, {pos = }"
        dx, dy = pos[0] - parent_pos[0], pos[1] - parent_pos[1]
        moved_direction = (dx, dy)

        # orient
        if moved_direction == self.UP:
            self.orient_down(robot)
        elif moved_direction == self.DOWN:
            self.orient_up(robot)
        elif moved_direction == self.LEFT:
            self.orient_right(robot)
        elif moved_direction == self.RIGHT:
            self.orient_left(robot)

        # move back
        self.curr_pos = parent_pos
        robot.move()

    # main exploration function (once it returns align it back to N)
    def explore(self, robot, pos, parent_pos):

        # clean current cell first
        robot.clean()
        self.cleaned_cells.add(pos)

        # explore up
        self.orient_up(robot)
        new_pos = (pos[0] + self.UP[0], pos[1] + self.UP[1])
        if new_pos not in self.cleaned_cells and robot.move():
            self.curr_pos = new_pos
            self.explore(robot, new_pos, pos)  # it is supposed to come back to the new_pos


        # explore left
        self.orient_left(robot)
        new_pos = (pos[0] + self.LEFT[0], pos[1] + self.LEFT[1])
        if new_pos not in self.cleaned_cells and robot.move():
            self.curr_pos = new_pos
            self.explore(robot, new_pos, pos)  # it is supposed to come back to the new_pos

        # explore right
        self.orient_right(robot)
        new_pos = (pos[0] + self.RIGHT[0], pos[1] + self.RIGHT[1])
        if new_pos not in self.cleaned_cells and robot.move():
            self.curr_pos = new_pos
            self.explore(robot, new_pos, pos)  # it is supposed to come back to the new_pos

        # explore down
        self.orient_down(robot)
        new_pos = (pos[0] + self.DOWN[0], pos[1] + self.DOWN[1])
        if new_pos not in self.cleaned_cells and robot.move():
            self.curr_pos = new_pos
            self.explore(robot, new_pos, pos)  # it is supposed to come back to the new_pos

        # Move back to parent cell
        if not parent_pos:
            # do nothing
            return

        self.move_to_parent(robot, pos, parent_pos)


if __name__ == '__main__':
    s = Solution()

    # test cases
    grid = [
        [1]
    ]
    row = 0
    col = 0
    robot = Robot(grid, row, col)
    s.cleanRoom(robot)
    assert robot.is_all_cleaned(), "Still dirty"
    print("test 1 done")

    grid = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    row = 1
    col = 0
    robot = Robot(grid, row, col)
    s.cleanRoom(robot)
    assert robot.is_all_cleaned(), "Still dirty"
    print("test 2 done")

    grid = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    row = 1
    col = 2
    robot = Robot(grid, row, col)
    s.cleanRoom(robot)
    assert robot.is_all_cleaned(), "Still dirty"

    grid = [
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    row = 1
    col = 3
    robot = Robot(grid, row, col)
    s.cleanRoom(robot)
    assert robot.is_all_cleaned(), "Still dirty"
    print("test 3 done")

    grid = [
        [1, 1, 0, 1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 0]
    ]
    row = 1
    col = 3
    robot = Robot(grid, row, col)
    s.cleanRoom(robot)
    assert robot.is_all_cleaned(), "Still dirty"
    print("test 4 done")