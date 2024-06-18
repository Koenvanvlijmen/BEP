import numpy as np
import random
import StatesAndActions as sa

class QLearning():

    def __init__(self, lr = 0.1, df = 0.6, exploration_prob = 0.7, epochs = 1000):
        self.lr = lr
        self.df = df
        self.exploration_prob = exploration_prob
        self.epochs = epochs
        self.state_index = dict()
        self.decay = (exploration_prob - 0.1) / self.epochs
    

    def set_q_table(self, env, q_table, state_index):
        self.states = sa.states(env.initialboard) # list of all the possible states
        self.nr_states = len(self.states) # Number of possible states

        self.actions = sa.actions(env.initialboard) # List of all the possible actions
        self.nr_actions = len(self.actions) # Number of possible actions


        # Get the number of states already in the q_table
        q_table_rows = q_table.shape[0]

        # Dictionary to link a state to a row in the q-table
        count = 0
        j = 0
        for i in self.states:
            state_reformat = tuple(map(tuple, self.states[j]))
            if state_reformat not in state_index:
                self.state_index[state_reformat] = q_table_rows + count
                count += 1
            j += 1

        # Dictionary to link an action to a column in the q-table
        self.action_index = dict()
        for i in range(self.nr_actions):
            self.action_index[self.actions[i]] = i

        
        # Add the new states to the q_table
        new_q_table = np.vstack([q_table, np.zeros((count, self.nr_actions))])
        self.q_table = new_q_table

        return self.q_table, self.state_index
    

    def indexing(self, state, state_index):
        return state_index[tuple(map(tuple, state))]


    # mask temporarily all the positions that can not be clicked
    def masking(self, env, q_table):
        copy_q_table = q_table.copy()
        # Get list of all the block coordinates that are not playable
        non_playable_blocks = env.not_playable()
        # Get a list of all the corresponding indexes of the not playable blocks
        indexes = [self.action_index[action] for action in non_playable_blocks]
        # Make all of the columns corresponding to the not playable blocks NaN
        for index in indexes:
            copy_q_table[:,index] = np.nan

        return copy_q_table


    def learn(self, env, state_index):

        for epoch in range(self.epochs):
            state = env.reset()

            done = False

            while not done:
                # Decide whether the algorithm will explore or exploit
                if random.uniform(0, 1) < self.exploration_prob:
                    action = env.action_space.sample()
                    # Masking
                    while action in env.not_playable():
                        action = env.action_space.sample()
                else:
                    # Masking
                    masked_table = self.masking(env, self.q_table.copy())
                    action_values = masked_table[self.indexing(state, state_index)]
                    action_index = np.nanargmax(action_values)
                    # rewrite index to position on the board
                    position = list(self.action_index.values()).index(action_index)
                    action = list(self.action_index.keys())[position]

                next_state, reward, done = env.step(action)

                old_value = self.q_table[self.indexing(state, state_index), self.action_index[action]]
                next_max = np.max(self.q_table[self.indexing(next_state, state_index)])
                new_value = old_value + self.lr * (reward + (self.df * next_max) - old_value)
                self.q_table[self.indexing(state, state_index), self.action_index[action]] = new_value
                state = next_state

            self.exploration_prob = max(0.1, self.exploration_prob - self.decay)

        return self.q_table

    
    def predict(self, state, env, state_index, q_table):
        masked_table = self.masking(env, q_table)
        action_values = masked_table[self.indexing(state, state_index)]
        action_index = np.nanargmax(action_values)
        position = list(self.action_index.values()).index(action_index)
        action = list(self.action_index.keys())[position]
        return action
