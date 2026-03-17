import numpy as np
import pandas as pd

np.random.seed(42)

def generate_security_logs(n_samples=5000):

    data = []

    for _ in range(n_samples):

        failed_logins = np.random.poisson(1)
        ip_risk = np.random.beta(2, 8)
        off_hours = np.random.binomial(1, 0.2)
        unusual_port = np.random.binomial(1, 0.1)

        risk_score = (
            0.4 * (failed_logins > 3)
            + 0.3 * (ip_risk > 0.7)
            + 0.2 * off_hours
            + 0.3 * unusual_port
        )

        label = 1 if risk_score > 0.5 else 0

        data.append([
            failed_logins,
            ip_risk,
            off_hours,
            unusual_port,
            label
        ])

    columns = [
        "failed_logins",
        "ip_risk",
        "off_hours",
        "unusual_port",
        "label"
    ]

    return pd.DataFrame(data, columns=columns)


if __name__ == "__main__":

    df = generate_security_logs()

    df.to_csv("data/logs.csv", index=False)

    print("Dataset saved to data/logs.csv")