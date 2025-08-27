"""
Lambda function for real-time lead scoring using an AWS SageMaker endpoint.

This function receives an event from AWS API Gateway, extracts input features from the request body,
invokes a SageMaker endpoint for prediction, and returns the prediction result along with the AWS request ID.

Environment Variables:
    SAGEMAKER_ENDPOINT (str): Name of the SageMaker endpoint to invoke. Defaults to 'lead-scoring-endpoint'.

Request Format:
    The event should contain a JSON body with an 'input_data' field containing the features for prediction.

Response Format:
    On success: Returns a JSON object with the prediction and AWS request ID.
    On error: Returns a JSON object with an error message.

Example event:
    {
        "body": "{\"input_data\": {\"feature1\": value1, \"feature2\": value2, ...}}"
    }
"""

from sagemaker import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer
import numpy as np
import json
import os

SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "lead-scoring-endpoint")

def lambda_handler(event, context):
    """
    AWS Lambda handler for lead scoring prediction.

    Args:
        event (dict): Event data passed by AWS Lambda, expected to contain a 'body' field with input features.
        context (LambdaContext): AWS Lambda context object.

    Returns:
        dict: API Gateway-compatible response with status code and JSON body.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        data = body.get("input_data", {})
        if not data:
            raise ValueError("No features provided in the request body.")
        predictor = Predictor(endpoint_name=SAGEMAKER_ENDPOINT,
                            serializer=JSONSerializer(),
                                        deserializer=JSONDeserializer())
        response = predictor.predict(data)
        response['aws_request_id'] = context.aws_request_id   
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
