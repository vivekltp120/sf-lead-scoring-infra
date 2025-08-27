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
        "body": "{\"input_data\": [[50 input features][50 input features][50 input features]]"
    }
"""
import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO) # Set desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)



runtime = boto3.client("sagemaker-runtime")
SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "xgb-lead-score-endpoint")



def lambda_handler(event, context):
    body = event.get("body",None)
    # If body is string → parse JSON
    logger.info("body-{0} type-{1}".format(body,type(body)))
    if body is None:
        logger.error("No body provided in the request")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "No body provided in the request"
            })
        }
    if isinstance(body, str):
        body = json.loads(body)
    # If body is already dict → leave as is
    data = body["input_data"]
    response = runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT,
        ContentType="application/json",
        Body=json.dumps(data)  # wrap in list
    )

    result = json.loads(response["Body"].read().decode("utf-8"))
    logger.info(f"Prediction result: {result}")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": result,
            "request_id": context.aws_request_id
        })
    }

