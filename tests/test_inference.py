import json
import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from src import inference

# ------------------------
# Fixtures
# ------------------------
@pytest.fixture(scope="module")
def model(tmp_path_factory):
    """Train a small multi-class XGB model and save to disk."""
    from xgboost import XGBClassifier

    X = np.random.rand(20, 5)
    y = np.random.randint(0, 5, size=20)
    clf = XGBClassifier(objective="multi:softprob", num_class=5, use_label_encoder=False)
    clf.fit(X, y)

    model_path = tmp_path_factory.mktemp("model") / inference.MODEL_FILENAME
    clf.save_model(model_path)

    return inference.model_fn(str(model_path.parent))


# ------------------------
# Unit Tests
# ------------------------
def test_model_fn(model):
    assert model is not None
    assert hasattr(model, "predict")


def test_input_fn_valid():
    body = "[[0.1, 0.2, 0.3, 0.4, 0.5]]"
    arr = inference.input_fn(body, "application/json")
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (1, 5)


def test_input_fn_invalid():
    with pytest.raises(ValueError):
        inference.input_fn("test", "text/csv")


def test_predict_fn(model):
    data = np.random.rand(2, 5)
    preds = inference.predict_fn(data, model)
    assert isinstance(preds, np.ndarray)
    assert preds.shape == (2,)  # class labels, not probs


def test_output_fn_json():
    preds = np.array([1, 3, 2])
    output = inference.output_fn(preds, "application/json")
    parsed = json.loads(output)
    assert "predictions" in parsed
    assert parsed["predictions"] == [1, 3, 2]


# ------------------------
# Mocked SageMaker runtime
# ------------------------
def test_sagemaker_runtime_invoke(monkeypatch):
    """Simulate SageMaker invoke_endpoint call."""
    mock_response = {
        "Body": MagicMock(read=lambda: json.dumps({"predictions": [1, 2, 0]}).encode("utf-8"))
    }

    mock_client = MagicMock()
    mock_client.invoke_endpoint.return_value = mock_response

    with patch("boto3.client", return_value=mock_client):
        import boto3
        client = boto3.client("sagemaker-runtime")

        response = client.invoke_endpoint(
            EndpointName="fake-endpoint",
            ContentType="application/json",
            Body=json.dumps([[0.5, 0.2, 0.1, 0.0, 0.2]])
        )

        body = json.loads(response["Body"].read())
        assert "predictions" in body
        assert isinstance(body["predictions"], list)
