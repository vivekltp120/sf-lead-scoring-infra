# inference.py
import os, json, joblib, numpy as np

def model_fn(model_dir):
    path = os.path.join(model_dir, "model.pkl")
    return joblib.load(path)

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
