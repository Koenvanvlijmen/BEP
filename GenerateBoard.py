# import time
# start_time = time.time()

import numpy as np
import random
import CheckSolvable as CS

# Colors: 
black = 0
red = 1
green = 2
qblue = 3
magenta = 4

colors = [red, green, qblue, magenta] # The colors used in the game


# Generates a solvable filled board
def create_board(rows, cols, colors):

    solvable = False

    # Loop that will generate filled boards until a solvable board is found
    while solvable == False:

        # 'Randomly' generate r x c matrix filled with color values
        board = np.zeros((rows, cols), dtype=int)
    
        for row in range(rows):
            for column in range(cols):
                board[row, column] = random.choice(colors)

        # Checks if the generated board is solvable
        solvable = CS.backtrack(board)

    return board

# board = create_board(10, 10, colors)
# board.tofile('board.dat')

# print("--- %s seconds ---" % (time.time() - start_time))