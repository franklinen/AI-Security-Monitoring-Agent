import numpy as np
import pandas as pd

np.random.seed(42)

def generate_security_logs(n_samples=5000):
    """
    Generate synthetic network security logs with 6 features.
    Labels are derived from a weighted risk score to simulate realistic attack patterns.
    """
    data = []

    for _ in range(n_samples):
        # Normal baseline traffic features
        failed_logins          = np.random.poisson(1)
        ip_risk                = np.random.beta(2, 8)          # skewed low (most IPs are safe)
        off_hours              = np.random.binomial(1, 0.2)
        unusual_port           = np.random.binomial(1, 0.1)
        data_transfer_volume   = np.random.uniform(0, 0.3)     # normalised 0-1
        location_change        = np.random.binomial(1, 0.05)

        # Risk score used to assign ground-truth label
        risk_score = (
            0.35 * (failed_logins > 3)
            + 0.25 * (ip_risk > 0.7)
            + 0.15 * off_hours
            + 0.20 * unusual_port
            + 0.20 * (data_transfer_volume > 0.6)
            + 0.15 * location_change
        )

        label = 1 if risk_score > 0.4 else 0

        data.append([
            failed_logins,
            ip_risk,
            off_hours,
            unusual_port,
            data_transfer_volume,
            location_change,
            label
        ])

    columns = [
        "failed_logins",
        "ip_risk",
        "off_hours",
        "unusual_port",
        "data_transfer_volume",
        "location_change",
        "label"
    ]

    return pd.DataFrame(data, columns=columns)


if __name__ == "__main__":
    df = generate_security_logs()
    df.to_csv("data/logs.csv", index=False)
    print(f"Dataset saved to data/logs.csv  |  shape: {df.shape}")
    print(df["label"].value_counts().rename({0: "benign", 1: "attack"}))
