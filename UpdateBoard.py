import numpy as np

# Colors: 
black = 0
red = 1
green = 2
qblue = 3
magenta = 4

colors = [red, green, qblue, magenta] # The colors used in the game


# Drops the blocks using gravity rule
def apply_gravity(board, rows, cols):
    for x in range(cols):
        lst = []

        # Makes list of column x of te board
        for y in range(rows):
            lst.append(board[y][x])
            has_black = black in lst

        # Removes all the black blocks from the column
        while has_black:
            lst.remove(black)
            has_black = black in lst

        # Adds the number of removed black blocks to the top of the column
        for i in range(rows - len(lst)):
            lst.insert(0, black)

        # Updates the matrix with the updated column x
        for y in range(rows):
            board[y][x] = lst[y]

    return board


# Shifts columns left of an empty column to the right
def shift_columns(board, rows, cols):
    # Create empty column (column full of black blocks)
    empty_column = np.zeros(rows, dtype=int)

    for x in range(cols):
        column = board[0:rows, x]

        # Checks if column x is an empty column
        if np.array_equal(column, empty_column):

            # Removes the empty column from the board and adds an empty column to the left of the matrix
            board = np.delete(board, x, 1)
            board = np.insert(board, 0, np.zeros(rows, dtype=int), axis=1)

    return board


# Updates the board using the gravity rule and empty column rule
def update_board(board):

    # Get the number of rows and the numbers of columns
    rows, cols = board.shape

    board_copy = board.copy()

    # Apply the gravity rule first
    new_board = apply_gravity(board_copy, rows, cols)

    # Then shift the columns left of the empty column to the right
    new_board2 = shift_columns(new_board, rows, cols)

    return new_board2