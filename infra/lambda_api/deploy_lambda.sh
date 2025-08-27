#!/bin/bash
set -e
zip predictor_lambda.zip predictor_lambda.py 

#aws lambda update-function-code --function-name lead-scoring-lambda --zip-file fileb://lambda_package.zip
# aws lambda create-function --function-name lead-scoring-lambda   --zip-file fileb://lambda_package.zip --role arn:aws:iam::947288527335:role/sagemaker --runtime python3.9 --handler lambda_function.lambda_handler
# aws lambda create-function --function-name predictor-lambda   --zip-file fileb://predictor_lambda.zip --role arn:aws:iam::947288527335:role/sagemaker --runtime python3.9 --handler predictor_lambda.lambda_handler
aws lambda update-function-code --function-name predictor-lambda   --zip-file fileb://predictor_lambda.zip
