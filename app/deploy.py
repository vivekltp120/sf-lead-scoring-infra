# deploy.py
import boto3, time
from sagemaker.xgboost.model import XGBoostModel
from utils import get_logger
logger = get_logger("deploy_service")

sm = boto3.client("sagemaker")
asg = boto3.client("application-autoscaling")

role = "arn:aws:iam::947288527335:role/sagemaker"

model = XGBoostModel(
    model_data="s3://salesforce-models/models/xgboost_model.tar.gz",
    role=role,
    entry_point="app/inference.py",   # only if you have custom logic
    framework_version="1.5-1"
)




endpoint_name = f"xgb-endpoint-{int(time.time())}"
logger.info(f"Deploying endpoint: {endpoint_name}")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name=endpoint_name,
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

print("Deployed:", endpoint_name)
