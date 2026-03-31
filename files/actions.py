"""
actions.py – Defines all security actions the agent can take.

Each action represents a different severity level of response.
The agent selects an action based on the combined output of the
Random Forest threat model and the Bayesian network reasoner.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ActionResult:
    """Represents the outcome of a security action."""
    action_name : str
    severity    : str          # LOW / MEDIUM / HIGH / CRITICAL
    timestamp   : str
    details     : str


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── Individual action functions ──────────────────────────────────────────────

def block_ip(percept) -> ActionResult:
    """
    BLOCK_IP – Highest severity response.
    Triggered when both the ML model and Bayesian network agree
    the event is almost certainly malicious (probability > 0.85).
    In a real SOC this would push a firewall rule via API.
    """
    details = (
        f"Blocking source IP. "
        f"ip_risk={percept.ip_risk:.2f}, "
        f"failed_logins={percept.failed_logins}, "
        f"location_change={percept.location_change}"
    )
    return ActionResult("BLOCK_IP", "CRITICAL", _timestamp(), details)


def alert_admin(percept) -> ActionResult:
    """
    ALERT_ADMIN – High severity response.
    Triggered when threat probability is high (0.65-0.85) but not
    conclusive enough to block automatically.
    In a real SOC this would page the on-call analyst.
    """
    details = (
        f"Alerting security team. "
        f"data_transfer={percept.data_transfer_volume:.2f}, "
        f"off_hours={percept.off_hours}, "
        f"unusual_port={percept.unusual_port}"
    )
    return ActionResult("ALERT_ADMIN", "HIGH", _timestamp(), details)


def investigate(percept) -> ActionResult:
    """
    INVESTIGATE – Medium severity response.
    Triggered when the Bayesian network raises contextual concern
    even if the ML probability is moderate (0.40-0.65).
    Queues the event for analyst review without immediate blocking.
    """
    details = (
        f"Flagging for analyst review. "
        f"ip_risk={percept.ip_risk:.2f}, "
        f"off_hours={percept.off_hours}"
    )
    return ActionResult("INVESTIGATE", "MEDIUM", _timestamp(), details)


def ignore(percept) -> ActionResult:
    """
    IGNORE – Low severity / benign.
    Triggered when both the ML model and Bayesian network agree
    the event is normal traffic (probability < 0.40).
    """
    details = "Event within normal parameters. No action required."
    return ActionResult("IGNORE", "LOW", _timestamp(), details)


# ── Action dispatcher ─────────────────────────────────────────────────────────

ACTION_MAP = {
    "BLOCK_IP"    : block_ip,
    "ALERT_ADMIN" : alert_admin,
    "INVESTIGATE" : investigate,
    "IGNORE"      : ignore,
}


def execute_action(action_name: str, percept) -> ActionResult:
    """
    Execute the named action and return an ActionResult.

    Parameters
    ----------
    action_name : str   – one of BLOCK_IP / ALERT_ADMIN / INVESTIGATE / IGNORE
    percept     : SecurityPercept

    Returns
    -------
    ActionResult
    """
    action_fn = ACTION_MAP.get(action_name)
    if action_fn is None:
        raise ValueError(f"Unknown action '{action_name}'. "
                         f"Valid options: {list(ACTION_MAP.keys())}")
    return action_fn(percept)
