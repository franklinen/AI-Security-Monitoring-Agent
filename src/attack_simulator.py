import numpy as np

def simulate_attack():

    attack_type = np.random.choice([
        "brute_force",
        "port_scan",
        "data_exfiltration"
    ])

    if attack_type == "brute_force":
        return {
            "failed_logins": np.random.randint(6,15),
            "ip_risk": np.random.uniform(0.6,1),
            "off_hours": 1,
            "unusual_port": 0,
            "data_transfer_volume": np.random.uniform(0,0.2),
            "location_change": 1,
            "label":1
        }

    elif attack_type == "port_scan":
        return {
            "failed_logins": np.random.randint(1,4),
            "ip_risk": np.random.uniform(0.5,0.9),
            "off_hours": np.random.binomial(1,0.5),
            "unusual_port": 1,
            "data_transfer_volume": np.random.uniform(0,0.3),
            "location_change":0,
            "label":1
        }

    else:  # data exfiltration
        return {
            "failed_logins": np.random.randint(0,3),
            "ip_risk": np.random.uniform(0.4,0.8),
            "off_hours":1,
            "unusual_port":0,
            "data_transfer_volume":np.random.uniform(0.7,1),
            "location_change":1,
            "label":1
        }