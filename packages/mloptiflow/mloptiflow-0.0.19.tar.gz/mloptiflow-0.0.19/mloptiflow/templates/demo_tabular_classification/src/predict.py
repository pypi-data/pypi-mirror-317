"""
Minimalistic demo example for a tabular classification paradigm (predict.py).
"""


import joblib
import logging
import logging.config
from pathlib import Path
from typing import Optional, Any, Dict, Union, List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer

try:
    from logger.logger import LOGGING_CONFIG
except ImportError:
    from mloptiflow.templates.demo_tabular_classification.logger.logger_config import (
        LOGGING_CONFIG,
    )


logging.config.dictConfig(LOGGING_CONFIG)


class PredictionError(Exception):
    pass


class ModelPredictor:
    def __init__(self, model_dir: str = "out/models"):
        self.model_dir = Path(model_dir)
        self.model: Optional[BaseEstimator] = None
        self.scaler: Optional[StandardScaler] = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        try:
            self.model = joblib.load(self.model_dir / "XGBoost_model.joblib")  # TODO:
            self.scaler = joblib.load(self.model_dir / "scaler.joblib")  # TODO:
        except Exception as e:
            logging.error(f"Failed to load model artifacts: {str(e)}")
            raise PredictionError(f"Failed to load model artifacts: {str(e)}") from e

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        try:
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X, columns=self.model.feature_names_in_)

            X_scaled = self.scaler.transform(X)

            y_pred = self.model.predict(X_scaled)
            y_pred_proba = self.model.predict_proba(X_scaled)

            return {
                "predictions": y_pred,
                "probabilities": y_pred_proba,
                "prediction_classes": self.model.classes_,
            }
        except Exception as e:
            logging.error(f"Failed to make predictions: {str(e)}")
            raise PredictionError(f"Failed to make predictions: {str(e)}") from e

    def predict_single(self, features: List[float]) -> Dict[str, Any]:
        try:
            X = np.array(features).reshape(1, -1)
            X_scaled = self.scaler.transform(X)
            y_pred = self.model.predict(X_scaled)
            y_pred_proba = self.model.predict_proba(X_scaled)

            return {
                "prediction": y_pred[0],
                "probability": y_pred_proba[0],
                "classes": self.model.classes_,
            }
        except Exception as e:
            logging.error(f"Failed to make single prediction: {str(e)}")
            raise PredictionError(f"Failed to make single prediction: {str(e)}") from e


def main():
    try:
        predictor = ModelPredictor()
        example_features = load_breast_cancer().data[0]
        result = predictor.predict_single(example_features)

        print("\nPrediction Results:")
        print(f"Predicted Class: {result['prediction']}")
        print(f"Class Probabilities: {result['probability']}")
        print(f"Classes: {result['classes']}")

    except Exception as e:
        logging.error(f"Error in prediction pipeline: {str(e)}")
        raise


if __name__ == "__main__":
    main()
