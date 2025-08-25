terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.55"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "model_bucket" {
  bucket = "${var.bucket_name}"
  acl    = "private"
}

resource "aws_s3_bucket_object" "model_object" {
  bucket = aws_s3_bucket.model_bucket.id
  key    = "xgboost_model.tar.gz"
  source = var.local_model_path
}

resource "aws_iam_role" "sagemaker_role" {
  name = "${var.role_name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "sagemaker.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_policy_attach" {
  role       = aws_iam_role.sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_sagemaker_model" "xgboost_model" {
  name               = var.model_name
  execution_role_arn = aws_iam_role.sagemaker_role.arn

  primary_container {
    image          = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:2.6-1-cpu-py39"
    model_data_url = aws_s3_bucket_object.model_object.id
  }
}

resource "aws_sagemaker_endpoint_configuration" "serverless_config" {
  name = "${var.model_name}-serverless-config"

  serverless_config {
    max_concurrency   = var.max_concurrency
    memory_size_in_mb = var.memory_size_in_mb
  }

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.xgboost_model.name
    initial_variant_weight = 1.0
  }
}

resource "aws_sagemaker_endpoint" "serverless_endpoint" {
  name                 = var.endpoint_name
  endpoint_config_name = aws_sagemaker_endpoint_configuration.serverless_config.name
}