import joblib
import numpy as np

class ThreatModel:

    def __init__(self, model_path="../models/threat_model.pkl", scaler_path="../models/scaler.pkl"):
        """
        Load trained model and scaler
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def preprocess(self, features):
        """
        Prepare incoming network features for prediction
        """
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        return features_scaled

    def predict(self, features):
        """
        Predict threat probability
        """
        processed = self.preprocess(features)

        probability = self.model.predict_proba(processed)[0][1]
        prediction = self.model.predict(processed)[0]

        return {
            "prediction": prediction,
            "threat_probability": probability
        }