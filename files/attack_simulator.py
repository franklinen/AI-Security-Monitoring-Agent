"""
attack_simulator.py – Generates synthetic attack events for live testing.

Previously this module was never called anywhere. It is now used by
run_agent.py in "simulation mode" to inject known-attack events into
the environment stream so the agent's detection can be visually verified.
"""

import numpy as np


ATTACK_TYPES = ["brute_force", "port_scan", "data_exfiltration"]


def simulate_attack(attack_type: str = None) -> dict:
    """
    Generate a synthetic attack event dict.

    Parameters
    ----------
    attack_type : str, optional
        One of 'brute_force', 'port_scan', 'data_exfiltration'.
        If None, a random attack type is chosen.

    Returns
    -------
    dict with the 6 standard feature keys + 'label' + 'attack_type'
    """
    if attack_type is None:
        attack_type = np.random.choice(ATTACK_TYPES)

    if attack_type == "brute_force":
        event = {
            "failed_logins"        : np.random.randint(6, 15),
            "ip_risk"              : np.random.uniform(0.6, 1.0),
            "off_hours"            : 1,
            "unusual_port"         : 0,
            "data_transfer_volume" : np.random.uniform(0.0, 0.2),
            "location_change"      : 1,
        }

    elif attack_type == "port_scan":
        event = {
            "failed_logins"        : np.random.randint(1, 4),
            "ip_risk"              : np.random.uniform(0.5, 0.9),
            "off_hours"            : int(np.random.binomial(1, 0.5)),
            "unusual_port"         : 1,
            "data_transfer_volume" : np.random.uniform(0.0, 0.3),
            "location_change"      : 0,
        }

    else:  # data_exfiltration
        event = {
            "failed_logins"        : np.random.randint(0, 3),
            "ip_risk"              : np.random.uniform(0.4, 0.8),
            "off_hours"            : 1,
            "unusual_port"         : 0,
            "data_transfer_volume" : np.random.uniform(0.7, 1.0),
            "location_change"      : 1,
        }

    event["label"]       = 1
    event["attack_type"] = attack_type
    return event


def simulate_benign() -> dict:
    """Generate a synthetic benign (normal) traffic event."""
    return {
        "failed_logins"        : np.random.randint(0, 2),
        "ip_risk"              : np.random.uniform(0.0, 0.3),
        "off_hours"            : int(np.random.binomial(1, 0.2)),
        "unusual_port"         : 0,
        "data_transfer_volume" : np.random.uniform(0.0, 0.2),
        "location_change"      : 0,
        "label"                : 0,
        "attack_type"          : "none",
    }
