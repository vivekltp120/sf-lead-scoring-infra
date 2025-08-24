from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional, Any
import math, os, time
from .utils import get_logger
logger = get_logger("model_service")

# ---- Schemas ----
class ScoreRequest(BaseModel):
    lead_id: str = Field(..., description="Lead identifier")
    features: Dict[str, float] = Field(..., description="50 numeric features")
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("features")
    @classmethod
    def validate_features(cls, v: Dict[str, float]):
        if len(v) < 10:
            # For demo lower the bar; prod would enforce 50 exact features
            raise ValueError("insufficient_features: expected ~50")
        return v

class ScoreResponse(BaseModel):
    lead_id: str
    score: int
    model_version: str
    latency_ms: int

# ---- Service ----
class ModelService:
    def __init__(self):
        self.ready = False
        self.model_version = os.getenv("MODEL_VERSION", "demo-1.0.0")
        # In prod, warm a SageMaker endpoint or load model file from local/S3
        self._weights = self._load_mock_model()
        self.ready = True

    def _load_mock_model(self):
        # Mock "xgboost" weights vector; deterministic and fast
        return {f"f{i}": (i * 0.01 + 0.1) for i in range(1, 51)}

    async def score(self, req: ScoreRequest) -> ScoreResponse:
        if not self.ready:
            raise RuntimeError("model_not_ready")
        t0 = time.perf_counter()
        # Mock scoring: weighted sum -> 1..5 bucket
        s = 0.0
        for k, v in req.features.items():
            w = self._weights.get(k, 0.05)
            s += w * float(v)
        # map to 1-5
        raw = 1 + 4 * (1 / (1 + math.exp(-s)))  # logistic squashing
        score = max(1, min(5, int(round(raw))))
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return ScoreResponse(
            lead_id=req.lead_id,
            score=score,
            model_version=self.model_version,
            latency_ms=latency_ms
        )
