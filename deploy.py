# deploy.py
import boto3
from sagemaker.xgboost.model import XGBoostModel
from src.utils import get_logger
logger = get_logger("deploy_service")

sm = boto3.client("sagemaker")
asg = boto3.client("application-autoscaling")

role = "arn:aws:iam::947288527335:role/sagemaker"

endpoint_name = "xgb-lead-score-endpoint"
model_name = "xgboost-lead-score-model"
# --- Cleanup old endpoint + config + model ---
try:
    desc = sm.describe_endpoint(EndpointName=endpoint_name)
    endpoint_config_name = desc["EndpointConfigName"]

    logger.info(f"Deleting old endpoint: {endpoint_name}")
    sm.delete_endpoint(EndpointName=endpoint_name)

    logger.info(f"Deleting old endpoint config: {endpoint_config_name}")
    sm.delete_endpoint_config(EndpointConfigName=endpoint_config_name)

    logger.info(f"Deleting old model: {endpoint_name}")
    sm.delete_model(ModelName=endpoint_name)

except sm.exceptions.ClientError:
    logger.info("No existing endpoint to clean up.")



model = XGBoostModel(
    name=model_name,
    model_data="s3://salesforce-models/models/xgboost_model.tar.gz",
    role=role,
    entry_point="src/inference.py",   # only if you have custom logic
    framework_version="1.7-1"
)

# Deploy the model to create a SageMaker endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name=endpoint_name,
    wait=True
)
logger.info(f"Endpoint in service: {endpoint_name}")

# Register scaling target
resource_id = f"endpoint/{endpoint_name}/variant/AllTraffic"
asg.register_scalable_target(
    ServiceNamespace="sagemaker",
    ResourceId=resource_id,
    ScalableDimension="sagemaker:variant:DesiredInstanceCount",
    MinCapacity=1,
    MaxCapacity=6,
)

# Target tracking policy (approx 300 req/s per instance, tune for your model)
asg.put_scaling_policy(
    PolicyName=f"{endpoint_name}-rps-scaling",
    ServiceNamespace="sagemaker",
    ResourceId=resource_id,
    ScalableDimension="sagemaker:variant:DesiredInstanceCount",
    PolicyType="TargetTrackingScaling",
    TargetTrackingScalingPolicyConfiguration={
        "TargetValue": 300.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
        },
        "ScaleInCooldown": 120,
        "ScaleOutCooldown": 60,
    },
)

logger.info("Deployed:{}".format(endpoint_name))
