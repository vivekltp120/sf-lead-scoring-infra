import json
import os
import boto3


SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "lead-scoring-endpoint")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        features = body.get("features", {})

        runtime = boto3.client("sagemaker-runtime")
        response = runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType="application/json",
            Body=json.dumps({"features": features})
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
