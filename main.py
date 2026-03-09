import pandas as pd

from src.train_agent import train_agent
from src.evaluate import evaluate, plot_learning_curve


def main():

    df = pd.read_csv("data/security_logs.csv")

    y_true, y_pred, reward_history = train_agent(df)

    evaluate(y_true, y_pred)

    plot_learning_curve(reward_history)


if __name__ == "__main__":

    main()