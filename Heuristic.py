def random_predict(env):
    # Sample a random action
    action = env.action_space.sample()

    # Masking
    while action in env.not_playable():
        action = env.action_space.sample()

    return action

import numpy as np
