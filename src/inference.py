# inference.py
import os
import json
import numpy as np
import xgboost as xgb


# A recommended filename for the XGBoost model within the tarball is 'xgboost_model.json'
MODEL_FILENAME = "xgboost_model.json"

def model_fn(model_dir):
    path = os.path.join(model_dir, MODEL_FILENAME)
    # For XGBClassifier
    booster = xgb.XGBClassifier()
    booster.load_model(path)
    return booster

def input_fn(body, content_type):
    """
    Parse and convert the input payload to a NumPy array.

    Parameters
    ----------
    body : str
        The request body containing input data, expected to be a JSON-encoded list or array.
    content_type : str
        The MIME type of the input data. Must be "application/json".

    Returns
    -------
    arr : numpy.ndarray
        The input data converted to a NumPy array of type float.

    Raises
    ------
    ValueError
        If the content_type is not "application/json".
    """
    if content_type == "application/json":
        payload = json.loads(body)
        arr = np.asarray(payload, dtype=float)
        return arr
    raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(data, model):
    # For XGBClassifier
    preds = model.predict(data)
    return preds

def output_fn(prediction, accept):
    return json.dumps({"predictions": prediction.tolist()})
