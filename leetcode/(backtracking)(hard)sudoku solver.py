'''
Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The '.' character indicates empty cells.

 

Example 1:


Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
Explanation: The input board is shown above and the only valid solution is shown below:


 

Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit or '.'.
It is guaranteed that the input board has only one solution.
'''

'''
Idea being that we can use bitmasks to store the numbers present in each row and col and square.

When getting potential candidates for location, we can just do a bitwise or across all 3 masks and then iterate only through 9 numbers to get the candidates in a bitwise manner

if not then the other way of solving it would be in the class Solution given below 
'''
class OptimalBitMaskSolution
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.empty_locs = self.get_empty_locs(board)
        
        # construct bit masks for row
        self.rows = [None] * 9 
        for r in range(9):
            row = 0
            for j in range(9):
                if board[r][j] != ".":
                    val = int(board[r][j])
                    row |= 1 << (val - 1)
            self.rows[r] = row

        # construct bit masks for col
        self.cols = [None] * 9 
        for c in range(9):
            col = 0
            for i in range(9):
                if board[i][c] != ".":
                    val = int(board[i][c])
                    col |= 1 << (val - 1)
            self.cols[c] = col

        # construct bit masks for squares
        self.sqs = [None] * 9
        for sq in range(9):
            sqI = sq // 3
            sqJ = sq % 3
            box = 0

            for i in range(3*sqI, 3*sqI + 3):
                for j in range(3*sqJ, 3*sqJ + 3):
                    if board[i][j] != ".":
                        val = int(board[i][j])
                        box |= 1 << (val - 1)
            
            self.sqs[sq] = box

        # try solving from the first empty location
        self.solve(0, board)

    def get_empty_locs(self, board):
        res = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    res.append((i, j))
        return res

    # k is index in the self.empty_locs which indicates that the kth empty loc has to be solved
    def solve(self, k, board):
        # only after filling all empty locations should you check 
        if k == len(self.empty_locs):
            return True

        # we are trying to solve the kth empty loc
        i, j = self.empty_locs[k] 

        # get candidate values for this spot based on the current state of the board
        candidate_values = self.get_loc_candidates(i, j)

        for candidate in candidate_values:
            # try adding it
            board[i][j] = candidate
            candidate = int(candidate)
            self.rows[i] |= 1 << (candidate - 1)
            self.cols[j] |= 1 << (candidate - 1)
            self.sqs[3*(i//3) + (j//3)] |= 1 << (candidate - 1)

            # check if it is a success down this path
            if self.solve(k + 1, board):
                return True

            # if not remove it 
            board[i][j] = '.'
            self.rows[i] ^= 1 << (candidate - 1)
            self.cols[j] ^= 1 << (candidate - 1)
            self.sqs[3*(i//3) + (j//3)] ^= 1 << (candidate - 1)

        return False

    def get_loc_candidates(self, i, j):
        combined_mask = self.rows[i] | self.cols[j] | self.sqs[3*(i//3) + (j//3)]
        
        # now check each index and which ones are zero
        candidates = []
        i = 1
        while i < 10:
            if not combined_mask & 1 << (i - 1):
                candidates.append(str(i))
            i += 1

        return candidates
   

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.empty_locs = self.get_empty_locs(board)
        self.solve(0, board)

    def get_empty_locs(self, board):
        res = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    res.append((i, j))
        return res

    # k is index in the self.empty_locs which indicates that the kth empty loc has to be solved
    def solve(self, k, board):
        # only after filling all empty locations should you check 
        if k == len(self.empty_locs):
            # we dont need to check if everything is solved because when it comes to filling the last empty location there would have been only one option 
            # return self.is_fully_solved(board)
            
            return True
            

        # we are trying to solve the kth empty loc
        i, j = self.empty_locs[k] 

        # get candidate values for this spot based on the current state of the board
        candidate_values = self.get_loc_candidates(i, j, board)

        for candidate in candidate_values:
            # try adding it
            board[i][j] = candidate

            # check if it is a success down this path
            if self.solve(k + 1, board):
                return True

            # if not remove it 
            board[i][j] = '.'

        return False

    # THIS IS THE BOTTLENECK
    def get_loc_candidates(self, i, j, board):
        candidates = {str(i) for i in range(1,10)}

        # go through the row and discard
        for J in range(9):
            candidates.discard(board[i][J])

        # go through the column and discard
        for I in range(9):
            candidates.discard(board[I][j])

        # go through that square and discard
        sqI, sqJ = i // 3, j // 3
        for I in range(3*sqI, 3*sqI + 3):
            for J in range(3*sqJ, 3*sqJ + 3):
                candidates.discard(board[I][J])

        return candidates
   
   # Technically not needed at all !
    def is_fully_solved(self, board):
        # check if all rows
        for r in range(9):
            row = []
            for j in range(9):
                row.append(board[r][j])

            if not self.check_collection(row):
                return False

        # check all cols
        for c in range(9):
            col = []
            for i in range(9):
                col.append(board[i][c])
                
            if not self.check_collection(col):
                return False

        # check all squares
        for sq in range(9):
            sqI = sq // 3
            sqJ = sq % 3
            box = []

            for i in range(3*sqI, 3*sqI + 3):
                for j in range(3*sqJ, 3*sqJ + 3):
                    box.append(board[i][j])
            
            if not self.check_collection(box):
                return False

        return True

    def check_collection(self, collection):
        left = {str(i) for i in range(1,10)}
        
        for item in collection:
            left.discard(item)

        return len(left) == 0