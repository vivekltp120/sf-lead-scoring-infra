#!/bin/bash
set -e

zip -r lambda_package.zip lambda_function.py

aws lambda create-function --function-name lead-scoring-lambda   --zip-file fileb://lambda_package.zip --role arn:aws:iam::947288527335:role/sagemaker --runtime python3.9 --handler lambda_function.lambda_handler
