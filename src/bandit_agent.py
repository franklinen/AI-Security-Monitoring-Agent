import numpy as np

class SecurityBanditAgent:

    def __init__(self, n_features, epsilon=0.1):

        self.epsilon = epsilon
        self.n_actions = 2
        self.weights = np.zeros((self.n_actions, n_features))

    def predict(self, state):

        values = self.weights @ state
        return np.argmax(values)

    def select_action(self, state):

        if np.random.rand() < self.epsilon:
            return np.random.randint(self.n_actions)

        return self.predict(state)

    def update(self, state, action, reward, lr=0.01):

        self.weights[action] += lr * reward * state