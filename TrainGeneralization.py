import time

start_time = time.time()

from Qlearning import QLearning
from GymEnvironment import SameGameEnv
import GenerateBoard as gb
import numpy as np
from Heuristic import random_predict

colors = [1, 2, 3, 4]

# Initialise Q-Table
q_table = np.zeros((0, 16))

state_index = dict()

tel = 0

train_size = 2500
test_size = 25

# To keep track of accuracy
reward_qlearning = []
reward_random = []

# Training the model on a lot of boards
for i in range(train_size):
    # Print to show progress in training
    if round(((1 + i) / train_size) % 0.01, ndigits=3) == 0:
        print((1 + i) / train_size)
    
    # Create new board
    board = gb.create_board(4, 4, colors)
    # Initiate the environment
    samegame = SameGameEnv(board, len(colors))
    samegame.reset()

    # Initiate Q-learning class
    model = QLearning(lr=0.2, df=0.6, exploration_prob=0.9, epochs= 1000)

    # Update State Index
    state_index.update(model.set_q_table(samegame, q_table, state_index)[1])

    # Train the model
    q_table = model.learn(samegame, state_index)

    tel += model.nr_states - len(model.state_index)

    samegame.reset()

# Shows how many states have been seen before, not counting the empty board state
print(tel - train_size)


# testing the model on x boards
for i in range(test_size):
    board = gb.create_board(4, 4, colors)
    samegame = SameGameEnv(board, len(colors))
    samegame.reset()

    # Initiate Q-learning class
    model = QLearning(lr=0.2, df=0.6, exploration_prob=0.9, epochs= 1000)

    # Update q_table and State Index
    q_table, added_indexes = model.set_q_table(samegame, q_table, state_index)
    state_index.update(added_indexes)

    state = samegame.reset()

    # Plays game using Q-learning until the board is empty or not solvable anymore
    done = False
    print("Nieuw bord!", i + 1)
    while not done:
        samegame.render()
        action = model.predict(state, samegame, state_index, q_table)
        state, reward, done = samegame.step(action)
    samegame.render()
    
    # Keeps track of rewards to calculate evaluation
    if reward != 0:
        reward_qlearning.append(reward)

    samegame.reset()

    # Plays a game until the board is empty or not solvable anymore
    done = False
    while not done:
        action = random_predict(samegame)
        state, reward, done = samegame.step(action)

    # Keeps track of rewards to calculate evaluation
    if reward != 0:
        reward_random.append(reward)

print("Average reward Q-learning:", np.mean(reward_qlearning), "Winrate Q-learning:", reward_qlearning.count(10)/test_size)
print("Average reward Heurstic Random:", np.mean(reward_random), "Winrate Heurstic Random:", reward_random.count(10)/test_size)

print(q_table.shape)

# saved_table = q_table.copy()
# saved_table.tofile('q_table.dat')

print("--- %s seconds ---" % (time.time() - start_time))