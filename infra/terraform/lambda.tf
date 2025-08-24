resource "aws_iam_role" "lambda_exec" {
  name = "lead-scoring-lambda-exec"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "null_resource" "package_lambda" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "cd ${path.module}/lambda_code && zip -r ${path.module}/lambda_package.zip ."
  }
}

resource "aws_lambda_function" "lead_scoring" {
  function_name    = "lead_scorer"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "app.handler"
  runtime          = "python3.12"

  filename         = "${path.module}/lambda_package.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda_package.zip")

  depends_on = [null_resource.package_lambda]
}

resource "aws_apigatewayv2_api" "lead_scoring_api" {
  name          = "LeadScoringAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.lead_scoring_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.lead_scoring.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "predict_route" {
  api_id    = aws_apigatewayv2_api.lead_scoring_api.id
  route_key = "POST /score"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lead_scoring.function_name
  principal     = "apigateway.amazonaws.com"
}
