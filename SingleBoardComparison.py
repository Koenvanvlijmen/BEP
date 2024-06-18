import time

start_time = time.time()

from Qlearning import QLearning
from GymEnvironment import SameGameEnv
import GenerateBoard as gb
import numpy as np

# Heuristic that plays moves randomly
def random_predict(env):
    # Sample a random action
    action = env.action_space.sample()

    # Masking
    while action in env.not_playable():
        action = env.action_space.sample()

    return action

# Constants
colors = [1, 2, 3, 4]
test_size = 250

# To keep track of accuracy
reward_qlearning = []
reward_random = []

# Train and play on the generated boards
for i in range(test_size):
    # Progress check
    print((i + 1) / test_size)

    board = gb.create_board(4, 4, colors)

    samegame = SameGameEnv(board, len(colors))
    samegame.reset()

    q_table = np.zeros((0, 16))
    state_index = dict()

    # Initiate Q-learning class
    model = QLearning(lr=0.2, df=0.6, exploration_prob=0.9, epochs= 1000)

    # Update State Index
    state_index.update(model.set_q_table(samegame, q_table, state_index)[1])

    # Train the model
    q_table = model.learn(samegame, state_index)

    state = samegame.reset()

    # Play game using Q-learning
    done = False
    while not done:
        action = model.predict(state, samegame, state_index, q_table)
        state, reward, done = samegame.step(action)
        
        if reward != 0:
            reward_qlearning.append(reward)

    # Reset the game
    samegame.reset()

    # Play game as Heuristic
    done = False
    while not done:
        action = random_predict(samegame)
        state, reward, done = samegame.step(action)

        if reward != 0:
            reward_random.append(reward)



print("Average reward Q-learning:", np.mean(reward_qlearning), "Accuracy Q-learning:", reward_qlearning.count(10)/test_size)
print("Average reward Heurstic Random:", np.mean(reward_random), "Accuracy Heurstic Random:", reward_random.count(10)/test_size)
        

print("--- %s seconds ---" % (time.time() - start_time))