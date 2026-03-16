import numpy as np
class UCBAgent:

    def __init__(self, n_actions=2):

        self.counts = np.zeros(n_actions)
        self.values = np.zeros(n_actions)
        self.total_steps = 0

    def select_action(self):

        self.total_steps += 1

        for a in range(len(self.counts)):
            if self.counts[a] == 0:
                return a

        ucb_values = self.values + np.sqrt(
            (2*np.log(self.total_steps)) / self.counts
        )

        return np.argmax(ucb_values)

    def update(self, action, reward):

        self.counts[action] += 1

        n = self.counts[action]

        value = self.values[action]

        self.values[action] = value + (reward-value)/n