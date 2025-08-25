output "endpoint_name" {
  value = module.xgboost_sagemaker.sagemaker_endpoint_name
}

output "endpoint_arn" {
  value = module.xgboost_sagemaker.sagemaker_endpoint_arn
}

output "s3_model_path" {
  value = module.xgboost_sagemaker.s3_model_path
}

output "sagemaker_role_arn" {
  value = module.xgboost_sagemaker.sagemaker_role_arn
}