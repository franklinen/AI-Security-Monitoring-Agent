import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score


def evaluate(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)


def plot_learning_curve(reward_history):

    cumulative_reward = np.cumsum(reward_history)

    plt.figure(figsize=(8,5))

    plt.plot(cumulative_reward)

    plt.title("Agent Learning Curve")

    plt.xlabel("Time Step")

    plt.ylabel("Cumulative Reward")

    plt.grid(True)

    plt.savefig("results/learning_curve.png")

    plt.show()