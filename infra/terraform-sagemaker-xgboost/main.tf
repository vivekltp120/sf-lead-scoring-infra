
module "xgboost_sagemaker" {
  source           = "./modules/sagemaker_model"
  aws_region       = "us-east-1"
  model_name       = "xgboost_model.json"
  endpoint_name    = "xgboost-serverless-endpoint"
  local_model_path = "/media/vivek/Data/Vivek/Interview_Prep/sf-lead-scoring-infra/model/xgboost_model.tar.gz"
  max_concurrency  = 5
  memory_size_in_mb = 2048
}