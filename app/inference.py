# inference.py
import os, json, joblib, numpy as np
import xgboost as xgb
from utils import get_logger
logger = get_logger("inference")

# A recommended filename for the XGBoost model within the tarball is 'xgboost_model.json'
MODEL_FILENAME = "xgboost_model.json"

def model_fn(model_dir):
    path = os.path.join(model_dir, MODEL_FILENAME)
    logger.info(f"Loading model from: {path}")
    # For XGBClassifier
    booster = xgb.XGBClassifier()
    booster.load_model(path)
    logger.info("Model loaded successfully")
    return booster

def input_fn(body, content_type):
    if content_type == "application/json":
        payload = json.loads(body)
        # Expect {"instances":[[...],[...]]}
        arr = np.asarray(payload["instances"], dtype=float)
        return arr
    raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(data, model):
    # For XGBClassifier
    preds = model.predict_proba(data)[:,1]
    return preds

def output_fn(prediction, accept):
    return json.dumps({"predictions": prediction.tolist()})
