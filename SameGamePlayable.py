import pygame, random

# Constants
width = 640
height = 480
rows = 4
cols = 4
block_size = min(width//cols, height//rows) # Makes sure the board is filled with blocks either in the length or the width
seed = 1204 # Seed is chosen to let the Q-learning get the same board over and over again
# seed = 1

# Colors:  R    G    B
black   = (0,     0,   0)
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
qblue   = (  0, 163, 232)
magenta = (255,   0, 255)

colors = [red, green, qblue, magenta] # The colors used in the game

# Initializes Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SameGame')

# Generates a filled board
def create_board(): 
    random.seed(seed)

    # 'Randomly' generate a rows x columns matrix filled with color values
    return [[random.choice(colors) for i in range(cols)] for j in range(rows)]


# Create visual of board
def draw_board(board):
    for y in range(rows):
        for x in range (cols):
            pygame.draw.rect(screen, board[y][x], (x * block_size, y * block_size, block_size, block_size))


# Checks if block is allowed to be clicked and returns the neigbours
def check_click(board, x, y):
    neighbours = []

    # If not left most column, then check block on the left
    if x > 0:
        neighbours.append(board[y][x - 1])

    # If not right most column, then check block on the right
    if x < cols - 1:
        neighbours.append(board[y][x + 1])

    # If not the upper row, then check block above
    if y > 0:
        neighbours.append(board[y -1][x])

    # If not lowwer row, then check block under
    if y < rows - 1:
        neighbours.append(board[y + 1][x])

    return board[y][x] in neighbours, neighbours


# Removes connected blocks from te playing field
def click_block(board, x, y, color):
    # Checks if inputted x,y are in bound, has the same color as the clicked block and not already empty
    if x < 0 or x >= cols or y < 0 or y >= rows or board[y][x] != color or board[y][x] == black:
        return
    
    else:
        # Removes block from te board
        board[y][x] = black

        # Recursively calls itself to remove connected blocks of the same color
        click_block(board, x + 1, y, color)
        click_block(board, x - 1, y, color)
        click_block(board, x, y + 1, color)
        click_block(board, x, y -1, color)


# Drops the blocks using gravity rule
def apply_gravity(board):
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
def shift_columns(board):
    # Create empty column (column full of black blocks)
    empty_column = rows * [(0, 0, 0)]

    for x in range(cols):
        column = []

        # Makes list of column x of the board
        for y in range(rows):
            column.append(board[y][x])

        # Checks if column x is an empty column
        if column == empty_column:

            # Removes the empty column from the board and adds an empty column to the left of the matrix
            for i in range(rows):
                board[i].pop(x)
                board[i].insert(0, black)

    return board


# Updates the board using the gravity rule and empty column rule
def update_board(board):
    # Apply the gravity rule first
    new_board = apply_gravity(board)

    # Then shift the columns left of the empty column to the right
    new_board = shift_columns(new_board)

    return new_board


# Ends the game if it there are no clickable blocks anymore
def game_over(board):
    for y in range(rows):
        for x in range(cols):
            if (board[y][x] in check_click(board, x, y)[1]) and (board[y][x] != black):
                return False
    else:
        return True
    
    
# Returns the entire group of a specific block in a set
def return_group(board, x, y, color):
    # Returns nothing if the checked block is black
    if color == black:
        return

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

    for y in range(rows):
        for x in range(cols):
            group_y_x = return_group(board, x, y, board[y][x])
            if group_y_x not in lst and group_y_x:
                lst.append(group_y_x)

    return [group for group in lst if len(group) > 1]
    

# Checks if the generated board is solvable
def check_solvable(board, count=0):

    # create empty board to know when a game is finished
    empty_row = cols * [black]
    empty_board = rows * [empty_row]

    # Get all the groups on a given board
    groups = return_all_groups(board)
    print(groups)

    for group in groups:
        # chooses a arbitrary block from a group to click
        # print(group)
        y, x = group.pop()
        new_board = board.copy()
        if x < cols and y < rows and check_click(new_board, x, y)[0]:
            click_block(new_board, x, y, new_board[y][x])
        
            # Updates the board (applies the gravity and shifting rules)
            new_board2 = update_board(new_board)

        # If solution to the game is found, then and the search and return True
        if new_board2 == empty_board:
            return True
    
        # If the game state is game over, than continue to check for other blocks
        if game_over(new_board2):
            continue

        # Checks if the new board is solvable
        check_solvable(new_board2, count)
            
        # new_board = update_board(board)

#############################################################################################################

# Runs the game
def game():
    # Creates the board and initializes the gameloop
    board = create_board()

    running = True

    # Empty board needed to check if the board is empty 
    empty_row = cols * [black]
    empty_board = rows * [empty_row]

    # Runs the gameloop
    while running:
        screen.fill(black)
        draw_board(board)
        pygame.display.flip()

        for event in pygame.event.get():
            # Quits the game if game is closed
            if event.type == pygame.QUIT:
                running = False

            # Processes clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                x, y = x_pos // block_size, y_pos // block_size
                if x < cols and y < rows and check_click(board, x, y)[0]:
                    click_block(board, x, y, board[y][x])
                board = update_board(board)

            # Quit the game if the board is empty
            if board == empty_board:
                running = False
                # still needs to return a reward

            # Quit the game if none of the blocks can be clicked. Has to be after the empty board check because empty places are black blocks
            if game_over(board):
                running = False
                # Still needs to return a reward
                               


if __name__ == "__main__":
    game()
    # board = create_board()
    # print(board)
    # print(check_solvable(board))

# Reward functie toevoegen en showen in de window