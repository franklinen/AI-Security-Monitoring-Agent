"""
threat_model.py – Random Forest threat detection model wrapper.

This class wraps the trained sklearn RandomForestClassifier and handles
all preprocessing (scaling) before inference.

The model is Stage 1 of the agent's two-stage reasoning pipeline.
Its output (threat_probability) feeds directly into the Bayesian Network.
"""

import joblib
import numpy as np


EXPECTED_FEATURE_COUNT = 6   # must match log_generator.py and percepts.py


class ThreatModel:

    def __init__(
        self,
        model_path  = "../models/threat_model.pkl",
        scaler_path = "../models/scaler.pkl"
    ):
        """Load pre-trained Random Forest classifier and its feature scaler."""
        self.model  = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"[ThreatModel] Loaded model from '{model_path}'")

    def preprocess(self, features: list) -> np.ndarray:
        """
        Scale a raw feature vector using the fitted StandardScaler.

        Parameters
        ----------
        features : list of length EXPECTED_FEATURE_COUNT

        Returns
        -------
        np.ndarray  shape (1, EXPECTED_FEATURE_COUNT)
        """
        if len(features) != EXPECTED_FEATURE_COUNT:
            raise ValueError(
                f"Expected {EXPECTED_FEATURE_COUNT} features, got {len(features)}. "
                f"Ensure log_generator.py, percepts.py, and threat_model.py are in sync."
            )
        arr    = np.array(features, dtype=float).reshape(1, -1)
        scaled = self.scaler.transform(arr)
        return scaled

    def predict(self, features: list) -> dict:
        """
        Predict threat probability for a single event.

        Parameters
        ----------
        features : list  – output of SecurityPercept.to_feature_vector()

        Returns
        -------
        dict with keys:
            prediction        : int   – 0 (benign) or 1 (threat)
            threat_probability: float – P(threat) from the Random Forest
        """
        scaled      = self.preprocess(features)
        prediction  = int(self.model.predict(scaled)[0])
        probability = float(self.model.predict_proba(scaled)[0][1])

        return {
            "prediction"        : prediction,
            "threat_probability": probability,
        }
