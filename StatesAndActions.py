import numpy as np
import CheckSolvable as cs
import UpdateBoard as ub

black = 0

# Function that returns a list of all the possible actions for the Q-table
def actions(board):

    # Get the number of rows and columns
    rows, cols = board.shape

    # List that will be returned with all the possible actions
    lst = []

    for row in range(rows):
        for col in range(cols):
            action = (row, col)
            lst.append(action)

    return lst


# Function that returns a list of all the possible states for the Q-table
def backtrack(board, lst=[]):
    # Adds board to possible states
    if not any(np.array_equal(board, i) for i in lst):
        lst.append(board)

    # Returns if an empty board is found
    if np.all(board == 0):
        return
    
    groups = cs.return_all_groups(board)
    
    # Returns if there are no groups on the board
    if not groups:
        return
    
    for group in groups:
        # Make a copy to keep the previous board
        new_board = board.copy()

        for position in group:
            new_board[position[0], position[1]] = black

        new_board = ub.update_board(new_board)

        backtrack(new_board, lst)
        

def states(board):
    lst = []
    backtrack(board, lst)
    return lst