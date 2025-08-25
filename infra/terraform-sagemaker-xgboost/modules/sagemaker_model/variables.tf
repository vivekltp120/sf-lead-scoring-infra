variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "model_name" {
  description = "SageMaker model name"
  type        = string
  default     = "xgboost_model.json"
}

variable "role_name" {
  description = "SageMaker model name"
  type        = string
  default     = "sagemaker"
}


variable "endpoint_name" {
  description = "SageMaker serverless endpoint name"
  type        = string
  default     = "None"
}

variable "bucket_name" {
  description = "S3 bucket from where model will be loaded"
  type        = string
  default     = "s3://salesforce-models/models/"
}


variable "local_model_path" {
  description = "Local path to model tar.gz"
  type        = string
  default ="/media/vivek/Data/Vivek/Interview_Prep/sf-lead-scoring-infra/model/xgboost_model.tar.gz"
}

variable "max_concurrency" {
  description = "Max concurrent requests for serverless endpoint"
  type        = number
  default     = 5
}

variable "memory_size_in_mb" {
  description = "Memory for serverless endpoint"
  type        = number
  default     = 2048
}