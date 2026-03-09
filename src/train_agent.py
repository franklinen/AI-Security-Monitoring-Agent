import pandas as pd
import numpy as np

from bandit_agent import SecurityBanditAgent

def compute_reward(action, label):

    if action == 1 and label == 1:
        return 5

    elif action == 0 and label == 0:
        return 1

    elif action == 1 and label == 0:
        return -2

    else:
        return -6


def train_agent(df):

    features = [
        "failed_logins",
        "ip_risk",
        "off_hours",
        "unusual_port"
    ]

    agent = SecurityBanditAgent(len(features))

    y_true = []
    y_pred = []
    reward_history = []

    for _, row in df.iterrows():

        state = row[features].values.astype(float)
        label = row["label"]

        action = agent.select_action(state)

        reward = compute_reward(action, label)

        agent.update(state, action, reward)

        y_true.append(label)
        y_pred.append(action)
        reward_history.append(reward)

    return y_true, y_pred, reward_history