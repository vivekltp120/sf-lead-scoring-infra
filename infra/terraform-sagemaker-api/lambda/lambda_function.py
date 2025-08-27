import os
import boto3
import json

runtime = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = os.environ["SAGEMAKER_ENDPOINT"]

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        payload = json.dumps(body["input_data"])
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=payload
        )

        result = json.loads(response["Body"].read().decode())
        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": result})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
