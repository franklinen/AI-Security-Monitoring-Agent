"""
bayesian_reasoner.py – Bayesian Network for contextual threat reasoning.

WHY THIS EXISTS
---------------
The Random Forest gives us a raw threat *probability* from statistical
patterns in the training data.  But it treats every event independently
and has no way to incorporate domain knowledge about how features relate
conditionally.

The Bayesian Network adds a second reasoning layer that asks:
  "Given what we already know about IP reputation AND the time of day,
   how much should we adjust our confidence that this is truly an attack?"

This satisfies the assignment requirement for an approved AI technique
(Bayesian networks) beyond supervised ML alone.

NETWORK STRUCTURE
-----------------
  ip_risk  off_hours
      \       /
       \     /
     [ThreatContext]     <-- hidden node (high_risk / low_risk context)
           |
    [ML_Prediction]      <-- observed node (threat_prob from Random Forest)
           |
       [FinalRisk]       <-- query node (posterior probability)

We use a hand-specified CPT (Conditional Probability Table) approach
rather than learning from data, which is valid for Bayesian networks
and common in security domain models where expert knowledge is available.
"""

import numpy as np


class BayesianReasoner:
    """
    A discrete Bayesian Network with three nodes:

    1. ThreatContext  – prior based on ip_risk and off_hours
    2. ML_Signal      – likelihood of the Random Forest output given context
    3. FinalRisk      – posterior probability of a genuine threat

    States: HIGH_RISK / LOW_RISK (binary for clarity)
    """

    def __init__(self):
        # ── Prior: P(ThreatContext = HIGH_RISK | ip_risk, off_hours) ──────────
        # These CPT values encode expert domain knowledge:
        #   high ip_risk + off_hours  → very likely malicious context
        #   low  ip_risk + on_hours   → very likely benign context
        self.prior_cpt = {
            (1, 1): 0.85,   # high ip_risk, off-hours  → P(HIGH_RISK)
            (1, 0): 0.65,   # high ip_risk, on-hours
            (0, 1): 0.40,   # low  ip_risk, off-hours
            (0, 0): 0.10,   # low  ip_risk, on-hours
        }

        # ── Likelihood: P(ML_Signal = POSITIVE | ThreatContext) ────────────────
        # How likely is it that the ML model fires given the true context?
        #   If context IS high-risk, model should fire with high probability.
        #   If context is low-risk, model may still fire (false positives).
        self.likelihood_cpt = {
            "HIGH_RISK": 0.92,   # P(ML fires | true high-risk context)
            "LOW_RISK" : 0.08,   # P(ML fires | true low-risk context)  ← false positive rate
        }

    def _context_prior(self, ip_risk: float, off_hours: int) -> float:
        """
        Compute P(ThreatContext = HIGH_RISK) from the CPT.
        Discretises continuous ip_risk using threshold of 0.6.
        """
        ip_high = 1 if ip_risk >= 0.6 else 0
        return self.prior_cpt[(ip_high, off_hours)]

    def posterior(self, percept, ml_threat_prob: float) -> float:
        """
        Compute posterior P(ThreatContext = HIGH_RISK | ML_signal, ip_risk, off_hours)
        using Bayes' theorem.

        Parameters
        ----------
        percept         : SecurityPercept
        ml_threat_prob  : float  – probability output from the Random Forest

        Returns
        -------
        float – posterior probability that this is a genuine threat (0-1)
        """
        # Safeguard: clamp ML probability to avoid log(0) issues
        ml_threat_prob = float(np.clip(ml_threat_prob, 1e-6, 1 - 1e-6))

        # Prior
        p_high = self._context_prior(percept.ip_risk, percept.off_hours)
        p_low  = 1.0 - p_high

        # Likelihood of the ML signal under each hypothesis
        # We treat ml_threat_prob itself as a soft likelihood signal
        p_ml_given_high = (
            self.likelihood_cpt["HIGH_RISK"] * ml_threat_prob
            + (1 - self.likelihood_cpt["HIGH_RISK"]) * (1 - ml_threat_prob)
        )
        p_ml_given_low = (
            self.likelihood_cpt["LOW_RISK"] * ml_threat_prob
            + (1 - self.likelihood_cpt["LOW_RISK"]) * (1 - ml_threat_prob)
        )

        # Bayes' theorem: posterior ∝ likelihood × prior
        numerator   = p_ml_given_high * p_high
        denominator = numerator + p_ml_given_low * p_low

        if denominator == 0:
            return 0.0

        posterior_prob = numerator / denominator

        # Additional boost for high data exfiltration (domain rule)
        if percept.data_transfer_volume > 0.6:
            posterior_prob = min(1.0, posterior_prob * 1.15)

        return float(posterior_prob)
