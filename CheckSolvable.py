import numpy as np
import UpdateBoard as UB

# Colors: 
black = 0
red = 1
green = 2
qblue = 3
magenta = 4

colors = [red, green, qblue, magenta] # The colors used in the game

# Returns the entire group of a specific block in a set
def return_group(board, x, y):
    # Get color of position
    color = board[y][x]

    # Returns nothing if the checked block is black
    if color == black:
        return 

    rows, cols = board.shape

    # A list that will contain all the blockpositions part of the group
    group = set()
    # A stack to do a depth-first search of the board
    stack = [(y, x)]

    # All the directions that need to be checked
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while len(stack) > 0:
        # Get y, x from the stack
        y, x = stack.pop()

        # If they are already stated as in the list containing the group, we can skip the next steps
        if (y, x) in group:
            continue

        # Add the y, x to the list containing the group
        group.add((y, x))

        # Check for each direction if 
        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            if ((0 <= ny < rows) and (0 <= nx < cols)) and ((board[ny][nx] == color) and ((ny, nx) not in group)):
                stack.append((ny, nx))

    return group


def return_all_groups(board):
    # Eerst checken of een blokje al in een groep zit
    lst = []

    rows, cols = board.shape

    for y in range(rows):
        for x in range(cols):
            group_y_x = return_group(board, x, y)
            if group_y_x not in lst and group_y_x:
                lst.append(group_y_x)

    return [group for group in lst if len(group) > 1]


def backtrack(board):
    # Returns True if an empty board is found
    if np.all(board == 0):
        return True
    
    groups = return_all_groups(board)
    
    # Returns False if there are no groups on the board
    if not groups:
        return False
    
    for group in groups:
        # Make a copy to keep the previous board
        new_board = board.copy()

        for position in group:
            new_board[position[0], position[1]] = black

        new_board = UB.update_board(new_board)

        # Returns true if a solved board was found in a deeper layer
        if backtrack(new_board):
            return True
        
    return False
