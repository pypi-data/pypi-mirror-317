from pydantic import BaseModel
from typing import List


class PredictionInput(BaseModel):
    features: List[float]


class PredictionResponse(BaseModel):
    predicted_class: int
    class_probabilities: List[float]
    classes: List[int]
