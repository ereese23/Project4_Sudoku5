import math,random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length # Set up row length and removed cells
        self.removed_cells = removed_cells
        '''
        This generates nested lists nicely enough. When row_length is 9, it generates a list containing 9 lists of 9 ints (0)
        I couldn't find a simple way to do this without range()
        '''
        self.board = [[0 for i in range(self.row_length)] for i in range(self.row_length)]
        self.box_length = int(math.sqrt(self.row_length)) # Calculate the length of each smaller box, standard is 9, sqrt(9) = 3.

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def get_board(self): # Required according to the project 4 pdf for some provided functions, simple enough.
        return self.board

    def print_board(self):
        for i in range(self.row_length): # Loop through every row, range() makes this fairly simple
            for j in range(self.row_length): # Then loop through every column in each row
                print(self.board[i][j], end=" ") # Print the number
            print() # Move to the next line

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        for i in range(self.row_length): # Loop through each column, range() makes this fairly simple
            if self.board[row][i] == num: # Check if the number is already anywhere in the row at this column, which would mean that num is invalid.
                return False # Return False if invalid
        return True # No issues? Valid enough, return True.
    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num): # this should be similar enough to valid_in_row
        for i in range(self.row_length): # Loop through each row
            if self.board[i][col] == num: # Check if the number is already anywhere in the column
                return False # Return False if invalid
        return True # Return true otherwise

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num): # I'm defining the box
        for i in range(row_start, row_start+3): # The comment says +2, but I think it should be +3 with my implementation, row_start is inclusive, row_start + 2 is 3, the last row start (+3) is exclusive, so we're covering 3 rows
            for j in range(col_start, col_start+3): # Same as above, for columns^
                if self.board[i][j] == num: # Check if our num already exists
                    return False # Return False if it does
        return True # Return true if it doesn't
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row, col, num))

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        num = list(range(1, self.row_length + 1))
        random.shuffle(num)
        num_index = 0

        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = num[num_index]
                num_index += 1

    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)


    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        cells_removed = 0
        num_cells_removed = self.calculate_num_cells_to_removed()

        while cells_removed < self.calculate_num_cells_to_removed():
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.box_length - 1)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_removed += 1

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


