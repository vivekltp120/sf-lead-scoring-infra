provider "aws" {
  region = "us-east-1"
}

# IAM Role for SageMaker + Lambda
resource "aws_iam_role" "lambda_role" {
  name = "sagemaker_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = ["lambda.amazonaws.com", "sagemaker.amazonaws.com"]
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "sagemaker_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# SageMaker Model
resource "aws_sagemaker_model" "xgb_model" {
  name               = "xgboost-model"
  execution_role_arn = aws_iam_role.lambda_role.arn

  primary_container {
    image          = "811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:1.5-1"
    model_data_url = var.model_data_url
  }
}

# Endpoint Config
resource "aws_sagemaker_endpoint_configuration" "xgb_config" {
  name = "xgboost-endpoint-config"

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.xgb_model.name
    initial_instance_count = 1
    instance_type          = "ml.m5.large"
  }
}

# Endpoint
resource "aws_sagemaker_endpoint" "xgb_endpoint" {
  name                 = "xgboost-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.xgb_config.name
}

# Lambda function
resource "aws_lambda_function" "predictor" {
  function_name = "predictor-lambda"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
  filename      = "${path.module}/lambda_package.zip"

  environment {
    variables = {
      SAGEMAKER_ENDPOINT = aws_sagemaker_endpoint.xgb_endpoint.name
    }
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "predict_api" {
  name = "predict-api"
}

resource "aws_api_gateway_resource" "predict_resource" {
  rest_api_id = aws_api_gateway_rest_api.predict_api.id
  parent_id   = aws_api_gateway_rest_api.predict_api.root_resource_id
  path_part   = "predict"
}

resource "aws_api_gateway_method" "predict_method" {
  rest_api_id   = aws_api_gateway_rest_api.predict_api.id
  resource_id   = aws_api_gateway_resource.predict_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "predict_integration" {
  rest_api_id = aws_api_gateway_rest_api.predict_api.id
  resource_id = aws_api_gateway_resource.predict_resource.id
  http_method = aws_api_gateway_method.predict_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.predictor.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.predictor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.predict_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "predict_deployment" {
  rest_api_id = aws_api_gateway_rest_api.predict_api.id
  stage_name  = "dev"
  depends_on  = [aws_api_gateway_integration.predict_integration]
}

# Enable API Gateway CloudWatch Logs
resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.lambda_role.arn
}

resource "aws_api_gateway_stage" "logging" {
  rest_api_id   = aws_api_gateway_rest_api.predict_api.id
  deployment_id = aws_api_gateway_deployment.predict_deployment.id
  stage_name    = "dev"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format = jsonencode({
      requestId        = "$context.requestId"
      ip               = "$context.identity.sourceIp"
      requestTime      = "$context.requestTime"
      httpMethod       = "$context.httpMethod"
      resourcePath     = "$context.resourcePath"
      status           = "$context.status"
      responseLatency  = "$context.responseLatency"
    })
  }
}

resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/apigateway/predict-api"
  retention_in_days = 7
}
