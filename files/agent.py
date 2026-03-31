"""
agent.py – Core intelligent security agent.

ARCHITECTURE
------------
The SecurityAgent implements a Perception → Reasoning → Action loop:

  1. perceive()  – converts raw log dict into a typed SecurityPercept
  2. decide()    – two-stage reasoning:
       Stage 1: Random Forest (threat_model) → raw threat probability
       Stage 2: Bayesian Network (bayesian_reasoner) → calibrated posterior
  3. act()       – maps posterior to a tiered security action with safeguards

SAFEGUARDS
----------
  (a) Input validation  – malformed or out-of-range percepts are rejected
      before reaching either model, preventing adversarial log injection.
  (b) Confidence threshold  – agent only acts autonomously for BLOCK_IP
      above 0.85 posterior; events in the 0.65-0.85 band escalate to a
      human analyst (ALERT_ADMIN) rather than automated blocking.
  (c) Rate limiting  – the agent tracks how many BLOCK_IP actions it has
      issued in the current session and refuses to exceed MAX_BLOCKS,
      preventing runaway automated blocking of legitimate traffic.
  (d) Memory / audit log  – every decision is logged with full reasoning
      trace for post-incident review.
"""

from percepts import SecurityPercept
from bayesian_reasoner import BayesianReasoner
from actions import execute_action, ActionResult


# ── Decision thresholds ───────────────────────────────────────────────────────
THRESHOLD_BLOCK       = 0.85   # posterior >= this → BLOCK_IP  (automated)
THRESHOLD_ALERT       = 0.65   # posterior >= this → ALERT_ADMIN
THRESHOLD_INVESTIGATE = 0.40   # posterior >= this → INVESTIGATE
# below 0.40 → IGNORE

MAX_BLOCKS_PER_SESSION = 50    # safeguard: cap autonomous blocking


class SecurityAgent:
    """
    Intelligent security agent combining a machine learning threat detector
    (Random Forest) with a Bayesian network for contextual reasoning.
    """

    def __init__(self, threat_model):
        """
        Parameters
        ----------
        threat_model : ThreatModel  – trained Random Forest wrapper
        """
        self.model    = threat_model
        self.reasoner = BayesianReasoner()
        self.memory   = []          # audit log of all decisions
        self._block_count = 0       # safeguard: rate limit counter

    # ── Perception ────────────────────────────────────────────────────────────

    def perceive(self, event: dict) -> SecurityPercept:
        """
        Convert a raw log event dict into a validated SecurityPercept.

        SAFEGUARD (a): validates all features are present and within
        expected ranges before any model inference is performed.

        Raises
        ------
        ValueError  if required features are missing or clearly out of range
        """
        required = SecurityPercept.FEATURE_NAMES
        missing = [k for k in required if k not in event]
        if missing:
            raise ValueError(
                f"[SAFEGUARD] Input validation failed — missing features: {missing}. "
                f"Possible adversarial log injection attempt."
            )

        # Range checks (domain-knowledge bounds)
        ip_risk = float(event["ip_risk"])
        dtv     = float(event["data_transfer_volume"])
        if not (0.0 <= ip_risk <= 1.0):
            raise ValueError(f"[SAFEGUARD] ip_risk={ip_risk} out of range [0,1].")
        if not (0.0 <= dtv <= 1.0):
            raise ValueError(f"[SAFEGUARD] data_transfer_volume={dtv} out of range [0,1].")

        return SecurityPercept(
            failed_logins        = int(event["failed_logins"]),
            ip_risk              = ip_risk,
            off_hours            = int(event["off_hours"]),
            unusual_port         = int(event["unusual_port"]),
            data_transfer_volume = dtv,
            location_change      = int(event["location_change"]),
        )

    # ── Reasoning ─────────────────────────────────────────────────────────────

    def decide(self, percept: SecurityPercept) -> str:
        """
        Two-stage reasoning pipeline.

        Stage 1 – Random Forest
            Produces a raw threat probability from statistical patterns
            learned from training data.

        Stage 2 – Bayesian Network
            Refines the probability using conditional domain knowledge
            (IP reputation, time-of-day context) to produce a calibrated
            posterior probability of a genuine threat.

        SAFEGUARD (b): confidence thresholding — automated blocking only
        above 0.85; lower-confidence events escalate to human review.

        SAFEGUARD (c): rate limiting — BLOCK_IP capped at MAX_BLOCKS_PER_SESSION.

        Returns
        -------
        str – action name: BLOCK_IP / ALERT_ADMIN / INVESTIGATE / IGNORE
        """
        # Stage 1: ML model
        ml_output      = self.model.predict(percept.to_feature_vector())
        ml_prob        = ml_output["threat_probability"]

        # Stage 2: Bayesian Network
        posterior_prob = self.reasoner.posterior(percept, ml_prob)

        # Decision policy (thresholded)
        if posterior_prob >= THRESHOLD_BLOCK:
            if self._block_count >= MAX_BLOCKS_PER_SESSION:
                # SAFEGUARD (c): rate limit hit — escalate instead of blocking
                action_name = "ALERT_ADMIN"
            else:
                action_name = "BLOCK_IP"
                self._block_count += 1
        elif posterior_prob >= THRESHOLD_ALERT:
            action_name = "ALERT_ADMIN"
        elif posterior_prob >= THRESHOLD_INVESTIGATE:
            action_name = "INVESTIGATE"
        else:
            action_name = "IGNORE"

        # Record decision in audit memory (safeguard d)
        self.memory.append({
            "percept"        : repr(percept),
            "ml_probability" : round(ml_prob, 4),
            "posterior"      : round(posterior_prob, 4),
            "action"         : action_name,
        })

        return action_name

    # ── Action ────────────────────────────────────────────────────────────────

    def act(self, action_name: str, percept: SecurityPercept) -> ActionResult:
        """Execute the chosen action and return a structured ActionResult."""
        return execute_action(action_name, percept)

    # ── Utilities ─────────────────────────────────────────────────────────────

    def get_audit_log(self):
        """Return the full decision audit log."""
        return self.memory

    def print_summary(self):
        """Print a summary of all actions taken this session."""
        from collections import Counter
        actions = Counter(entry["action"] for entry in self.memory)
        print("\n── Agent Session Summary ──────────────────────────")
        print(f"  Total events processed : {len(self.memory)}")
        for action, count in sorted(actions.items()):
            print(f"  {action:<20}: {count}")
        print(f"  Autonomous blocks issued: {self._block_count} / {MAX_BLOCKS_PER_SESSION}")
        print("───────────────────────────────────────────────────\n")
