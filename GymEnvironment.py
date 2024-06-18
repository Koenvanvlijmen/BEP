import gymnasium as gym
from gymnasium import spaces
import numpy as np
import GenerateBoard as gb
import CheckSolvable as cs
import UpdateBoard as ub


class SameGameEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, board, nr_colors):
        super(SameGameEnv, self).__init__()
        self.initialboard = board
        self.state = board
        self.nr_colors = nr_colors
        self.rows, self.cols = self.initialboard.shape
        self.action_space = spaces.Tuple((spaces.Discrete(self.rows), spaces.Discrete(self.cols)))
        self.observation_space = spaces.Box(low=0, high=nr_colors, shape=(self.initialboard.shape))

        self.done = 0
        self.reward = 0
    

    # Resets the state of the game
    def reset(self):
        self.state = self.initialboard.copy()
        self.done = 0
        self.reward = 0
        return self.state
    

    # Checks whether a given position is part of a group
    def check_block(self, x, y):
        neighbours = []

        # If not left most column, then check block on the left
        if x > 0:
            neighbours.append(self.state[y][x - 1])

        # If not right most column, then check block on the right
        if x < self.cols - 1:
            neighbours.append(self.state[y][x + 1])

        # If not the upper row, then check block above
        if y > 0:
            neighbours.append(self.state[y -1][x])

        # If not lowwer row, then check block under
        if y < self.rows - 1:
            neighbours.append(self.state[y + 1][x])

        return self.state[y][x] in neighbours
    

    # Returns a list of all the blocks not part of a group or black
    def not_playable(self):
        lst = []
        for x in range(self.cols):
            for y in range(self.rows):
                if self.state[y][x] == 0:
                    lst.append((y, x))
                elif self.check_block(x, y) == False:
                    lst.append((y, x))
        return lst
    

    # Checks whether the game is won, lost or can keep on going
    def check(self):
        # Checks if the board is empty and returns 0 if that is the case
        if np.array_equal(self.state, np.zeros(self.initialboard.shape, dtype=int)):
            return 0
        
        # Checks if there are playable groups left on the board and return 1 if there are
        for x in range(self.cols):
            for y in range(self.rows):
                if (self.check_block(x, y) == True) and (self.state[y][x] != 0):
                    return 1
        
        # Returns 2 if it is "game over"
        else:
            return 2


    # Plays a step of the game and returns new state, reward and if we are done
    def step(self, action):
        y, x = action
        state = self.state.copy()
        group = cs.return_group(self.state, x, y)

        # Only plays a move if the selected block is part of a group and not black
        if group != None:
            if len(group) > 1:
                for block in group:
                    y, x = block
                    state[y][x] = 0

                # Update the board using gravity and shifting rules
                new_board = ub.update_board(state)
                self.state = new_board

        # Check the status of the board
        status = self.check()

        if status == 0:
            self.reward += 10
            self.done = 1

        if status == 2:
            self.reward -= 10
            self.done = 1

        return self.state, self.reward, self.done

    # Prints the board
    def render(self):
        print(self.state)
