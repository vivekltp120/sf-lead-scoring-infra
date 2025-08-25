output "sagemaker_endpoint_name" {
  description = "Name of the deployed SageMaker endpoint"
  value       = aws_sagemaker_endpoint.serverless_endpoint.name
}

output "sagemaker_endpoint_arn" {
  description = "ARN of the deployed SageMaker endpoint"
  value       = aws_sagemaker_endpoint.serverless_endpoint.arn
}

output "s3_model_path" {
  description = "S3 path of the uploaded model"
  value       = "s3://${aws_s3_bucket.model_bucket.id}/${aws_s3_bucket_object.model_object.key}"
}

output "sagemaker_role_arn" {
  description = "IAM role ARN used by SageMaker"
  value       = aws_iam_role.sagemaker_role.arn
}